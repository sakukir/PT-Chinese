"""
Cisco Packet Tracer .ts 汉化脚本 —— DeepSeek API 版
用法：
    pip install openai lxml
    python translate_ts.py default.ts Chinese.ts
"""

import sys
import time
import re
import os
import json
from lxml import etree
from openai import OpenAI

# ===================== 配置区 =====================
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "输入你的密钥")
MODEL_NAME       = "deepseek-chat"
BATCH_SIZE       = 40    # DeepSeek 速率限制宽松，可以多一点
RETRY_TIMES      = 3
RETRY_DELAY      = 5
# ==================================================

SYSTEM_PROMPT = """你是一名专业的软件本地化翻译专家，正在翻译思科 Packet Tracer 网络模拟器的界面文本。

翻译要求：
1. 目标语言：简体中文
2. 风格：简洁、专业，符合软件界面习惯
3. 专业术语统一翻译规范：
   - Router → 路由器
   - Switch → 交换机
   - Hub → 集线器
   - Firewall → 防火墙
   - Packet → 数据包
   - Frame → 帧
   - Topology → 拓扑
   - Simulation → 仿真
   - Realtime → 实时
   - Interface → 接口（硬件）/ 界面（UI）根据上下文判断
   - Port → 端口
   - Gateway → 网关
   - Subnet → 子网
   - Bandwidth → 带宽
   - Latency → 延迟
   - Protocol → 协议
   - Configure → 配置
   - Debug → 调试
   - Enable → 启用
   - Disable → 禁用
4. 以下内容保持原文不翻译：
   - URL（http://...）
   - 占位符（%1、%2、{name} 等）
   - 纯数字或单位
   - 产品型号（如 Cisco 2811）
   - 命令行指令（如 show ip route）
5. 菜单项、按钮文字要简短（通常2-4个汉字）

输入格式：JSON 数组，每项包含 id 和 source 字段
输出格式：JSON 数组，每项包含 id 和 translation 字段，只输出 JSON，不要加任何说明或 markdown 代码块"""


def should_skip(text: str) -> bool:
    patterns = [
        r'^https?://',
        r'^\s*$',
        r'^[\d\s\.\,\-\_\:\+\=\/\\]+$',
        r'^\%\d+$',
        r'^\{[^}]+\}$',
    ]
    return any(re.match(p, text.strip()) for p in patterns)


def translate_batch(client, items: list) -> dict:
    data = [{"id": i["id"], "source": i["source"]} for i in items]
    prompt = f"请翻译以下界面文本：\n{json.dumps(data, ensure_ascii=False, indent=2)}"

    for attempt in range(RETRY_TIMES):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
            )
            text = response.choices[0].message.content.strip()
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```\s*', '', text)
            results = json.loads(text)
            return {str(item["id"]): item["translation"] for item in results}

        except json.JSONDecodeError as e:
            print(f"  [警告] JSON解析失败 (第{attempt+1}次): {e}")
            if attempt < RETRY_TIMES - 1:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"  [警告] API请求失败 (第{attempt+1}次): {e}")
            if attempt < RETRY_TIMES - 1:
                time.sleep(RETRY_DELAY)

    return {}


def translate_ts(input_file: str, output_file: str):
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",
    )

    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(input_file, parser)
    root = tree.getroot()

    all_items = []
    translation_nodes = {}

    for idx, t in enumerate(root.findall('.//translation')):
        if t.text and t.text.strip():
            continue

        message = t.getparent()
        source = message.find('source')
        if source is None or not source.text:
            continue

        src = source.text.strip()

        if should_skip(src):
            t.text = src
            if 'type' in t.attrib:
                del t.attrib['type']
            continue

        all_items.append({"id": str(idx), "source": src})
        translation_nodes[str(idx)] = t

    total = len(all_items)
    print(f"共 {total} 条需要翻译，每批 {BATCH_SIZE} 条，使用模型 {MODEL_NAME}\n")

    done = 0
    for batch_start in range(0, total, BATCH_SIZE):
        batch = all_items[batch_start: batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"[批次 {batch_num}/{total_batches}] 翻译 {len(batch)} 条...", end=" ", flush=True)

        results = translate_batch(client, batch)

        for item in batch:
            translated = results.get(item["id"])
            node = translation_nodes[item["id"]]

            if translated:
                node.text = translated
                if 'type' in node.attrib:
                    del node.attrib['type']
                done += 1
            else:
                node.text = item["source"]

        print(f"✓ 累计 {done}/{total}")

        # 每10批保存一次进度，防止中途崩溃丢失
        if batch_num % 10 == 0:
            tree.write(output_file, encoding='utf-8', xml_declaration=True, pretty_print=True)
            print(f"  [进度已保存 → {output_file}]")

        if batch_start + BATCH_SIZE < total:
            time.sleep(0.5)

    tree.write(output_file, encoding='utf-8', xml_declaration=True, pretty_print=True)
    print(f"\n✅ 翻译完成！共 {done}/{total} 条成功")
    print(f"输出文件：{output_file}")
    print("\n下一步：用 Qt Linguist 打开输出文件 → File → Release as → 后缀改为 .ptl")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python translate_ts.py <输入.ts> <输出.ts>")
        print("示例: python translate_ts.py default.ts Chinese.ts")
        sys.exit(1)

    translate_ts(sys.argv[1], sys.argv[2])
