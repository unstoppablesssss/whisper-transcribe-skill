# Whisper 本地转写技能

把音频文件（mp3/m4a/wav/aiff）转成带时间戳的逐字稿（txt）。全部本地运行，录音不出门。

## 何时使用本技能

- 学生/用户说「转写这个录音」「把访谈变成文字」「语音转文字」
- 用户提到 interviews/ 目录里的音频需要处理
- 用户安装了本仓库（见下）

## 首次安装（AI 自主完成，不要问用户技术细节）

检查是否已装：

```bash
test -f .venv/bin/python && .venv/bin/python -c "import faster_whisper" 2>/dev/null && echo INSTALLED
```

未安装则执行：

```bash
bash install.sh
```

install.sh 会自动：创建独立 venv → 安装 faster-whisper（开源，含 CPU 推理）→ 验证导入 → 打印 OK。
**安装中遇到报错**：先读报错原文；常见解法见文末「故障排查」。连续失败 2 次再求助用户。

## 使用方法（每次转写）

```bash
.venv/bin/python transcribe.py <音频文件路径>
# 可选参数：--model small（更准，下载更大） 默认 base（快，中文可用）
```

- 输出：`transcripts/<原文件名>.txt`（纯文本逐字稿，带 [MM:SS] 时间戳）
- 首次使用某模型会自动下载权重（base ≈ 145MB，small ≈ 480MB），需要网络；
  下载完成后**转写全程离线**
- 中文音频建议 base 起步；效果不满意升级 small
- 时间戳是跳跃的属正常：VAD 已自动剔除停顿/静音/呼吸声（见 AUDIO_CLEANING.md）

## 验证安装成功（AI 必须跑通后才算完成）

用 OpenAI 官方测试音频（真人语音，10 秒英文）验证全链路：

```bash
curl -sL -o /tmp/jfk.flac https://github.com/openai/whisper/raw/main/tests/jfk.flac
.venv/bin/python transcribe.py /tmp/jfk.flac
cat transcripts/jfk.txt
# 正确输出应包含: "And so my fellow Americans, ask not what your country
#                  can do for you, ask what you can do for your country."
.venv/bin/python to_blog.py transcripts/jfk.txt --title "安装验证"   # 顺手验证博客档
```

⚠️ 不要用 `say` 命令生成测试音频——部分环境下输出为空文件，会误判为转写故障。
向用户报告时附上验证输出原文。

## 给学生的推荐用法（集成进工作流）

访谈录音统一放入 `interviews/`，命名 `受访者_日期`。批量转写+博客：

```bash
for f in interviews/*.m4a; do .venv/bin/python transcribe.py "$f"; done
.venv/bin/python to_blog.py transcripts/*.txt
```

转写稿自动落在 transcripts/，博客页落在 blog/——后续笔记工作流直接消费。

## 三档方案速查

- **云 API 档**（最方便，有免费额度）：读 [CLOUD_APIS.md](CLOUD_APIS.md)
- **本地档**（最私密，零成本）：本文件
- **音频清理**（气泡音/停顿）：[AUDIO_CLEANING.md](AUDIO_CLEANING.md) —— 本脚本默认已开 VAD 自动过滤

## 故障排查（AI 先自查）

| 症状 | 处理 |
|---|---|
| pip 安装超时 | 换源：`uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple faster-whisper` |
| 模型下载失败 | 重试一次；或手动 `export HF_ENDPOINT=https://hf-mirror.com` 后重跑 |
| 转写很慢 | 正常（CPU 推理）。换 `--model tiny` 或耐心等待；长音频按 10 分钟一段切分 |
| 中文全是错字 | 升级 `--model small`；转写前先改录音质量（问题多半在音频本身） |
| m4a 不识别 | 脚本已自动 afconvert 转 wav；若报错说明系统异常，走云端档 |
| 转写 0 段 | 先确认音频本身有声音（`afinfo 文件` 看时长）。音频正常但 0 段 → 升级 `--model small` |

## 依赖清单

- Python 3.10+（macOS 自带即可）
- faster-whisper（CTranslate2 后端，CPU 可跑，比原版 whisper 快 4 倍）
- 无 GPU 要求、无订阅、无网络依赖（模型下载后）
