#!/usr/bin/env python3
"""掃描 wiki/ 下所有頁面，改寫 index.html 中 PAGES 標記之間的清單。"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
INDEX = ROOT / "index.html"
START, END = "<!-- PAGES:START -->", "<!-- PAGES:END -->"


def page_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix == ".html":
        m = re.search(r"<title>(.*?)</title>", text, re.S | re.I) or \
            re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S | re.I)
        if m:
            return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    else:
        for line in text.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return path.stem


def main() -> None:
    pages = sorted(
        p for p in WIKI.rglob("*")
        if p.is_file() and p.suffix in {".html", ".md"}
    )
    if pages:
        items = "\n".join(
            f'      <li><a href="{html.escape(p.relative_to(ROOT).as_posix())}">'
            f"{html.escape(page_title(p))}</a>"
            f'<span class="path">{html.escape(p.relative_to(ROOT).as_posix())}</span></li>'
            for p in pages
        )
        block = f'{START}\n    <ul class="pages">\n{items}\n    </ul>\n    {END}'
    else:
        block = f'{START}\n    <p class="empty">wiki/ 目前還沒有頁面。</p>\n    {END}'

    src = INDEX.read_text(encoding="utf-8")
    out = re.sub(re.escape(START) + r".*?" + re.escape(END), block, src, flags=re.S)
    out = re.sub(r'(<span id="count">)\d+(</span>)', rf"\g<1>{len(pages)}\g<2>", out)
    INDEX.write_text(out, encoding="utf-8")
    print(f"index.html 已更新：{len(pages)} 個頁面")


if __name__ == "__main__":
    main()
