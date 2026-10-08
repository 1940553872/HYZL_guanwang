#!/usr/bin/env python3
"""从 素材库/ 生成网站种子内容与媒体文件。

输出：
- website/apps/api/src/main/resources/seed/*.json   （后端启动时导入数据库）
- website/apps/web/public/media/**                  （转为 WebP 的图片，证书类加水印）

依据：design_document/02（内容呈现）、03（产品唯一清单、迁移映射、素材处理规范）、
assets/asset-mapping.csv（素材处理方式）。

用法：python3 website/tools/build_content.py [--skip-media]
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_site import fix, load_lines, parse_news, parse_panels, tokenize  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "素材库"
TXT = SRC / "官网补录文字.txt"
SEED = ROOT / "website" / "apps" / "api" / "src" / "main" / "resources" / "seed"
MEDIA = ROOT / "website" / "apps" / "web" / "public" / "media"

SKIP_MEDIA = "--skip-media" in sys.argv

# ------------------------------------------------------------------ 媒体处理

_media_cache: dict[str, dict] = {}
WATERMARK = "华云智联 · 仅用于官网展示"
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"


def _out_path(src_rel: str, suffix: str = "") -> tuple[Path, str]:
    rel = Path(src_rel)
    if rel.parts[0] == "images":
        rel = Path(*rel.parts[1:])
    target = rel.with_name(rel.stem + suffix + ".webp")
    return MEDIA / target, "/media/" + target.as_posix()


def _watermark(img):
    from PIL import Image, ImageDraw, ImageFont

    w, h = img.size
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    size = max(14, int(min(w, h) * 0.035))
    try:
        font = ImageFont.truetype(FONT, size)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), WATERMARK, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = int(size * 0.6)
    draw.rectangle([w - tw - pad * 2, h - th - pad * 2, w, h], fill=(255, 255, 255, 120))
    draw.text((w - tw - pad, h - th - pad - bbox[1]), WATERMARK, font=font, fill=(10, 26, 63, 150))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def media(src_rel: str, *, max_w: int = 1600, watermark: bool = False, thumb: tuple[int, int] | None = None) -> dict:
    """转换一张素材图片，返回 {src, w, h[, thumb]}。"""
    key = f"{src_rel}|{max_w}|{watermark}|{thumb}"
    if key in _media_cache:
        return _media_cache[key]
    src = SRC / src_rel
    out, url = _out_path(src_rel)
    info: dict = {"src": url}
    if SKIP_MEDIA:
        from PIL import Image
        with Image.open(src) as im:
            w, h = im.size
        scale = min(1.0, max_w / w)
        info.update(w=int(w * scale), h=int(h * scale))
        if thumb:
            info["thumb"] = _out_path(src_rel, "-thumb")[1]
        _media_cache[key] = info
        return info
    from PIL import Image

    out.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGBA") if im.mode in ("P", "LA", "RGBA") else im.convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        full = _watermark(im) if watermark else im
        full.save(out, "WEBP", quality=82, method=6)
        info.update(w=full.width, h=full.height)
        if thumb:
            tw, th = thumb
            canvas = Image.new("RGB", (tw, th), (255, 255, 255))
            t = im.convert("RGB").copy()
            t.thumbnail((tw - 24, th - 24), Image.LANCZOS)
            canvas.paste(t, ((tw - t.width) // 2, (th - t.height) // 2))
            if watermark:
                canvas = _watermark(canvas)
            tout, turl = _out_path(src_rel, "-thumb")
            canvas.save(tout, "WEBP", quality=80, method=6)
            info["thumb"] = turl
    _media_cache[key] = info
    return info


def logos() -> dict:
    """Logo：彩色版原样转换；反白版把深蓝像素改为白色（临时方案，待矢量源文件）。"""
    out_dir = MEDIA / "brand"
    out_dir.mkdir(parents=True, exist_ok=True)
    if not SKIP_MEDIA:
        from PIL import Image

        with Image.open(SRC / "images" / "logo.png") as im:
            im = im.convert("RGBA")
            im.save(out_dir / "logo.png")
            im.save(out_dir / "logo.webp", "WEBP", quality=90)
            px = im.load()
            for y in range(im.height):
                for x in range(im.width):
                    r, g, b, a = px[x, y]
                    if a and b > r + 20:  # 蓝色系 → 白色，保留橙色 H
                        px[x, y] = (255, 255, 255, a)
            im.save(out_dir / "logo-white.png")
            im.save(out_dir / "logo-white.webp", "WEBP", quality=90)
        for name in ("wechat_qrcode.jpg",):
            media(f"images/about/{name}", max_w=480)
    return {"color": "/media/brand/logo.webp", "white": "/media/brand/logo-white.webp", "png": "/media/brand/logo.png"}


# ------------------------------------------------------------------ 工具

def item(type_: str, slug: str, title: str, *, summary: str = "", category: str | None = None, sort: int = 0,
         featured: bool = False, published_at: str | None = None, expires_at: str | None = None,
         authorized: bool = True, archived: bool = False, data: dict | None = None) -> dict:
    return {
        "type": type_, "slug": slug, "title": title, "summary": summary, "category": category, "sort": sort,
        "featured": featured, "publishedAt": published_at, "expiresAt": expires_at, "authorized": authorized,
        "archived": archived, "data": data or {},
    }


def blocks_from_items(items: list[dict], img_kw: dict | None = None) -> list[dict]:
    out = []
    for it in items:
        if "img" in it:
            m = media(it["img"]["src"], **(img_kw or {}))
            out.append({"t": "img", **m, "alt": it["img"]["alt"]})
        elif "heading" in it:
            out.append({"t": "h", "text": it["heading"]})
        elif "label" in it:
            out.append({"t": "cap", "label": it["label"], "text": it["text"]})
        else:
            out.append({"t": "p", "text": it["p"]})
    return out


def first_sentence(text: str, limit: int = 80) -> str:
    s = re.split(r"[。；]", text)[0]
    return s if len(s) <= limit else s[:limit] + "…"


# ------------------------------------------------------------------ 新闻

NEWS_FIX = {  # design_document/01 §5 E24—E26：以详情为准；E25 统一为事件日期
    ("company", 12): {"date": "2019-01-07"},
}


def build_news(lines: list[str]) -> list[dict]:
    result = []
    for n in parse_news(lines):
        fixd = NEWS_FIX.get((n.category, n.no), {})
        d = fixd.get("date", n.date)
        blocks = []
        for b in n.blocks:
            if b["t"] == "img":
                m = media(b["src"], max_w=1200)
                blocks.append({"t": "img", **m, "alt": b["alt"]})
            else:
                blocks.append(b)
        paras = [b["text"] for b in blocks if b["t"] == "p"]
        cover = next((b for b in blocks if b["t"] == "img"), None)
        slug = f"{d[:4]}/{n.category}-{n.no:02d}"
        result.append(item(
            "news", slug, n.title, summary=first_sentence(paras[0], 120) if paras else "",
            category=n.category, published_at=d, archived=True,
            sort=-int(d.replace("-", "")),
            data={"source": n.source, "blocks": blocks, "cover": cover and {k: cover[k] for k in ("src", "w", "h", "alt")}},
        ))
    # 2026 年动态：内容完全取自官网“企业简介”原文（design_document/03 §7 N3 需市场部补写更多）
    result.append(item(
        "news", "2026/company-scenario-release",
        "华云智联参与项目入选陕西省首批15个重大创新应用场景", category="company", published_at="2026-07-22",
        sort=-20260722, featured=True,
        summary="陕西延长石油、陕西联通、华云智联以及京、陕高校联合研发的《国家多能源勘探、开采和加工过程安全的具身智能场景验证和应用推广》入选。",
        data={"source": None, "blocks": [
            {"t": "p", "text": "2026年7月22日，陕西省发展改革委在西咸新区秦创原·陕西科技创新产品路演中心举办全省创新应用场景发布大会，发布首批15个重大创新应用场景。"},
            {"t": "p", "text": "陕西延长石油、陕西联通、华云智联以及京、陕高校联合研发的《国家多能源勘探、开采和加工过程安全的具身智能场景验证和应用推广》入选，并获得一致好评，华云智联提供行业具身智能软件和场景验证工作。"},
        ], "cover": None},
    ))
    return result


# ------------------------------------------------------------------ 产品

ENGINE_META = {  # code → (slug, 简称)
    "iDCE": ("idce", "实时数据引擎"),
    "iVEE-ViM/VC/AC": ("ivee", "机器音视觉引擎"),
    "iGIS": ("igis", "地理信息引擎"),
    "iCTE": ("icte", "工业控制引擎"),
    "iGCE": ("igce", "可视图表引擎"),
    "iKGE 2.0": ("ikge", "决策分析引擎"),
    "iMDT 2.0": ("imdt", "数字孪生引擎"),
}

SOFTWARE_META = {  # 匹配关键字 → (slug, code, 名称, 分组)
    "iPLM": ("iplm", "iPLM", "产品全生命周期管理系统", "standard"),
    "iMES": ("imes", "iMES", "生产执行系统", "standard"),
    "iWMS": ("iwms", "iWMS", "仓储管理系统", "standard"),
    "iELMS": ("ielms", "iELMS", "设备全生命周期管理系统", "standard"),
    "iQMS": ("iqms", "iQMS", "质量管理系统", "standard"),
    "iEMS": ("iems", "iEMS", "能源管理系统", "standard"),
    "iAPC&Mimic": ("iapc", "iAPC&Mimic", "先进过程控制和仿真优化系统", "standard"),
    "iESS": ("iess", "iESS", "应急安全管理系统", "standard"),
    "iRIM": ("irim", "iRIM", "无人巡检系统", "standard"),
    "iDCS": ("idcs", "iDCS", "智能分布式工业控制系统", "advanced"),
    "iAPAMS": ("iapams", "iAPAMS", "先进过程报警管理系统", "advanced"),
    "iDTOTS": ("idtots", "iDTOTS", "工业操作仿真培训系统", "advanced"),
    "iDTM L2级": ("idtm", "iDTM L2", "工业数字孪生系统", "advanced"),
    "带式输送机无人值守系统": ("belt-unattended", "", "带式输送机无人值守系统", "advanced"),
    "装置数字孪生": ("device-twin", "", "装置数字孪生", "advanced"),
}

AGENT_META = {
    "生产智能作业智能体": ("production-agent", 1),
    "AI质量识别智能体": ("quality-agent", 2),
    "设备预测性维护智能体": ("maintenance-agent", 3),
    "智能仓储调度智能体": ("warehouse-agent", 4),
    "应急安全预测预警智能体": ("emergency-agent", 5),
    "虚拟数字员工系统": ("digital-employee", 6),
    "生产智能作业系统": ("production-system", 7),
}


def panel_data(p, section_title: str | None = None) -> dict:
    return {
        "en": p.en, "positioning": p.positioning, "overview": p.overview,
        "sectionTitle": section_title or p.section_title,
        "blocks": blocks_from_items(p.items),
        "tables": p.tables,
    }


def build_products(lines: list[str]) -> list[dict]:
    panels = {p.title: p for p in parse_panels(lines)}
    out: list[dict] = []

    # 平台：iMoM 3.2（关于页产品矩阵）+ 工业生产智慧大脑面板
    brain = panels["工业生产智慧大脑"]
    out.append(item("product", "imom", "盘古华云智能工厂平台", category="platform", sort=1, featured=True,
                    summary="基于多类人工智能平台，可根据智能工厂成熟度需求“乐高”式灵活配置算法引擎、工业软件、智能系统、智能体集群和工业增强模型。",
                    data={"code": "iMoM 3.2", "name": "盘古华云智能工厂平台（工业生产智慧大脑）",
                          "facts": [
                              "具备多维约束RAG、Prompt、Skills、Harness参数阈值自适应，以及“零代码”配置多智能体人机交互功能",
                              "可灵活在670B全量模型或1B-32B的轻量模型间迁移",
                          ],
                          "brain": panel_data(brain)}))

    # 旗舰：SpatiGo™ 及四个子产品（定位句取自关于页产品矩阵；能力引用对应智能体原文）
    out.append(item("product", "spatigo", "空间群弈™ SpatiGo™", category="flagship", sort=2, featured=True,
                    summary="工业监管—执行智能体集群：基于“人在回路”的语言模型（LLM）—世界模型（WM）之上的监管—执行多智能体集群（Agentic AI）人工智能应用架构。",
                    data={"code": "SpatiGo™", "name": "空间群弈™（SpatiGo™）工业监管—执行智能体集群",
                          "intro": [
                              "公司核心产品为空间群弈™（SpatiGo™）工业监管智能体和工业执行智能体集群，包含四个子产品。",
                              "聚焦构建基于“人在回路”的语言模型（LLM）—世界模型（WM）之上的监管—执行多智能体集群（Agentic AI）人工智能应用架构，塑造未来工业研发和工厂智能清晰的能力边界和软硬约束，为中国企业提供可靠、高效、安全的工业增强模型规划、智能体集群管控和具身智能可信执行的全新体验。",
                              "2025年发布，得到工信部、发改委、应急部、中国工程院和众多大型企业（集团）的认可和肯定。",
                          ]}))
    subs = [
        ("spatigo-quality", "质量之弈", "Quality", "质量波动找不到原因？", "多模态质量采集、SPC分析和CPK/PPK能力评估", ["quality-agent", "iqms"]),
        ("spatigo-maintenance", "运维之弈", "Maintenance", "设备总在计划外停机？", "工业设备预测性维护FMEA智能体", ["maintenance-agent", "ielms"]),
        ("spatigo-safety", "安全之弈", "Safety", "高危作业还靠人盯？", "多模态安全监测和合规执行智能体", ["emergency-agent", "iess", "iapams"]),
        ("spatigo-embodied", "具身之弈", "Embodied", "巡检进不去、看不全？", "UAV/UGV多类型混合监管—执行智能体集群（旋翼UAV、轮式/四足/人形UGV）", ["irim", "security-integration"]),
    ]
    for i, (slug, name, en, question, tagline, related) in enumerate(subs):
        out.append(item("product", slug, name, category="sub_product", sort=10 + i, featured=True, summary=tagline,
                        data={"parent": "spatigo", "code": f"SpatiGo™ · {en}", "question": question,
                              "tagline": tagline, "related": related, "icon": slug.split("-")[1]}))

    # 模型：iMLLM 1.0 = 三个面板
    sections = []
    for key, slug in (("工业多模态应用大模型", "multimodal"), ("工业增强语言模型LLM交互功能", "llm"),
                      ("多模态信息融合工业智能体群控系统", "swarm")):
        p = panels[key]
        sections.append({"id": slug, "title": p.title, **panel_data(p)})
    out.append(item("product", "imllm", "工业增强大模型 iMLLM", category="model", sort=3, featured=True,
                    summary="深度融合N类多模态生成式人工智能（MGAI）L0级模型，包括千问Qwen、深度求索DeepSeek等通用开源模型，支持实时云化和私有化部署。",
                    data={"code": "iMLLM 1.0", "name": "判别式工业增强大模型", "sections": sections,
                          "facts": ["已构建工艺优化、质量提升、设备管理、安全应急、无人巡检、智能调度和技术培训等模块",
                                    "具备PLC/DCS代码生成与验证、机器人具身与群控能力"]}))

    # 智能体
    for title, (slug, order) in AGENT_META.items():
        p = panels[title]
        out.append(item("product", slug, title, category="agent", sort=100 + order, summary=p.positioning,
                        data={"code": "", "name": title, **panel_data(p)}))

    # 引擎
    eng = panels["智能引擎群"]
    out.append(item("product", "engines", "智能引擎群", category="engine_group", sort=4,
                    summary=eng.positioning, data={"en": eng.en, "overview": eng.overview,
                                                   "image": None}))
    sort = 200
    for it in eng.items:
        if "label" not in it:
            continue
        m = re.search(r"（(i[^）]+)）", it["label"])
        code = m.group(1)
        slug, short = ENGINE_META[code]
        sort += 1
        out.append(item("product", slug, f"{code.split()[0]} {short}", category="engine", sort=sort,
                        summary=first_sentence(it["text"], 90),
                        data={"code": code, "name": short, "fullName": it["label"], "text": it["text"]}))

    # 工业软件
    for group_title in ("工业标准软件", "工业先进软件"):
        p = panels[group_title]
        cur = None
        for it in p.items:
            if "heading" in it:
                key = next((k for k in SOFTWARE_META if k in it["heading"]), None)
                if key:
                    slug, code, name, group = SOFTWARE_META[key]
                    cur = item("product", slug, f"{code} {name}".strip(), category="software",
                               sort=300 + len([o for o in out if o["data"].get("kind") == "software"]),
                               data={"kind": "software", "code": code, "name": name, "fullName": it["heading"],
                                     "group": group, "items": []})
                    out.append(cur)
                    continue
            if cur is not None:
                cur["data"]["items"].append(it)
        out.append(item("product", f"software-{'standard' if group_title == '工业标准软件' else 'advanced'}",
                        group_title, category="software_group", sort=5,
                        summary=p.positioning, data={"en": p.en, "overview": p.overview}))
    for o in out:
        if o["data"].get("kind") == "software":
            o["data"]["blocks"] = blocks_from_items(o["data"].pop("items"))
            first = next((b["text"] for b in o["data"]["blocks"] if b["t"] in ("p", "cap")), "")
            o["summary"] = first_sentence(first, 90)
    # 关于页仅列名称与一句话的两款软件
    for slug, code, name, desc, n in (("iaps", "iAPS", "调度管理系统", "高级计划与排程（APS）智能调度管理", 398),
                                      ("isrm", "iSRM", "供应管理系统", "供应链协同与供应商关系管理", 399)):
        out.append(item("product", slug, f"{code} {name}", category="software", sort=n, summary=desc,
                        data={"kind": "software", "code": code, "name": name, "group": "standard",
                              "blocks": [{"t": "p", "text": desc}], "brief": True}))

    # 安全与集成
    proto, sec = panels["工业协议、数据安全和数据接口"], panels["安全与可靠性"]
    out.append(item("product", "security-integration", "安全与集成", category="security", sort=6,
                    summary=sec.positioning,
                    data={"sections": [{"id": "protocol", "title": proto.title, **panel_data(proto)},
                                       {"id": "reliability", "title": sec.title, **panel_data(sec)}]}))
    return out


# ------------------------------------------------------------------ 资质与研究（来自内容整理文档的结构化表格）

NATIONAL_STANDARDS = [
    "统一架构与5G集成技术规范 第1部分：通用要求", "信息技术 数字孪生 第2部分：数字实体", "信息技术 数字孪生能力成熟度模型",
    "工业仪表智能化等级要求与评价方法", "信息技术装备数字孪生系统通用要求", "智能服务 预测性维护绩效评价方法",
    "智能服务 预测性维护虚拟维护系统技术要求", "智能服务 预测性维护算法测评方法", "智能设备管理 第1部分：概念和定义",
    "智能服务 预测性维护通用要求", "基于蜂窝网络的工业无线通信规范 第4部分：安全要求", "用于工业应用的资产管理壳 第1部分：资产管理壳结构",
    "智能工厂安全一体化 第1部分：一般要求", "智能工厂安全一体化 第2部分：风险评估要求", "智能工厂安全一体化 第3部分：系统协同设计要求",
    "智能工厂安全一体化 第4部分：系统评测要求", "无人值守场站运行及风险防控水平综合评价导则", "人工智能 知识图谱技术框架",
]
INTL_STANDARDS = [
    ("IEEE P2807", "知识图谱架构", "project"),
    ("IEC 63270-1:2025", "工业自动化设备和系统的预测性维护 第1部分：通用要求", "published"),
    ("IEC 63270", "Industrial Automation Equipment and Systems – Predictive Maintenance（立项证明）", "proof"),
    ("P2807.1", "人工智能知识图谱与大规模预训练模型融合 第1部分：参考架构", "project"),
    ("IEC 62682", "过程工业报警系统管理", "published"),
    ("ISO/IEC 25872", "人工智能 知识增强预训练模型 第1部分：框架（第8章编制）", "drafting"),
    ("ISO/IEC 30173:2023", "数字孪生 概念和术语", "published"),
    ("IEC 63270-2", "工业自动化设备和系统的预测性维护 第2部分：算法测评方法", "drafting"),
    ("IEC TR 63283-1", "工业过程测量、控制和自动化 智能制造 第1部分：术语和定义", "published"),
    ("IEC TR 63283-2", "工业过程测量、控制和自动化 智能制造 第2部分：用例", "published"),
    ("IEC TR 63283-3", "工业过程测量、控制和自动化 智能制造 第3部分：网络安全面临的挑战", "published"),
    ("—", "国际标准编制证明", "proof"),
]
DRAFTING_2026 = [
    ("IEEE P3701", "知识增强工业大模型应用系统参考架构"),
    ("IEEE P3701.1", "知识增强工业大模型测评基准"),
    ("ISO/IEC 25872", "人工智能 知识增强预训练模型 第1部分：框架"),
    ("P4123", "领域本体智能构建与集成"),
]
PATENTS = [
    ("一种用于山体滑坡的监测数据处理方法", "ZL 2023 1 0767064.3", "invention", "granted"),
    ("一种基于数据分析的山体滑坡智能形变监管系统", "ZL 2023 1 0669623.7", "invention", "granted"),
    ("一种应用于振动筛的杂物清理装置", "ZL 2023 1 0572352.3", "invention", "granted"),
    ("一种电机故障分析方法", "ZL 2023 1 0684706.3", "invention", "granted"),
    ("一种剃齿加工参数全局优化设计方法", "ZL 2021 1 0231647.5", "invention", "granted"),
    ("安装于矿井巷道的危险区域提醒装置", "ZL 2022 2 1201032.4", "utility", "granted"),
    ("一种多合一的无线文物环境检测器及文物储藏柜", "ZL 2019 2 0628344.5", "utility", "granted"),
    ("一种应对矿井致灾气体的应急逃生路线的生成装置及方法", "202210759602.X", "invention", "pending"),
    ("一种基于GIS的巷道涌水提醒和避灾路线设计的装置", "202210762443.9", "invention", "pending"),
    ("应用于矿井下的危险区域提醒方法、装置及计算机系统", "202210466748.5", "invention", "pending"),
    ("一种数据处理方法及模块、计算平台及工业物联网", "201810756810.8", "invention", "pending"),
    ("用于电子设备的工业智能体交互图形用户界面", "外观设计专利", "design", "granted"),
]
COPYRIGHTS = [
    ("掘进装备预测性维护及远程智能监控系统 V1.0", "2023SR0272753"), ("采煤装备预测性维护及远程智能监控系统 V1.0", "2023SR0272754"),
    ("皮带智能综合保护、预测性维护管理系统 V1.0", "2023SR0272755"), ("产品全生命周期管理系统 V1.0", "2023SR0226323"),
    ("洗选煤设备FMEA故障模式及影响分析系统 V1.0", "2022SR0623453"), ("灾害感知预警预测系统 V1.0", "2022SR0623466"),
    ("安全风险评估管控系统 V1.0", "2022SR0557911"), ("工业带式输送机FMEA故障模式及影响分析系统 V1.0", "2022SR0557927"),
    ("再生水厂水质在线监测数据管理系统 V1.0", "2021SR0644980"), ("再生水厂综合生产执行控制系统 V1.0", "2021SR0644981"),
    ("再生水厂能耗监测管理系统 V1.0", "2021SR0640121"), ("污水厂水质监测管理系统 V1.0", "2021SR0650025"),
    ("污水厂综合生产操作执行系统 V1.0", "2021SR0644985"), ("污水厂综合能源监测管理系统 V1.0", "2021SR0650026"),
    ("自来水厂水处理综合监测系统 V1.0", "2021SR0635335"), ("自来水厂生产管理系统 V1.0", "2021SR0640120"),
    ("自来水厂能源综合管理系统 V1.0", "2021SR0644982"), ("设备全生命周期管理系统 V1.0", "2021SR0617481"),
    ("基于4D-GIS和知识图谱的矿井生产执行系统 V2.0", "2021SR0556274"), ("井下高清视频图像5G传输应用系统 V1.0", "2021SR0414626"),
    ("智慧矿山综合管理APP V1.0", "2023SR0226457"), ("智慧矿山数字孪生应用系统 V1.0", "2022SR1358621"),
    ("多模态信息融合工业智能体群控系统 V1.0", "2026SR0578220"), ("盘古华云工业控制引擎软件 V1.0", "2025SR0987256"),
    ("盘古华云决策分析引擎软件 V1.0", "2025SR0987260"), ("盘古华云可视图表引擎软件 V1.0", "2025SR0978637"),
    ("盘古华云视频处理引擎软件 V1.0", "2025SR0949345"), ("盘古华云机器音视觉引擎软件 V1.0", "2025SR0949376"),
]
PROJECTS = [
    ("national", 2022, "延长石油煤电油化复合场景5G+网业融通建设", "国家发改委新基建", "课题负责人", "closed", 244.59),
    ("national", 2020, "区域一体化工业互联网公共服务平台——面向西部能源化工聚集区工业互联网公共服务平台", "工信部创新发展", "课题负责人", "closed", 32.0),
    ("national", 2022, "面向网络协同制造的云网边端跨域可信接入与服务安全技术", "科技部重点研发", "技术骨干", "closed", 65.0),
    ("national", 2018, "煤炭物联网工业数据接入及边缘计算平台", "工信部物联网集成创新（国家级示范）", "课题负责人", "closed", None),
    ("national", 2019, "IoT边缘端红外-可见光异构图像传感单元及AI处理系统", "工信部物联网关键技术（国家级示范）", "课题负责人", "closed", None),
    ("national", 2021, "面向国家矿山能源多元灾害环境的工业互联网+安全生产解决方案", "工信部工业互联网试点（国家级示范）", "课题负责人", "closed", None),
    ("provincial", 2019, "基于AI及煤炭CPS的采掘装备智能化及其监控技术", "陕西省自然科学基金", "课题负责人", "closed", 50.0),
    ("provincial", 2020, "面向工业互联网边缘端的制造图像智能感知与处理技术研究", "陕西省重点研发计划", "课题负责人", "closed", 20.0),
    ("provincial", 2020, "智能制造中多源设备接入与智能计算物联网技术研究", "陕西省重点研发计划", "课题负责人", "closed", 20.0),
    ("provincial", 2021, "断路/断电/断网等重大突发事件快速恢复应急通信解决方案研究", "陕西省应急管理科技攻关", "课题负责人", "closed", 10.0),
    ("provincial", 2021, "陕煤“5G+智慧矿区”项目", "陕西省5G工业应用试点", "课题负责人", "closed", 60.0),
    ("provincial", 2022, "面向国家矿山能源多元灾害环境的工业互联网+安全生产解决方案", "陕西省工业互联网标杆工厂", "课题负责人", "closed", 40.0),
    ("provincial", 2024, "5G+工业互联网技术及应用", "陕西省重点研发计划", "项目负责人", "ongoing", 80.0),
    ("provincial", 2020, "室内广域聚集人员红外成像温度筛查/识别系统", "西安高新区科技攻关", "项目负责人", "closed", 50.0),
    ("provincial", 2022, "面向国家矿山能源多元灾害环境工业互联网+安全生产解决方案", "陕煤集团科技项目", "项目负责人", "closed", 200.0),
    ("provincial", 2026, "基于增强模型和智能体的中国西部工业企业事故灾害数据治理和智能交互技术攻关", "西安市重点研发计划", "项目负责人", "ongoing", 100.0),
]
AWARDS = [  # (名称, 等级, 年份, 图片)
    ("陕西省科学技术进步奖", "二等奖", "2020", "award_sx_progress_2nd.jpg"),
    ("中央军委科学技术委员会", "三等奖", "2019-2020", "award_central_military_3rd.jpg"),
    ("中国煤炭工业科协技术奖", "二等奖", "2019-2020", "award_coal_sci_2nd.jpg"),
    ("第四届“绽放杯”5G应用征集大赛", "优秀奖", "2021", "award_bloom4_excellent.jpg"),
    ("陕西省科技工作者创新创业大赛", "一等奖", "2021", "award_2021sx_first.jpg"),
    ("第五届“绽放杯”5G应用征集大赛", "一等奖", "2022", "award_bloom5_gold.jpg"),
    ("第二届工业数字孪生大赛", "三等奖", "2022", "award_dt_2nd_3rd.jpg"),
    ("第三届工业数字孪生大赛", "三等奖", "2023", "award_dt_3rd_3rd.jpg"),
    ("陕西省科技工作者创新创业大赛", "二等奖", "2024", "award_2024sx_2nd.jpg"),
    ("陕西省企业“三新三小”创新竞赛项目", "一等奖", "2024", "award_2024sx3n_first.jpg"),
    ("“沣东杯”陕西省科技工作者创新创业大赛", "银奖", "2019", "award_2019_fengdong_silver.jpg"),
    ("第三届琶洲算法大赛", "季军", "2025", "award_pazhou_third.jpg"),
    ("数字中国创新大赛·人工智能赛道", "三等奖", "2025", "award_digital_china_3rd.jpg"),
    ("第四届全国数字孪生大赛", "三等奖", "2025", "award_dt_4th_3rd.jpg"),
]
CERTIFICATES = [  # (名称, 编号, 发证, 到期, 图片, 说明)
    ("高新技术企业证书", "GR202361006777", "2023-12-12", "2026-12-11", "cert_hightech.jpg", "有效期三年"),
    ("ISO 9001 质量管理体系认证", "GB/T19001-2016/ISO9001:2015", "2024-01-16", "2027-01-15", "cert_iso9001.jpg", "认证范围：计算机软件开发"),
    ("技术贸易资格证", "181262291", "2018-08-01", None, "cert_tech_trade.jpg", "2018年8月签发"),
    ("注册商标 Pangoo Cloud（第9类）", "第32276354号", "2019-06-07", "2029-06-06", "cert_trademark_01.jpg", ""),
    ("注册商标 Pangoo Cloud（第42类）", "第32277238号", "2019-04-07", "2029-04-06", "cert_trademark_02.jpg", ""),
    ("注册商标 盘古华云（第9类）", "第32282717号", "2019-04-07", "2029-04-06", "cert_trademark_03.jpg", ""),
]
PARTNERS = {
    "university": ["北京大学", "南开大学", "西安交通大学", "长安大学", "北京航空航天大学", "西北工业大学", "西安理工大学", "中国民航大学",
                   "西安建筑科技大学", "西安财经学院"],
    "industry": ["中国石油", "中国海油", "中国电子", "中国神华", "中国电信", "中国移动", "中国联通", "中国航天科工集团", "陕西煤业化工集团",
                 "友发钢管集团", "西安水务集团"],
    "research": ["国家制造强国建设战略咨询委员会", "中国信息通信研究院", "中国工程院", "中国信息安全测评中心", "中国自动化学会", "CSTC",
                 "中国机械工程学会", "工信部电子第一研究所", "中国科学院", "工业大数据应用技术国家工程实验室", "国家信息技术安全研究中心",
                 "陕西工业互联网研究院", "陕西工业互联网联合实验室"],
    "integrator": ["Siemens", "Honeywell", "Emerson", "Endress+Hauser", "Yokogawa", "Mitsubishi Electric", "Schneider Electric",
                   "OMRON", "HACH"],
}


def build_research() -> dict[str, list[dict]]:
    honor = "images/about/honor"
    std_files = sorted(p.name for p in (SRC / honor / "std").iterdir())
    lines = load_lines(TXT)
    ocr_codes = _standard_codes_from_ocr(lines)
    standards = []
    for i, name in enumerate(NATIONAL_STANDARDS, 1):
        imgs = [media(f"{honor}/std/{f}", max_w=1400, watermark=True, thumb=(360, 480))
                for f in std_files if f.startswith(f"std_gb_{i:02d}_")]
        code = ocr_codes.get(i)
        standards.append(item("standard", f"gb-{i:02d}", name, category="national", sort=i,
                              data={"code": code or "制定中", "codeSource": "ocr" if code else None,
                                    "status": "published" if code else "drafting", "role": "参与制定",
                                    "images": imgs}))
    for i, (code, name, status) in enumerate(INTL_STANDARDS, 1):
        imgs = [media(f"{honor}/std/{f}", max_w=1400, watermark=True, thumb=(360, 480))
                for f in std_files if f.startswith(f"std_iec_{i:02d}_")]
        standards.append(item("standard", f"intl-{i:02d}", name, category="international", sort=100 + i,
                              data={"code": code, "status": status, "role": "参与制定", "images": imgs}))
    for i, (code, name) in enumerate(DRAFTING_2026, 1):
        standards.append(item("standard", f"drafting-2026-{i}", name, category="drafting", sort=200 + i, featured=True,
                              data={"code": code, "status": "drafting", "role": "编写（2026年）", "images": []}))

    patents = [item("patent", f"patent-{i:02d}", t, category=kind, sort=i,
                    data={"number": num, "kind": kind, "state": state,
                          "image": media(f"{honor}/patent/patent_{i:02d}.jpg", max_w=1400, watermark=True, thumb=(360, 480))})
               for i, (t, num, kind, state) in enumerate(PATENTS, 1)]
    copyrights = [item("copyright", reg.lower(), t, category=reg[:4], sort=i,
                       data={"regNo": reg, "year": int(reg[:4]),
                             "image": media(f"{honor}/soft/soft_{i:02d}.jpg", max_w=1400, watermark=True, thumb=(360, 480))})
                  for i, (t, reg) in enumerate(COPYRIGHTS, 1)]
    projects = [item("project", f"project-{i:02d}", t, category=level, sort=i,
                     data={"level": level, "year": y, "source": src, "role": role, "status": st, "amountWan": amt})
                for i, (level, y, t, src, role, st, amt) in enumerate(PROJECTS, 1)]
    awards = [item("award", f"award-{i:02d}", t, category=grade, sort=i,
                   data={"grade": grade, "year": y,
                         "image": media(f"{honor}/award/{img}", max_w=1400, watermark=True, thumb=(360, 480))})
              for i, (t, grade, y, img) in enumerate(AWARDS, 1)]
    certs = [item("certificate", f"cert-{i:02d}", t, sort=i, published_at=issued, expires_at=exp,
                  data={"number": num, "note": note,
                        "image": media(f"{honor}/cert/{img}", max_w=1400, watermark=True, thumb=(360, 480))})
             for i, (t, num, issued, exp, img, note) in enumerate(CERTIFICATES, 1)]
    partners = []
    n = 0
    for cat, names in PARTNERS.items():
        for name in names:
            n += 1
            partners.append(item("partner", f"partner-{n:02d}", name, category=cat, sort=n,
                                 data={"logo": media(f"images/about/introduce/Logo_{n:02d}.jpg", max_w=686)}))
    labs = build_labs(lines)
    return {"standard": standards, "patent": patents, "copyright": copyrights, "project": projects,
            "award": awards, "certificate": certs, "partner": partners, "lab": labs}


def _standard_codes_from_ocr(lines: list[str]) -> dict[int, str]:
    """从国家标准扫描件 OCR 中提取已发布标准号（仅取格式完整的 GB/T 编号；正式上线前需对照原图）。"""
    s = next(i for i, l in enumerate(lines) if l.strip() == "NATIONAL STANDARDS")
    e = next(i for i, l in enumerate(lines) if l.strip() == "INTERNATIONAL STANDARDS")
    result: dict[int, str] = {}
    cur = None
    for l in lines[s:e]:
        m = re.match(r"^(\d{2})(\S.*)$", l.strip())
        if m and len(l) < 60:
            cur = int(m.group(1))
            continue
        if cur and cur not in result:
            c = re.search(r"GB/T\s?(\d{4,5}(?:\.\d+)?)\s?[—\-–]\s?(20\d{2})", l)
            if c and "发布" in l:
                result[cur] = f"GB/T {c.group(1)}—{c.group(2)}"
    return result


def build_labs(lines: list[str]) -> list[dict]:
    toks = tokenize(lines[next(i for i, l in enumerate(lines) if l.strip() == "先进技术实验室完整文字与图像") + 1:
                          next(i for i, l in enumerate(lines) if l.strip() == "服务中心完整文字与图像")])
    labs, cur = [], None
    images = ["images/lab/content_01_pic.jpg", "images/lab/content_02.jpg", "images/lab/content_03.jpg"]
    for t in toks:
        if t.kind == "heading" and ("实验室" in t.text or "中心" in t.text):
            cur = {"title": t.text, "en": "", "paras": []}
            labs.append(cur)
        elif cur and t.kind == "caps":
            cur["en"] = t.text
        elif cur and t.kind == "para":
            cur["paras"].append(t.text)
    out = []
    for i, lab in enumerate(labs):
        body = "".join(lab["paras"])
        out.append(item("lab", f"lab-{i + 1}", lab["title"], sort=i + 1, summary=first_sentence(body, 100),
                        data={"en": lab["en"], "body": body, "image": media(images[i], max_w=1600)}))
    return out


# ------------------------------------------------------------------ 解决方案、案例、页面

SOLUTIONS = [
    ("mining-power", "矿山与电力", "矿山能源多元灾害环境下的安全生产、装备预测性维护与无人值守。",
     ["华云智联承担了“煤炭物联网工业数据接入及边缘计算平台”“面向国家矿山能源多元灾害环境的工业互联网+安全生产解决方案”等国家级与省级项目。",
      "形成掘进、采煤装备预测性维护及远程智能监控，皮带智能综合保护，灾害感知预警预测，智慧矿山数字孪生等系统。"],
     ["maintenance-agent", "emergency-agent", "belt-unattended", "irim", "iess", "spatigo-maintenance"],
     ["设备健康与预测性维护", "安全应急", "无人巡检与具身作业"]),
    ("petrochemical", "石油化工", "油气田特种作业监管、化工安全应急与装置数字孪生。",
     ["工业增强语言模型支撑长庆油田特种作业全流程智能化管控；参与的具身智能场景验证项目入选陕西省首批15个重大创新应用场景。",
      "提供化工安全应急与设备健康专有知识库构建、先进过程报警管理与装置数字孪生。"],
     ["imllm", "spatigo-safety", "spatigo-embodied", "iapams", "idcs", "device-twin"],
     ["安全应急", "工艺优化", "无人巡检与具身作业"]),
    ("aerospace-equipment", "航空航天与装备制造", "研制生产过程的质量识别、仓储调度与全生命周期管理。",
     ["智能仓储调度智能体支持原套（整套产品）装配出入库、设计变更与批次升级管理，以及宇航元器件、火箭燃料等物资的独立成本核算。",
      "产品全生命周期管理与生产执行系统覆盖设计、工艺、生产到质量追溯。"],
     ["warehouse-agent", "quality-agent", "iplm", "imes", "spatigo-quality"],
     ["质量提升", "生产经营管理"]),
    ("steel-metallurgy", "钢铁冶金", "连续生产装备的健康管理、能源管理与先进过程控制。",
     ["设备预测性维护智能体以非侵入方式采集三相电流与振动信号，覆盖电机、泵、风机等关键设备。",
      "能源管理与先进过程控制系统面向非线性、大滞后、强干扰和变量耦合的工艺单元。"],
     ["maintenance-agent", "iems", "iapc", "ielms", "spatigo-maintenance"],
     ["设备健康与预测性维护", "工艺优化"]),
    ("tobacco-food", "烟草与食药制造", "制程质量检测、生产标准化与办公智能化。",
     ["AI质量识别智能体基于非接触式图像/视频检测，识别表面斑点、霉变、颜色差异、结块等缺陷。",
      "虚拟数字员工系统提供烟草流程标准化查询与典型工艺异常问题的参考方案。"],
     ["quality-agent", "digital-employee", "production-agent", "iqms", "spatigo-quality"],
     ["质量提升", "生产经营管理"]),
    ("water-municipal", "水务与市政", "水厂生产执行、水质监测与能耗管理。",
     ["已形成再生水厂、污水厂、自来水厂的水质监测、生产执行与能源管理系列软件。"],
     ["imes", "iems", "ielms", "iess"],
     ["生产经营管理", "设备健康与预测性维护"]),
]

SCENARIOS = ["质量提升", "设备健康与预测性维护", "安全应急", "工艺优化", "生产经营管理", "无人巡检与具身作业"]


def build_solutions() -> list[dict]:
    return [item("solution", slug, name, summary=summary, sort=i, featured=True,
                 data={"paras": paras, "products": prods, "scenarios": scen})
            for i, (slug, name, summary, paras, prods, scen) in enumerate(SOLUTIONS, 1)]


def build_cases(lines: list[str]) -> list[dict]:
    cases = [
        item("case", "embodied-energy-safety", "多能源勘探、开采和加工过程安全的具身智能场景验证", category="petrochemical",
             sort=1, featured=True, published_at="2026-07-22",
             summary="陕西延长石油、陕西联通、华云智联以及京、陕高校联合研发，入选陕西省首批15个重大创新应用场景。",
             data={"customer": "陕西延长石油、陕西联通及京、陕高校联合项目", "scenario": "具身智能 · 安全生产",
                   "challenge": "国家多能源勘探、开采和加工过程中的安全生产需要可验证、可推广的具身智能应用场景。",
                   "solution": "华云智联提供行业具身智能软件和场景验证工作，依托空间群弈™具身之弈的UAV/UGV混合监管—执行能力。",
                   "timeline": [{"date": "2026-07-22", "text": "陕西省发展改革委全省创新应用场景发布大会发布首批15个重大创新应用场景，本项目入选。"}],
                   "results": [], "products": ["spatigo-embodied", "spatigo-safety", "imllm"],
                   "image": media("images/product/v2/swarm.jpg", max_w=1600)}),
        item("case", "oilfield-special-operations", "油田特种作业全流程智能化管控", category="petrochemical", sort=2, featured=True,
             summary="工业增强语言模型与智能体群控系统支撑长庆油田特种作业事前、事中、事后全流程智能化管控。",
             data={"customer": "长庆油田（据官网产品介绍）", "scenario": "特种作业监管",
                   "challenge": "特种作业环节多、风险高，依赖人工旁站监护，作业准备、违章识别与结果核查难以闭环。",
                   "solution": "工业增强LLM理解油田作业术语、违章描述与场景指令，实现“目标物—场景—行为”一体化分析；群控系统打通集团特种作业管理、运营管理与风险隐患识别系统，形成事前作业准备指导、事中违章识别与同步报警、事后作业结果汇总的安全审验闭环，异常时人在环上核查。",
                   "timeline": [], "results": [], "products": ["imllm", "spatigo-safety"],
                   "image": media("images/product/v2/llm.jpg", max_w=1600)}),
    ]
    legacy = [
        ("huda-aisheng", "湖大艾盛注塑件云制造方案", "助力云制造落地湖南汽车内饰注塑件行业。",
         "帮助湖大艾盛达成企业经营目标：产线稼动率提高3%；产品合格率提高5%；用工人数减少10人；能源节约（换算标准煤）3万吨/年；尝试实现支持NB-IoT协议传感器（温度、物位）的组网及接入；帮助培养工业云管理及操作人员；归纳总结长株潭地区汽车内饰注塑件生产企业通过云制造提高竞争力的有效路径。",
         ["photo_01.jpg", "photo_02.jpg"]),
        ("great-wall-finance", "长城金融设备云运维方案", "设备集中管理、质量管理分析与微信工单监控。",
         "长沙工业云平台与长城金融合作，设备云运维系统采用移动互联、工业4.0、云服务、大数据分析等技术实现设备集中管理、质量管理分析、微信工单大数据监控，提高运维服务效率、降低运维成本。",
         ["photo_03.jpg", "photo_04.jpg"]),
        ("clp-software-park", "中电软件园云园区方案", "智慧园区基础设施与信息化运营。",
         "中电软件园智慧园区解决方案运用长沙工业云平台，通过智能化的园区基础设施、信息化的运营管理工具，专业化的业务流程设计提升了园区服务品质，提高了运作效率，辅助了科学策略，控制了前期建设成本、建设后期运维成本以及后期的增值效益。",
         ["photo_05.jpg", "photo_06.jpg"]),
    ]
    for i, (slug, title, summary, body, imgs) in enumerate(legacy, 1):
        cases.append(item("case", slug, title, category="legacy", sort=100 + i, archived=True, summary=summary,
                          data={"customer": title.split("注塑")[0].replace("设备云运维方案", "").replace("云园区方案", ""),
                                "scenario": "工业云", "challenge": "", "solution": body.replace("NB-loT", "NB-IoT"),
                                "results": [], "products": [], "legacy": True,
                                "images": [media(f"images/about/display/{f}", max_w=1200) for f in imgs],
                                "image": media(f"images/about/display/{imgs[0]}", max_w=1200)}))
    return cases


def build_jobs(lines: list[str]) -> list[dict]:
    s = next(i for i, l in enumerate(lines) if l.strip() == "RECRUITMENT POSITION" and i > 4000)
    e = next(i for i, l in enumerate(lines) if i > s and l.strip().startswith("A226"))
    jobs, cur, part = [], None, None
    for raw in lines[s + 1:e]:
        l = raw.strip()
        if not l or l.startswith(("A2", "原图来源", "图片文字识别")) or "待核" in l or l.startswith("Hello"):
            continue
        if l in ("工程项目经理", "Web前端工程师", "Java后端工程师"):
            cur = {"title": l, "duties": [], "reqs": []}
            jobs.append(cur)
            continue
        if cur is None:
            continue
        if l.startswith("一、岗位职责"):
            part = "duties"; continue
        if l.startswith("二、任职要求"):
            part = "reqs"; continue
        if part and re.match(r"^(\d+、|（\d+）)", l):
            cur[part].append(fix(re.sub(r"^\d+、", "", l)))
        elif part and cur[part]:
            cur[part][-1] += fix(l)
    return [item("job", f"job-{i}", j["title"], sort=i, data={"duties": j["duties"], "reqs": j["reqs"]})
            for i, j in enumerate(jobs, 1)]


def build_pages(lines: list[str], logo: dict) -> list[dict]:
    about_photos = [
        ("photo_01.jpg", "美国华盛顿大学工业互联网交流"), ("photo_02.jpg", "西安市工业互联网及云平台汇报"),
        ("photo_03.jpg", "CEC全国NB-IoT示范项目汇报"), ("photo_04.jpg", "带锯制造全球领军企业调研"),
        ("photo_05.png", "华云智联MES产品发布"), ("photo_06.png", "陕西省通信管理局局长莅临华云智联展台"),
        ("photo_07.png", "主持中国西部工业互联网发展论坛"), ("photo_08.png", "华云智联展台交流"),
    ]
    common = {
        "company": "西安华云智联信息科技有限公司",
        "companyEn": "Xi'an H.Y Wisdom Information Technology Co., Ltd.",
        "phone": "029-88810623", "email": "yanggan@hywisdom.cn", "postcode": "710075",
        "address": "西安市雁塔区科技路48号创业广场C座2楼C201（WEI SPACE）",
        "icp": "陕ICP备2026024028号-1", "website": "www.huayunzhilian.cn",
        "logo": logo, "wechat": media("images/about/wechat_qrcode.jpg", max_w=480),
        "foundedYear": 2018,
    }
    home = {
        "announcement": {"text": "入选陕西省首批15个重大创新应用场景：多能源勘探开采加工安全的具身智能场景验证",
                         "href": "/news/2026/company-scenario-release"},
        "hero": {
            "eyebrow": "工业人工智能 · 监管—执行智能体集群",
            "title": "让智能释放产业效能",
            "subtitle": "空间群弈™ SpatiGo™ 把工业增强大模型、7组智能引擎和工业软件连成一个“人在回路”的监管—执行智能体集群，在油田、矿山、化工和产线现场闭环运行。",
            "primary": {"label": "预约现场演示", "href": "/demo"},
            "secondary": {"label": "了解 SpatiGo™", "href": "/products/spatigo"},
        },
        "stats": [
            {"value": "100+", "label": "工业（集团）落地应用", "note": 1},
            {"value": "30", "label": "国家 / 国际标准工作条目", "note": 2},
            {"value": ">95%", "label": "靶向增强后推荐准确度", "note": 3},
            {"value": "1.3B", "label": "最低可部署模型规模", "note": 4},
        ],
        "footnotes": [
            "据公司统计，截至2026年7月，在矿山、石油、化工、半导体、烟草等行业的100余家工业（集团）落地应用。",
            "国家标准目录18条、国际标准目录12条，含立项、编制中项目及编制证明，详见“标准与研究”。",
            "靶向增强后数据推荐准确度，来源：公司产品资料（测试数据集与场景待公布）。",
            "盘古华云智能工厂平台可在低至1.3B模型上部署，来源：公司产品资料。",
        ],
        "customers": ["中国航天科技", "中国航空工业", "中国石油", "中国保利", "中国烟草", "中国联通", "陕西煤业", "陕西延长石油",
                      "德国巴斯夫", "沙特阿美"],
        "committees": [
            {"code": "SAC/TC124", "name": "全国工业过程测量控制和自动化标准化技术委员会"},
            {"code": "SAC/TC28", "name": "全国信息技术标准化技术委员会（SC41、SC42）"},
            {"code": "SAC/TC88", "name": "全国矿山机械标准化技术委员会"},
            {"code": "IEC/TC65", "name": "国际电工委员会工业测量、控制和自动化技术委员会"},
        ],
        "arch": [
            {"key": "n", "title": "N 个智能体", "desc": "空间群弈™监管—执行智能体集群与7类工业智能体应用，人在回路。", "href": "/products/spatigo"},
            {"key": "2", "title": "2 类约束", "desc": "物理—化学混合算法模型预测（MPC）硬约束，成本—效率混合优化软约束。", "href": "/products"},
            {"key": "10", "title": "10 组工业软件", "desc": "iPLM、iMES、iQMS、iELMS、iWMS、iAPS、iEMS、iSRM、iESS、iRIM。", "href": "/products/software"},
            {"key": "7", "title": "7 组智能引擎", "desc": "实时数据、机器音视觉、地理信息、工业控制、可视图表、决策分析、数字孪生。", "href": "/products/engines"},
            {"key": "base", "title": "跨媒体数据底座", "desc": "数据、文本、视频、音频统一标准化基座，兼容 IEC 61131-3 FBD / SFC / ST 控制编译器。", "href": "/products/imllm"},
        ],
        "deploy": [
            {"title": "私有化部署", "text": "支持主流大模型私有化部署，数据不出厂网；满足等保2.0二级安全规范要求。"},
            {"title": "大小模型迁移", "text": "可在670B全量模型与1B—32B轻量模型间迁移，低至1.3B模型可部署。"},
            {"title": "传输与存储安全", "text": "TLS 1.3 + 国密SM4；RBAC分级权限；操作日志留存≥180天。"},
        ],
        "evidence": ["embodied-energy-safety", "oilfield-special-operations"],
        "cta": {"title": "带一个现场问题来，我们用智能体给出答案。", "primary": {"label": "预约现场演示", "href": "/demo"}},
    }
    intro = [
        "西安华云智联信息科技有限公司成立于2018年，是新一代工业人工智能科技公司，秉承“让智能释放产业效能”的信念，致力于工业感知控制、工业软件和人工智能深度融合，服务矿山电力、石油化工、航空航天、钢铁冶金、电子信息、装备制造、食药制造和烟草生产等行业“提质增效、节能降耗”的服务型制造转型。",
        "公司是SAC/TC124、SAC/TC28（SC41、SC42）、SAC/TC88和IEC/TC65等国际和国家标委会委员单位，参与数字孪生、工业软件、人工智能、工业通信、智能工厂、工业仪表控制等国家与国际标准工作；2026年参与编写IEEE P3701、IEEE P3701.1、ISO/IEC 25872与P4123。",
        "公司聚焦“人在回路”的多模态语言模型—物理世界模型之上的监管—执行多智能体集群（Agentic AI）应用架构，2025年发布空间群弈™（SpatiGo™）工业监管—执行智能体集群。截至2026年7月，在矿山、石油、化工、半导体、烟草行业的100余家工业（集团）的工艺优化、质量提升、设备健康管理和预测维护、FMEA、安全应急和产品研发等判别式大模型应用场景落地。",
    ]
    milestones = [
        ("2018", "公司成立，发布盘古（Pangoo）工业互联网平台理念"),
        ("2019", "参与预测性维护国家标准工作组和国际标准国内对口工作组工作，提出基于图像和声音处理的预测性维护方法"),
        ("2020", "联合申请项目获批工信部“关键技术与平台创新类”示范项目；获陕西省科学技术进步奖二等奖"),
        ("2022", "承担延长石油煤电油化复合场景5G+网业融通建设（国家发改委新基建）"),
        ("2023", "获高新技术企业认定"),
        ("2025", "发布空间群弈™（SpatiGo™）工业监管—执行智能体集群；获数字中国创新大赛·人工智能赛道三等奖"),
        ("2026", "参与编写IEEE P3701、IEEE P3701.1、ISO/IEC 25872、P4123；参与项目入选陕西省首批15个重大创新应用场景"),
    ]
    about = {
        "mission": "让智能释放产业效能", "missionEn": "Intelligence that unlocks industrial performance",
        "intro": intro, "values": [
            {"title": "可靠", "text": "人在回路的监管—执行架构，关键动作由人在环上确认。"},
            {"title": "标准", "text": "以国家与国际标准工作沉淀工程方法，产品对标标准落地。"},
            {"title": "可信", "text": "私有化部署、国密加密与全过程审计，数据不出厂网。"},
        ],
        "milestones": [{"year": y, "text": t} for y, t in milestones],
        "photos": [dict(media(f"images/about/introduce/{f}", max_w=1200), alt=a) for f, a in about_photos],
    }
    support = {
        "hotline": "029-88810623",
        "intro": ["我们设立了7×24H服务中心，任何时候只要您需要，技术服务团队都将快速做出反应，为您的生产业务护航。"],
        "steps": [
            {"title": "分析咨询", "en": "Analytical Consultation", "text": "调研现场与业务目标，梳理数据与系统现状。"},
            {"title": "方案论证", "en": "Demonstration Program", "text": "给出智能体、引擎与软件组合方案并论证可行性。"},
            {"title": "项目实施", "en": "Project Implementation", "text": "部署、集成与联调，接入PLC/DCS/SCADA等系统。"},
            {"title": "交付验证", "en": "Delivery Acceptance", "text": "按约定指标验证效果并完成交付。"},
            {"title": "运营优化", "en": "Operational Optimization", "text": "持续运营、模型迭代与效果优化。"},
        ],
        "services": [
            {"title": "顾问咨询", "en": "Consultancy", "items": ["精益质量管理", "标准合规", "流程优化", "业务改善"]},
            {"title": "软件开发", "en": "Software Development", "items": ["数据分析工具", "雾计算与边缘计算", "人工智能工具", "预测性维护工具"]},
            {"title": "产品设计", "en": "Product Design", "items": ["终端感知", "信息采集", "物联网 NB-IoT 接入", "移动与固定接入"]},
            {"title": "系统集成", "en": "System Integration", "items": ["数字化车间", "柔性供应链", "智能化工厂", "智慧化平台"]},
        ],
    }
    privacy = {"blocks": [
        {"t": "h", "text": "我们收集的信息"},
        {"t": "p", "text": "当您通过本网站提交“预约现场演示”或联系表单时，我们会收集您主动填写的姓名、公司、职位、手机号或邮箱及需求描述，仅用于与您联系并提供产品与服务信息。"},
        {"t": "h", "text": "信息的保护"},
        {"t": "p", "text": "手机号、邮箱等个人信息在存储时加密保护，后台默认脱敏显示；数据存储在中华人民共和国境内。"},
        {"t": "h", "text": "保存期限与您的权利"},
        {"t": "p", "text": "我们仅在实现上述目的所需的期限内保存您的个人信息。您可以通过电子邮件 yanggan@hywisdom.cn 或电话 029-88810623 申请查询、更正或删除您的个人信息。"},
        {"t": "p", "text": "（本文为网站开发版本的隐私政策草案，正式上线前须经法务审定。）"},
    ]}
    return [
        item("page", "common", "全站信息", data=common),
        item("page", "home", "首页", data=home),
        item("page", "about", "公司介绍", data=about),
        item("page", "support", "服务支持", data=support),
        item("page", "privacy", "隐私政策", data=privacy),
    ]


# ------------------------------------------------------------------ 主流程

def main() -> None:
    lines = load_lines(TXT)
    SEED.mkdir(parents=True, exist_ok=True)
    logo = logos()
    groups: dict[str, list[dict]] = {
        "page": build_pages(lines, logo),
        "product": build_products(lines),
        "solution": build_solutions(),
        "case": build_cases(lines),
        "news": build_news(lines),
        "job": build_jobs(lines),
    }
    groups.update(build_research())
    total = 0
    for name, items in groups.items():
        path = SEED / f"{name}.json"
        path.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        total += len(items)
        print(f"{name:12s} {len(items):4d} -> {path.relative_to(ROOT)}")
    meta = {"generatedAt": date.today().isoformat(), "items": total, "scenarios": SCENARIOS,
            "source": "素材库/官网补录文字.txt + design_document/03"}
    (SEED / "_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print("total", total, "media", len(_media_cache))


if __name__ == "__main__":
    main()
