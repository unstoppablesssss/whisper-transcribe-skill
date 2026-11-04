# -*- coding: utf-8 -*-
"""本地语音转文字 · faster-whisper
用法: transcribe.py <音频文件> [--model base|small|tiny]
输出: transcripts/<原文件名>.txt
"""
import argparse, pathlib, subprocess, sys, os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('audio')
    ap.add_argument('--model', default='base', choices=['tiny', 'base', 'small'])
    a = ap.parse_args()

    src = pathlib.Path(a.audio).expanduser()
    if not src.exists():
        sys.exit(f'文件不存在: {src}')

    out_dir = pathlib.Path(__file__).parent / 'transcripts'
    out_dir.mkdir(exist_ok=True)

    # 非 wav 先用系统 afconvert 转 wav（macOS 自带，免 ffmpeg 依赖）
    if src.suffix.lower() != '.wav':
        wav = out_dir / (src.stem + '.wav')
        subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16@16000',
                        str(src), str(wav)], check=True,
                       capture_output=True)
    else:
        wav = src

    # 模型权重首次自动下载（~145MB base），之后完全离线
    from faster_whisper import WhisperModel
    print(f'加载模型 {a.model}（首次会自动下载权重，请稍等）...')
    model = WhisperModel(a.model, device='cpu', compute_type='int8')
    print('转写中（CPU，1 小时录音约 5-15 分钟）...')
    segments, info = model.transcribe(str(wav), language=None, vad_filter=True)

    lines, lang = [], info.language
    for seg in segments:
        ts = f'[{int(seg.start//60):02d}:{int(seg.start%60):02d}]'
        lines.append(f'{ts} {seg.text.strip()}')

    out = out_dir / (src.stem + '.txt')
    out.write_text(
        f'# 转写稿 · {src.stem}\n# 模型: faster-whisper {a.model} · 语言: {lang}\n\n'
        + '\n'.join(lines) + '\n', encoding='utf-8')
    print(f'完成 → {out}（{len(lines)} 段，语言 {lang}）')

if __name__ == '__main__':
    main()
