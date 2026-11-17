#!/usr/bin/env python3
"""掃描 pages/*.html，依 <meta name="category"> 分類，改寫 index.html 的卡片區。"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
INDEX = ROOT / "index.html"
START, END = "<!-- CARDS:START -->", "<!-- CARDS:END -->"

# 分類順序與圖示；新增分類時請同步更新 agents.md
CATEGORIES = {
    "下肢肌力": "🦵",
    "平衡防跌": "🧍",
    "心肺有氧": "❤️",
    "柔軟伸展": "🤸",
    "上肢肌力": "💪",
}
OTHER = "其他"


def meta(text: str, name: str) -> str:
    m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', text, re.I)
    return m.group(1).strip() if m else ""


def title(text: str, fallback: str) -> str:
    m = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
    return m.group(1).strip() if m else fallback


def main() -> None:
    groups: dict[str, list[tuple[str, str, str]]] = {}
    files = sorted(PAGES.glob("*.html"))
    for p in files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        cat = meta(t, "category") or OTHER
        if cat not in CATEGORIES:
            print(f"警告：{p.name} 的分類「{cat}」不在 CATEGORIES 中，暫列入「{OTHER}」")
            cat = OTHER
        groups.setdefault(cat, []).append(
            (f"pages/{p.name}", title(t, p.stem), meta(t, "description"))
        )

    order = list(CATEGORIES) + [OTHER]
    parts = []
    for cat in order:
        items = groups.get(cat, [])
        if not items and cat == OTHER:
            continue
        icon = CATEGORIES.get(cat, "📄")
        parts.append(f'    <section class="cat">\n      <h2>{icon} {html.escape(cat)}'
                     f'<span class="n">{len(items)} 篇</span></h2>')
        if items:
            parts.append('      <div class="grid">')
            for href, t, d in items:
                parts.append(
                    f'        <a class="card" href="{html.escape(href)}">'
                    f'<h3>{html.escape(t)}</h3><p>{html.escape(d)}</p>'
                    f'<span class="go">閱讀 →</span></a>'
                )
            parts.append("      </div>")
        else:
            parts.append('      <p class="empty">尚無內容</p>')
        parts.append("    </section>")

    block = START + "\n" + "\n".join(parts) + "\n    " + END
    src = INDEX.read_text(encoding="utf-8")
    out = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, src, flags=re.S)
    out = re.sub(r'(<span id="count">)\d+(</span>)', rf"\g<1>{len(files)}\g<2>", out)
    INDEX.write_text(out, encoding="utf-8")
    print(f"index.html 已更新：共 {len(files)} 篇")


if __name__ == "__main__":
    main()
