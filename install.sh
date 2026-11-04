#!/bin/bash
# Whisper 本地转写 · 一键安装（学生把链接丢给 AI，AI 执行本脚本即可）
set -e
cd "$(dirname "$0")"

echo "==> [1/4] 检查 Python"
PY=python3
command -v $PY >/dev/null || { echo "未找到 python3，请先安装"; exit 1; }
$PY --version

echo "==> [2/4] 创建独立环境"
if command -v uv >/dev/null 2>&1; then
  echo "使用 uv"
  uv venv .venv --python 3.11 2>/dev/null || uv venv .venv
  UV=1
else
  $PY -m venv .venv
  UV=0
fi

echo "==> [3/4] 安装 faster-whisper（开源推理引擎，CPU 可跑）"
if [ "$UV" = "1" ]; then
  uv pip install --python .venv/bin/python faster-whisper || \
  uv pip install --python .venv/bin/python --index-url https://pypi.tuna.tsinghua.edu.cn/simple faster-whisper
else
  .venv/bin/pip install --quiet --upgrade pip
  .venv/bin/pip install faster-whisper || \
  .venv/bin/pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple faster-whisper
fi

echo "==> [4/4] 验证安装"
.venv/bin/python - <<'EOF'
from faster_whisper import WhisperModel
import sys
# 仅验证导入（模型权重首次转写时自动下载）
try:
    from faster_whisper.audio import decode_audio
    print("IMPORT OK")
except Exception as e:
    print("IMPORT FAIL:", e); sys.exit(1)
EOF

mkdir -p transcripts
echo ""
echo "=============================================="
echo " 安装完成 ✔"
echo " 验证转写：say -o /tmp/t.aiff 安装测试 --data-format=LEF32@16000"
echo "           .venv/bin/python transcribe.py /tmp/t.aiff"
echo "=============================================="
