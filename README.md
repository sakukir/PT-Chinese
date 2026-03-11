# 🚀 PT-Chinese
PT-Chinese 是一个适用于 Cisco Packet Tracer 9.0.0 的中文汉化包。 使用 DeepSeek 大模型进行翻译，配合提示词。

**基于 DeepSeek AI 的思科模拟器汉化包**  
*让 Cisco Packet Tracer 更贴近中文用户！*

---

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Version](https://img.shields.io/badge/Version-9.0.0-brightgreen)
![GitHub Stars](https://img.shields.io/github/stars/sakukir/PT-Chinese?style=social)
![GitHub Forks](https://img.shields.io/github/forks/sakukir/PT-Chinese?style=social)

---

## 📜 项目简介

**PT-Chinese** 是一个适用于 **Cisco Packet Tracer 9.0.0** 的中文汉化包。  
使用 **DeepSeek** 大模型进行翻译，配合专业的网络术语提示词，翻译质量自然、准确。

---

## 🌟 主要特点

- **AI 高质量翻译**：使用 DeepSeek 大模型，针对网络模拟器专业术语定制提示词，确保术语统一准确
- **术语规范统一**：路由器、交换机、数据包、拓扑等专业词汇全程统一翻译
- **易于安装**：只需将文件拖入指定文件夹即可完成汉化
- **开源透明**：翻译脚本完全开源，欢迎自行改进

---

## 🛠️ 使用方法

### 1. 下载汉化包

从 [Releases 页面](https://github.com/sakukir/PT-Chinese/releases) 下载 `Chinese.ptl` 文件。

### 2. 安装汉化包

将 `Chinese.ptl` 放入 Cisco Packet Tracer 安装目录下的 `languages` 文件夹：

```
C:\Program Files\Cisco Packet Tracer 9.0.0\languages\
```

### 3. 启用汉化

打开 Cisco Packet Tracer，依次点击：

```
Options → Preferences → Interface
```

在语言选项中选择 `Chinese.ptl`，点击 **Change Language**，重启软件即可。

---

## 🧩 项目背景

网上现有的 Cisco Packet Tracer 汉化包大多基于旧版本或翻译质量参差不齐。  
本项目使用 DeepSeek 大模型，针对网络模拟器场景定制翻译提示词，对 9599 条界面文本进行了全量翻译，力求做到专业、自然、统一。

---

## 🤖 翻译方式

| 项目 | 说明 |
|------|------|
| 翻译模型 | DeepSeek `deepseek-chat` |
| 原始文件 | `default.ts`（Qt 翻译源文件） |
| 翻译条数 | 9599 条 |
| 打包工具 | Qt Linguist |

翻译脚本已开源，见 [`translate_ts.py`](./translate_ts.py)。

---

此项目由ai生成，不喜勿喷

---

## 📜 许可证

本项目采用 [MIT 许可证](./LICENSE)。
