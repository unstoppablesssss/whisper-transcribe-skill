# -*- coding: utf-8 -*-
"""转写稿 → 可分享的博客页面
用法: to_blog.py transcripts/xxx.txt [--title "标题"]
输出: blog/xxx.html（可直接浏览器打开 / 拖进任何静态托管）
"""
import argparse, html, pathlib, re, datetime

STYLE = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<style>
:root{--bg:#0B0B0F;--ink:#F4F1E8;--ink2:#B9B4A8;--amb:#E8A33D;--line:rgba(244,241,232,.1)}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:-apple-system,'PingFang SC',sans-serif;
line-height:2;font-size:16.5px;padding:0 20px}
main{max-width:720px;margin:0 auto;padding:64px 0 100px}
h1{font-size:30px;letter-spacing:-.02em;margin-bottom:6px}
.meta{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:#8B867C;margin-bottom:44px}
.meta b{color:var(--amb)}
.line{padding:9px 0 9px 14px;border-left:1px solid var(--line)}
.line:hover{border-left-color:var(--amb);background:rgba(232,163,61,.05)}
.ts{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--amb);
display:inline-block;width:52px;margin-right:10px;user-select:none}
</style></head><body><main>
<h1>{title}</h1>
<div class="meta">{date} · <b>{n} 段</b> · {lang} · faster-whisper {model}</div>
{body}
<p style="margin-top:60px;font-family:ui-monospace;font-size:11px;color:#5A564E">
由 whisper-transcribe-skill 生成 · 本地转写 · 时间戳可定位回原音频</p>
</main></body></html>"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('transcript')
    ap.add_argument('--title', default=None)
    a = ap.parse_args()
    src = pathlib.Path(a.transcript)
    txt = src.read_text(encoding='utf-8')

    title = a.title or re.search(r'# 转写稿 · (.+)', txt).group(1)
    lang = re.search(r'语言: (\S+)', txt)
    model = re.search(r'模型: faster-whisper (\S+)', txt)

    body = []
    for ln in txt.splitlines():
        m = re.match(r'\[(\d+:\d+)\]\s*(.+)', ln)
        if m and m.group(2).strip():
            body.append(f'<div class="line"><span class="ts">{m.group(1)}</span>'
                        f'{html.escape(m.group(2))}</div>')
    n = len(body)
    page = (STYLE.replace('{title}', html.escape(title))
                 .replace('{date}', datetime.date.today().isoformat())
                 .replace('{n}', str(n))
                 .replace('{lang}', lang.group(1) if lang else '—')
                 .replace('{model}', model.group(1) if model else '—')
                 .replace('{body}', '\n'.join(body)))
    out = pathlib.Path(__file__).parent / 'blog'
    out.mkdir(exist_ok=True)
    f = out / (src.stem + '.html')
    f.write_text(page, encoding='utf-8')
    print(f'完成 → {f}（{n} 段）')

if __name__ == '__main__':
    main()
