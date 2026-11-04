# whisper-transcribe

本地语音转文字（开源 Whisper）。**给 AI 看的说明：把这个仓库链接发给你的 AI 助手，说「装这个」，它会自动完成一切。**

## 学生使用（一句话流程）

1. 把这个仓库的地址发给你的 AI（ChatGPT/Codex/Hermes）：

   > 「帮我安装这个：https://github.com/flaglee/whisper-transcribe-skill —— 装好后用一段音频验证给我看。」

2. AI 会：clone 仓库 → 读 SKILL.md → 跑 install.sh → 用系统语音生成测试音频 → 跑通转写 → 报告结果。

3. 之后每次转写：把录音文件路径发给 AI，说「转写」即可。

## 手动安装（不用 AI 时）

```bash
git clone <本仓库> && cd whisper-transcribe-skill
bash install.sh
.venv/bin/python transcribe.py 你的录音.m4a
```

## 文件说明

| 文件 | 用途 |
|---|---|
| SKILL.md | **AI 的说明书**（安装/使用/验证/排障，AI 读它就学会全部） |
| install.sh | 一键安装（venv + faster-whisper + 验证） |
| transcribe.py | 转写脚本（m4a/mp3/wav 自动转换，输出带时间戳 txt） |

## 特性

- 100% 本地运行，录音不出门（隐私）
- 无 GPU 要求，CPU 可跑；无订阅，全开源
- 中文/英文自动识别；输出带时间戳，方便回听核对
- m4a 直接支持（macOS afconvert 免装 ffmpeg）
