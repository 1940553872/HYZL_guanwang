"""解析 素材库/官网补录文字.txt，提取新闻、产品中心面板等结构化内容。

文本格式约定（来自内容整理文档 §09）：
- 图片块以 "A123  标题" 开头，随后为 "原图来源  images/..."、"图片文字识别：" 或
  "对照原图补录：" 以及一行识别文字，最后可能重复一行图片标题（图注）。
- OCR 文字不进入网站正文（design_document/03 §1）。
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

A_BLOCK = re.compile(r"^A\d{3}\s{2}(.+)$")
SRC_LINE = re.compile(r"^原图来源\s+(images/\S+)$")
CAPS_LINE = re.compile(r"^[A-Z][A-Z0-9 &,.\-–/()'+*]{5,}$")
NEWS_HEAD = re.compile(r"^(公司动态|行业资讯) (\d{2}) (.+)$")
NEWS_META = re.compile(r"^详情页日期与来源\s+发布时间：(\d{4}-\d{1,2}-\d{1,2})(?:\s+来源：(.+))?$")

# 已确认可直接修正的勘误（design_document/01 §5 中处理方式为“改”的条目）
TEXT_FIXES = [
    ("UPC-DA", "OPC DA"),
    ("BlueTeeth", "Bluetooth"),
    ("INDUSTRIIAL", "INDUSTRIAL"),
    ("数学孪生", "数字孪生"),
    ("UAC/UGV", "UAV/UGV"),
    ("INFOMATION", "INFORMATION"),
    ("Angluar", "Angular"),
    ("THML5", "HTML5"),
    ("IEC61***-3", "IEC 61131-3"),
    ("Agententic", "Agentic"),
]


def fix(text: str) -> str:
    for old, new in TEXT_FIXES:
        text = text.replace(old, new)
    return text.strip()


@dataclass
class Token:
    kind: str  # heading | para | image | caps
    text: str = ""
    src: str = ""


def load_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").split("\n")


def tokenize(lines: list[str]) -> list[Token]:
    """把一段原文切成标题 / 段落 / 图片三类记号，跳过 OCR 内容。"""
    tokens: list[Token] = []
    i = 0
    n = len(lines)
    last_image_title = None
    while i < n:
        raw = lines[i].strip()
        i += 1
        if not raw:
            continue
        m = A_BLOCK.match(raw)
        if m:
            title = m.group(1).strip()
            src = ""
            # 读取原图来源与 OCR 行
            while i < n:
                nxt = lines[i].strip()
                if not nxt:
                    i += 1
                    continue
                s = SRC_LINE.match(nxt)
                if s:
                    src = s.group(1)
                    i += 1
                    continue
                if nxt in ("图片文字识别：", "对照原图补录："):
                    i += 1
                    # 识别文字可能跨多行，直到空行后出现非识别内容；保守跳过紧随的一段
                    while i < n and lines[i].strip() == "":
                        i += 1
                    # 对照原图补录可能有多段，以“图注重复行”或下一个块为止
                    if nxt == "对照原图补录：":
                        while i < n:
                            t = lines[i].strip()
                            if t == title or A_BLOCK.match(t):
                                break
                            if t and (t.startswith("新闻详情") or NEWS_HEAD.match(t)):
                                break
                            i += 1
                    else:
                        i += 1
                    continue
                if nxt.startswith("未识别出可可靠提取的文字"):
                    i += 1
                    continue
                break
            tokens.append(Token("image", fix(title), src))
            last_image_title = title
            continue
        if last_image_title and raw == last_image_title:
            # 图注重复行
            last_image_title = None
            continue
        last_image_title = None
        if raw.startswith(("网页来源", "原图来源", "Copyright", "陕ICP备")):
            continue
        if CAPS_LINE.match(raw):
            tokens.append(Token("caps", fix(raw)))
            continue
        if "：" not in raw and len(raw) <= 40 and not raw.endswith(("。", "；", "，")):
            tokens.append(Token("heading", fix(raw)))
        else:
            tokens.append(Token("para", fix(raw)))
    return tokens


# ---------------------------------------------------------------- 新闻

@dataclass
class NewsItem:
    category: str
    no: int
    title: str
    date: str
    source: str | None
    blocks: list[dict] = field(default_factory=list)


def parse_news(lines: list[str]) -> list[NewsItem]:
    start = next(i for i, l in enumerate(lines) if l.strip() == "新闻详情全文")
    end = next(i for i, l in enumerate(lines) if l.strip() == "产品中心完整文字与图像")
    items: list[NewsItem] = []
    cur: NewsItem | None = None
    seg: list[str] = []

    def flush():
        if cur is None:
            return
        for t in tokenize(seg):
            if t.kind == "image":
                cur.blocks.append({"t": "img", "src": t.src, "alt": t.text.replace(" 配图", "").strip()})
            elif t.kind in ("para", "heading", "caps"):
                if t.text in ("新闻详情来源",):
                    continue
                cur.blocks.append({"t": "p", "text": t.text})

    for raw in lines[start + 1:end]:
        line = raw.strip()
        m = NEWS_HEAD.match(line)
        if m:
            flush()
            seg = []
            cur = NewsItem("company" if m.group(1) == "公司动态" else "industry", int(m.group(2)), fix(m.group(3)), "", None)
            items.append(cur)
            continue
        mm = NEWS_META.match(line)
        if mm and cur is not None:
            y, mo, d = mm.group(1).split("-")
            cur.date = f"{y}-{int(mo):02d}-{int(d):02d}"
            cur.source = mm.group(2).strip() if mm.group(2) else None
            continue
        seg.append(raw)
    flush()
    return items


# ---------------------------------------------------------------- 产品中心

@dataclass
class Panel:
    title: str
    en: str = ""
    positioning: str = ""
    overview: list[str] = field(default_factory=list)
    section_title: str = ""
    items: list[dict] = field(default_factory=list)  # {label,text} | {heading} | {p} | {img}
    images: list[dict] = field(default_factory=list)
    tables: list[dict] = field(default_factory=list)


def _split_panels(tokens: list[Token]) -> list[list[Token]]:
    """面板以“标题、重复标题、英文大写标题”三连开始。"""
    starts = []
    for k in range(len(tokens) - 2):
        a, b, c = tokens[k], tokens[k + 1], tokens[k + 2]
        if a.kind == "heading" and b.kind == "heading" and a.text == b.text and c.kind == "caps":
            starts.append(k)
    panels = []
    for idx, s in enumerate(starts):
        e = starts[idx + 1] if idx + 1 < len(starts) else len(tokens)
        panels.append(tokens[s:e])
    return panels


def parse_panels(lines: list[str]) -> list[Panel]:
    start = next(i for i, l in enumerate(lines) if l.strip() == "产品中心完整文字与图像")
    end = next(i for i, l in enumerate(lines) if l.strip() == "先进技术实验室完整文字与图像")
    tokens = tokenize(lines[start + 1:end])
    result: list[Panel] = []
    for group in _split_panels(tokens):
        p = Panel(title=group[0].text, en=group[2].text)
        mode = None
        table_title = None
        for t in group[3:]:
            if t.kind == "heading" and t.text == "产品定位":
                mode = "pos"; continue
            if t.kind == "heading" and t.text == "产品概述":
                mode = "ov"; continue
            if t.kind == "heading" and t.text.startswith(("核心", "三大能力单元")):
                p.section_title = t.text
                mode = "items"; continue
            if t.kind == "caps":
                continue
            if t.kind == "image":
                img = {"src": t.src, "alt": t.text}
                p.images.append(img)
                if mode == "items":
                    p.items.append({"img": img})
                continue
            if t.kind == "para" and "  ｜  " in t.text:
                cells = [c.strip() for c in t.text.split("｜")]
                if not p.tables or p.tables[-1].get("_title") != table_title:
                    p.tables.append({"_title": table_title, "title": table_title or "参数", "rows": []})
                p.tables[-1]["rows"].append(cells)
                continue
            if mode == "pos":
                p.positioning = (p.positioning + t.text).strip()
            elif mode == "ov":
                p.overview.append(t.text)
            elif mode == "items" or mode is None:
                if t.kind == "heading":
                    if t.text.endswith("参数"):
                        table_title = t.text
                        continue
                    p.items.append({"heading": t.text})
                elif "：" in t.text and t.text.index("：") <= 40:
                    label, text = t.text.split("：", 1)
                    p.items.append({"label": label.strip(), "text": text.strip()})
                else:
                    p.items.append({"p": t.text})
        for tb in p.tables:
            tb.pop("_title", None)
        result.append(p)
    return result


# ---------------------------------------------------------------- 简单段落区

def section_text(lines: list[str], begin: str, end: str) -> list[Token]:
    s = next(i for i, l in enumerate(lines) if l.strip() == begin)
    e = next(i for i, l in enumerate(lines) if i > s and l.strip() == end)
    return tokenize(lines[s + 1:e])


if __name__ == "__main__":
    import json
    import sys

    root = Path(__file__).resolve().parents[2]
    lines = load_lines(root / "素材库" / "官网补录文字.txt")
    if len(sys.argv) > 1 and sys.argv[1] == "news":
        for it in parse_news(lines):
            print(it.category, it.no, it.date, it.source, it.title, len(it.blocks))
    else:
        for p in parse_panels(lines):
            print(json.dumps({"title": p.title, "en": p.en, "pos": p.positioning[:40], "ov": len(p.overview),
                              "items": len(p.items), "imgs": [i["src"] for i in p.images], "tables": len(p.tables)},
                             ensure_ascii=False))
