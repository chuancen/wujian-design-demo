#!/usr/bin/env python3
from __future__ import annotations

import html
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screenshots-v3"
SVG_OUT = ROOT / "screenshot-sources-svg-v3"
W, H = 1440, 1440


PAGES = [
    ("P01", "登录/角色入口", "医院端、学校端、医护端、家长端入口", "portal"),
    ("P02", "工作台首页", "今日任务、异常待复核、离线同步状态", "dashboard"),
    ("P03", "组织与角色管理", "组织树、角色列表、数据范围、权限矩阵", "permissions"),
    ("P04", "用户权限与审计", "操作日志、敏感操作、导出记录、审计筛选", "audit"),
    ("P05", "学校班级学生管理", "学校/年级/班级树、学生表、导入导出按钮", "students"),
    ("P06", "数据导入结果", "成功/失败统计、错误行、错误原因、重试", "import"),
    ("P07", "儿童健康档案列表", "风险标签、最近体检、档案状态", "archive_list"),
    ("P08", "儿童档案详情", "五健指标、趋势图、复查记录", "archive_detail"),
    ("P09", "档案合并弹窗", "重复字段对比、合并策略、冲突提示", "merge"),
    ("P10", "体检任务列表", "任务进度、覆盖人数、异常数、同步状态", "tasks"),
    ("P11", "任务创建向导", "步骤条、项目选择、科室人员、通知", "wizard"),
    ("P12", "项目与规则配置", "年龄段、性别、指标阈值、建议文案", "rules"),
    ("P13", "二维码/条码打印", "打印预览、绑定状态、批量生成", "qr"),
    ("P14", "医护采集工作台", "待检队列、采集进度、设备状态", "collection"),
    ("P15", "单人采集录入", "分项录入、范围校验、漏项提示", "entry"),
    ("P16", "离线同步中心", "本地暂存、同步队列、冲突记录", "sync"),
    ("P17", "设备接入状态", "身高体重仪、视力、血压、肺活量设备", "devices"),
    ("P18", "异常复核", "异常字段、规则说明、复核意见", "review"),
    ("P19", "纸质补登", "按学生/项目快速补登、补登来源", "paper"),
    ("P20", "随访工作台", "联系状态、通知渠道、随访结果", "followup"),
    ("P21", "五健总览", "营养、视力、脊柱、口腔、心理五类卡片", "five"),
    ("P22", "五健专题详情", "异常分布、趋势、建议、复查计划", "specialty"),
    ("P23", "家长端信息确认", "基础信息、既往史、过敏史、同意确认", "parent_form"),
    ("P24", "家长端报告", "本次报告、历次趋势、异常项、建议", "parent_report"),
    ("P25", "家长端健康教育", "推荐文章、异常关联、阅读状态", "education"),
    ("P26", "接口配置", "接口系统列表、认证方式、启用状态", "interfaces"),
    ("P27", "数据交换记录", "批次记录、匹配率、失败原因", "exchange"),
    ("P28", "转诊协同", "建议科室、预约状态、回传结果", "referral"),
    ("P29", "区域统计驾驶舱", "覆盖率、完成率、异常率、复查率", "analytics"),
    ("P30", "现场调度大屏", "采集点位、漏项预警、设备在线", "dispatch"),
    ("P31", "汇报只读模式", "脱敏数据、无后台入口、只读标识", "readonly"),
    ("P32", "系统部署与备份", "部署环境、备份计划、恢复记录", "backup"),
]


THEMES = {
    "A": {
        "dir": "方案A-Winform内网桌面系统",
        "brand": "儿童青少年五健体检管理系统",
        "mode": "Winform 内网桌面版",
        "bg": "#cfd6df",
        "panel": "#f4f4f4",
        "soft": "#e8edf4",
        "text": "#1f2937",
        "muted": "#536170",
        "primary": "#2b579a",
        "accent": "#0078d7",
        "warn": "#d97706",
        "bad": "#d13f3f",
        "line": "#98a4b3",
        "dark": "#2f3b4a",
    },
    "B": {
        "dir": "方案B-Java企业管理平台",
        "brand": "五健体检综合管理平台",
        "mode": "Java/Spring 企业管理版",
        "bg": "#f3f6fb",
        "panel": "#ffffff",
        "soft": "#eef5ff",
        "text": "#1f2937",
        "muted": "#6b7280",
        "primary": "#1677ff",
        "accent": "#13a8a8",
        "warn": "#f59e0b",
        "bad": "#ef4444",
        "line": "#d8e1ee",
        "dark": "#1f2a44",
    },
    "C": {
        "dir": "方案C-儿童健康服务品牌产品",
        "brand": "小鹿五健健康服务",
        "mode": "家长友好 / 学校协同",
        "bg": "#fbf7ef",
        "panel": "#ffffff",
        "soft": "#effaf4",
        "text": "#283329",
        "muted": "#758072",
        "primary": "#21a67a",
        "accent": "#ff8d66",
        "warn": "#eaa21a",
        "bad": "#e66262",
        "line": "#dfe8d9",
        "dark": "#22312b",
    },
    "D": {
        "dir": "方案D-临床采集效率工具",
        "brand": "ClinicFlow 五健采集台",
        "mode": "现场采集 / 离线容错",
        "bg": "#f5f5f2",
        "panel": "#ffffff",
        "soft": "#f0f1ed",
        "text": "#191b1f",
        "muted": "#6b6e75",
        "primary": "#22252b",
        "accent": "#65e854",
        "warn": "#ff9d2e",
        "bad": "#f04f64",
        "line": "#d6d8d2",
        "dark": "#191b1f",
    },
}


def esc(v: str) -> str:
    return html.escape(str(v), quote=True)


def wlen(value: str) -> float:
    return sum(1.0 if ord(ch) > 127 else 0.55 for ch in value)


def wrap(value: str, max_units: float) -> list[str]:
    lines, cur = [], ""
    for ch in value:
        if cur and wlen(cur + ch) > max_units:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines[:5]


class SVG:
    def __init__(self, theme):
        self.t = theme
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
            "<defs><style>text{font-family:'Hiragino Sans GB','STHeiti','PingFang SC','Helvetica Neue',Arial,sans-serif}.mono{font-family:'SF Mono','Menlo',monospace}</style></defs>",
            f'<rect width="{W}" height="{H}" fill="{theme["bg"]}"/>',
        ]

    def rect(self, x, y, w, h, fill=None, stroke=None, rx=8, sw=1, opacity=1):
        stroke_attr = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or self.t["panel"]}" opacity="{opacity}"{stroke_attr}/>')

    def text(self, x, y, value, size=16, fill=None, weight=500, anchor="start", cls="", opacity=1):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill or self.t["text"]}" font-weight="{weight}" text-anchor="{anchor}" class="{cls}" opacity="{opacity}">{esc(value)}</text>')

    def line(self, x1, y1, x2, y2, color=None, sw=1, opacity=1):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or self.t["line"]}" stroke-width="{sw}" opacity="{opacity}"/>')

    def circle(self, x, y, r, fill=None, stroke=None, sw=1, opacity=1):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill or self.t["primary"]}" opacity="{opacity}"{st}/>')

    def para(self, x, y, value, units, size=16, fill=None, line_h=24, weight=500):
        for i, line in enumerate(wrap(value, units)):
            self.text(x, y + i * line_h, line, size=size, fill=fill or self.t["muted"], weight=weight)

    def badge(self, x, y, value, fill=None, color=None, w=None, h=30, rx=15):
        w = w or int(24 + wlen(value) * 12)
        self.rect(x, y, w, h, fill=fill or self.t["soft"], rx=rx)
        self.text(x + w / 2, y + h / 2 + 5, value, size=13, fill=color or self.t["primary"], weight=800, anchor="middle")

    def path(self, d, stroke=None, fill="none", sw=3, opacity=1):
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{stroke or self.t["primary"]}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>')

    def end(self):
        self.parts.append("</svg>")
        return "\n".join(self.parts)


def table(s, x, y, w, h, headers, rows, row_h=42):
    s.rect(x, y, w, h, stroke=s.t["line"], fill=s.t["panel"])
    s.rect(x, y, w, 44, fill=s.t["soft"], rx=8)
    cw = w / len(headers)
    for i, head in enumerate(headers):
        s.text(x + 16 + i * cw, y + 28, head, size=14, fill=s.t["muted"], weight=800)
    for r, row in enumerate(rows):
        yy = y + 44 + r * row_h
        if yy + row_h > y + h:
            break
        s.line(x, yy, x + w, yy, opacity=0.65)
        for c, val in enumerate(row[: len(headers)]):
            color = s.t["bad"] if any(k in val for k in ["异常", "失败", "冲突", "离线"]) else s.t["text"]
            s.text(x + 16 + c * cw, yy + 27, val, size=14, fill=color, weight=650)


def metric(s, x, y, w, label, value, note="", color=None):
    s.rect(x, y, w, 104, fill=s.t["panel"], stroke=s.t["line"], rx=8)
    s.text(x + 18, y + 30, label, size=14, fill=s.t["muted"], weight=700)
    s.text(x + 18, y + 72, value, size=32, fill=color or s.t["primary"], weight=900, cls="mono")
    if note:
        s.badge(x + w - 88, y + 18, note, fill=s.t["soft"], color=color or s.t["primary"], w=68)


def bars(s, x, y, w, h, vals, color=None):
    gap = 8
    bw = (w - gap * (len(vals) - 1)) / len(vals)
    m = max(vals) or 1
    for i, v in enumerate(vals):
        bh = h * v / m
        s.rect(x + i * (bw + gap), y + h - bh, bw, bh, fill=color or s.t["primary"], rx=4)


def line_chart(s, x, y, w, h, vals, color=None):
    for i in range(4):
        yy = y + i * h / 3
        s.line(x, yy, x + w, yy, opacity=0.45)
    pts = []
    m, mn = max(vals), min(vals)
    span = max(m - mn, 1)
    for i, v in enumerate(vals):
        pts.append((x + i * w / (len(vals) - 1), y + h - (v - mn) / span * h))
    d = "M " + " L ".join(f"{int(px)} {int(py)}" for px, py in pts)
    s.path(d, stroke=color or s.t["primary"], sw=4)
    for px, py in pts:
        s.circle(px, py, 4, fill=color or s.t["primary"])


def rows(kind="student"):
    names = ["陈小雨", "李明轩", "周安然", "王子涵", "赵一诺", "孙嘉乐", "林沐辰", "高悦宁", "钱若溪", "吴昊然"]
    if kind == "audit":
        return [["09:42", "导出档案", "医院管理员", "成功"], ["09:37", "修改权限", "信息科主管", "成功"], ["09:31", "查看敏感字段", "眼科医生", "已审计"], ["09:20", "批量导入", "学校管理员", "失败"], ["09:10", "接口回传", "系统任务", "成功"]]
    if kind == "task":
        return [["五健体检-实验小学", "1832", "82%", "待同步"], ["幼儿园春季筛查", "624", "91%", "已完成"], ["视力专项复查", "216", "46%", "异常"], ["口腔干预随访", "88", "73%", "复查中"]]
    return [[n, f"实验小学{(i % 4) + 1}班", ["正常", "异常", "待复核", "待同步"][i % 4], ["营养", "视力", "脊柱", "心理"][i % 4]] for i, n in enumerate(names)]


def frame(s, theme_key, page):
    code, title, proof, _ = page
    t = s.t
    if theme_key == "A":
        s.rect(18, 16, 1404, 36, fill="#eef1f5", stroke="#6b7280", rx=2)
        s.text(34, 41, t["brand"], 17, "#111827", 850)
        s.text(1350, 41, "□  ×", 18, "#111827", 800, anchor="middle")
        s.rect(18, 52, 1404, 34, fill="#f7f7f7", stroke="#b6bec9", rx=0)
        for i, item in enumerate(["文件", "基础资料", "体检任务", "数据采集", "统计分析", "系统设置", "帮助"]):
            s.text(38 + i * 106, 75, item, 14, "#1f2937", 700)
        s.rect(18, 86, 1404, 54, fill="#dfe6ef", stroke="#9aa7b8", rx=0)
        for i, item in enumerate(["新增", "修改", "删除", "导入", "导出", "打印", "刷新", "审核", "同步"]):
            xx = 34 + i * 72
            s.rect(xx, 98, 58, 30, fill="#f8fafc", stroke="#9aa7b8", rx=2)
            s.text(xx + 29, 119, item, 13, "#1f2937", 750, anchor="middle")
        s.rect(18, 140, 230, 1118, fill="#eef1f5", stroke="#9aa7b8", rx=0)
        s.text(38, 170, "模块导航", 16, "#111827", 850)
        nav = ["工作台", "体检任务", "采集管理", "五健专项", "儿童档案", "基础信息", "随访复查", "统计分析", "系统集成", "系统设置"]
        active = nav[(int(code[1:]) - 1) % len(nav)]
        for i, item in enumerate(nav):
            yy = 210 + i * 42
            if item == active:
                s.rect(34, yy - 24, 198, 32, fill="#c9ddf7", stroke="#6b92c8", rx=0)
            s.text(48, yy, "▣ " + item, 14, "#111827" if item == active else "#374151", 800 if item == active else 600)
        s.rect(248, 140, 1174, 38, fill="#eef1f5", stroke="#9aa7b8", rx=0)
        s.text(270, 165, f"{code} {title}", 17, "#111827", 900)
        s.text(1396, 165, "当前机构：杭州市第一人民医院  用户：医院管理员", 13, "#374151", 650, anchor="end")
        s.rect(248, 178, 1174, 1038, fill="#f7f7f7", stroke="#9aa7b8", rx=0)
        s.rect(260, 190, 1150, 44, fill="#ffffff", stroke="#c0c7d1", rx=0)
        s.text(278, 218, f"验收点：{proof}", 15, "#374151", 700)
        s.rect(18, 1258, 1404, 30, fill="#e7ebf0", stroke="#9aa7b8", rx=0)
        s.text(34, 1279, "就绪 | 数据库连接正常 | 最近同步 09:42 | 内网地址 10.12.8.24", 13, "#374151", 700)
        return (278, 258, 1110, 850)
    if theme_key == "B":
        s.rect(0, 0, 232, H, fill=t["dark"], rx=0)
        s.text(28, 54, "WUJIAN-ADMIN", 20, "#fff", 900)
        s.text(28, 82, t["mode"], 13, "#aebbd0", 650)
        nav = ["首页工作台", "基础信息", "体检任务", "现场采集", "五健专项", "家长服务", "转诊随访", "数据交换", "统计驾驶舱", "系统管理"]
        active = nav[(int(code[1:]) - 1) % len(nav)]
        for i, item in enumerate(nav):
            yy = 134 + i * 52
            if item == active:
                s.rect(18, yy - 30, 198, 40, fill="#315a94", rx=6)
            s.text(42, yy, item, 15, "#fff" if item == active else "#c7d2e5", 800 if item == active else 600)
        s.rect(232, 0, 1208, 72, fill="#fff", stroke=t["line"], rx=0)
        s.text(262, 44, t["brand"], 22, t["text"], 900)
        s.badge(1062, 22, "医院管理员", fill=t["soft"], color=t["primary"], w=112)
        s.badge(1190, 22, "杭州院区", fill="#eefdfb", color=t["accent"], w=104)
        s.rect(232, 72, 1208, 54, fill="#fbfdff", stroke=t["line"], rx=0)
        s.text(262, 106, f"首页 / {active} / {code} {title}", 15, t["muted"], 700)
        s.rect(262, 148, 1128, 70, fill=t["panel"], stroke=t["line"], rx=6)
        s.text(286, 176, f"{code} {title}", 24, t["text"], 900)
        s.para(286, 204, f"验收点：{proof}", 74, 14)
        return (262, 240, 1128, 850)
    if theme_key == "C":
        s.text(58, 62, t["brand"], 30, t["primary"], 900)
        s.text(58, 96, t["mode"], 17, t["muted"], 750)
        s.badge(1194, 48, "家校协同", fill="#fff2e8", color=t["accent"], w=116)
        s.text(58, 150, f"{code} {title}", 34, t["text"], 900)
        s.para(58, 188, f"页面说明：{proof}", 74, 17)
        return (58, 228, 1324, 760)
    s.rect(24, 22, 1392, 62, fill=t["dark"], rx=8)
    s.text(52, 62, t["brand"], 23, "#fff", 900)
    s.text(360, 62, f"{code} {title}", 21, "#d9dcd5", 800)
    for i, cmd in enumerate(["扫码", "暂存", "同步", "复核", "下一位"]):
        fill = t["accent"] if cmd in ["暂存", "同步"] else "#2a2d33"
        col = "#111" if fill == t["accent"] else "#fff"
        s.rect(980 + i * 84, 36, 70, 32, fill=fill, rx=4)
        s.text(1015 + i * 84, 58, cmd, 14, col, 850, anchor="middle")
    s.para(32, 118, f"操作目标：{proof}", 76, 16)
    return (32, 156, 1376, 820)


def portal(s, a, theme_key):
    x, y, w, h = a
    if theme_key in ["A", "C"]:
        cards = [("医院管理端", "任务、档案、权限、接口"), ("医护采集端", "扫码、采集、离线同步"), ("学校/区域端", "班级、进度、风险分析"), ("家长端 H5", "确认信息、报告、复查")]
        for i, (title, desc) in enumerate(cards):
            xx = x + (i % 2) * (w / 2 + 10)
            yy = y + (i // 2) * 220
            s.rect(xx, yy, w / 2 - 24, 184, stroke=s.t["line"], fill=s.t["panel"])
            s.circle(xx + 54, yy + 58, 28, fill=[s.t["primary"], s.t["accent"], s.t["warn"], s.t["bad"]][i], opacity=0.92)
            s.text(xx + 96, yy + 55, title, 24, weight=900)
            s.para(xx + 96, yy + 92, desc, 24, 16)
            s.badge(xx + 96, yy + 130, "进入工作台", color=[s.t["primary"], s.t["accent"], s.t["warn"], s.t["bad"]][i], w=118)
        s.rect(x, y + 462, w - 36, 138, fill=s.t["soft"], stroke=s.t["line"])
        s.text(x + 28, y + 508, "私有化部署 / 多租户 / 统一认证", 24, weight=900)
        s.para(x + 28, y + 546, "同一入口根据医院、学校、科室、现场负责人、家长等角色展示不同门户和数据范围。", 62)
    else:
        for i, item in enumerate(["医院端", "医护端", "学校端", "家长端"]):
            s.rect(x + i * 315, y + 80, 284, 240, fill=s.t["panel"], stroke=s.t["line"], rx=4)
            s.text(x + i * 315 + 142, y + 188, item, 30, [s.t["primary"], s.t["accent"], s.t["warn"], s.t["bad"]][i], 900, anchor="middle")
            s.text(x + i * 315 + 142, y + 228, "角色准入 / 数据隔离", 16, s.t["muted"], 700, anchor="middle")
        line_chart(s, x + 80, y + 430, w - 180, 220, [42, 58, 71, 69, 84, 96, 103], s.t["primary"])


def dashboard(s, a):
    x, y, w, h = a
    for i, m in enumerate([("今日任务", "12", "+3"), ("覆盖人数", "18,426", "96%"), ("异常待复核", "36", "高"), ("待同步", "128", "离线")]):
        metric(s, x + i * (w - 30) / 4, y, (w - 70) / 4, *m, color=[s.t["primary"], s.t["accent"], s.t["bad"], s.t["warn"]][i])
    s.rect(x, y + 136, w * 0.62, 318, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 24, y + 176, "任务进度与异常趋势", 22, weight=900)
    line_chart(s, x + 50, y + 240, w * 0.56, 170, [55, 63, 71, 76, 82, 86, 91], s.t["primary"])
    s.rect(x + w * 0.65, y + 136, w * 0.35 - 30, 318, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.65 + 24, y + 176, "待办队列", 22, weight=900)
    for i, item in enumerate(["异常复核 36", "家长未确认 128", "设备离线 1", "导入失败 27", "复查预约 18"]):
        s.badge(x + w * 0.65 + 26, y + 212 + i * 48, item, fill=s.t["soft"], color=[s.t["bad"], s.t["warn"], s.t["bad"], s.t["bad"], s.t["accent"]][i], w=190, rx=6)
    table(s, x, y + 488, w - 30, 258, ["任务", "覆盖", "进度", "状态"], rows("task"), 46)


def permissions(s, a):
    x, y, w, h = a
    s.rect(x, y, 300, 650, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 24, y + 42, "组织树", 22, weight=900)
    orgs = ["省儿童健康中心", "杭州市第一人民医院", "体检科 / 眼科 / 口腔科", "实验小学", "一年级 / 二年级 / 三年级"]
    for i, o in enumerate(orgs):
        s.text(x + 32 + i * 12, y + 94 + i * 54, "□ " + o, 16, s.t["text"] if i < 2 else s.t["muted"], 750)
    s.rect(x + 326, y, w - 356, 650, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 354, y + 42, "权限矩阵", 22, weight=900)
    roles = ["医院管理员", "科室医生", "学校管理员", "区域监管", "现场负责人"]
    perms = ["档案查看", "批量导出", "异常复核", "任务配置", "接口管理", "审计查看"]
    for i, p in enumerate(perms):
        s.text(x + 514 + i * 118, y + 92, p, 14, s.t["muted"], 800, anchor="middle")
    for r, role in enumerate(roles):
        yy = y + 132 + r * 76
        s.text(x + 354, yy + 28, role, 16, weight=800)
        for c in range(len(perms)):
            color = s.t["accent"] if (r + c) % 3 != 0 else s.t["line"]
            s.circle(x + 514 + c * 118, yy + 22, 13, fill=color)
            if color == s.t["accent"]:
                s.text(x + 514 + c * 118, yy + 28, "✓", 15, "#fff" if s.t["bg"] != "#06111f" else s.t["dark"], 900, anchor="middle")


def audit(s, a):
    x, y, w, h = a
    table(s, x, y, w * 0.62, 520, ["时间", "事件", "操作者", "结果"], rows("audit"), 56)
    s.rect(x + w * 0.65, y, w * 0.35 - 20, 520, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.65 + 24, y + 42, "审计筛选", 22, weight=900)
    for i, item in enumerate(["敏感字段访问", "数据导出", "角色变更", "接口调用", "失败登录"]):
        s.badge(x + w * 0.65 + 28, y + 88 + i * 56, item, fill=s.t["soft"], color=[s.t["bad"], s.t["warn"], s.t["primary"], s.t["accent"], s.t["bad"]][i], w=170, rx=6)
    bars(s, x + w * 0.65 + 32, y + 390, w * 0.28, 90, [4, 9, 3, 12, 6], s.t["primary"])


def students(s, a):
    x, y, w, h = a
    s.rect(x, y, 270, 650, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 24, y + 42, "学校 / 年级 / 班级", 21, weight=900)
    for i, item in enumerate(["实验小学", "一年级", "一(1)班 46人", "一(2)班 44人", "二年级", "二(3)班 48人"]):
        s.text(x + 26 + (i % 3) * 12, y + 92 + i * 48, "▸ " + item, 16, s.t["text"] if i in [0, 1] else s.t["muted"], 750)
    s.rect(x + 300, y, w - 330, 650, fill=s.t["panel"], stroke=s.t["line"])
    for i, b in enumerate(["批量导入", "模板下载", "导出名单", "批量修改"]):
        s.badge(x + 326 + i * 132, y + 26, b, color=[s.t["primary"], s.t["accent"], s.t["warn"], s.t["primary"]][i], w=112, rx=6)
    table(s, x + 324, y + 84, w - 378, 520, ["姓名", "学校班级", "状态", "重点项目"], rows(), 47)


def import_result(s, a):
    x, y, w, h = a
    for i, m in enumerate([("导入总数", "1,859", ""), ("成功", "1,832", "98.5%"), ("失败", "27", "需修正"), ("重复", "16", "可合并")]):
        metric(s, x + i * (w - 40) / 4, y, (w - 80) / 4, *m, color=[s.t["primary"], s.t["accent"], s.t["bad"], s.t["warn"]][i])
    table(s, x, y + 150, w * 0.66, 500, ["行号", "学生姓名", "错误字段", "原因"], [["42", "陈小雨", "证件号", "格式错误"], ["88", "李明轩", "班级", "未匹配"], ["104", "周安然", "姓名", "疑似重复"], ["168", "王子涵", "出生日期", "超出范围"], ["217", "赵一诺", "家长手机号", "缺失"]], 58)
    s.rect(x + w * 0.69, y + 150, w * 0.31 - 20, 500, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.69 + 26, y + 198, "修正建议", 22, weight=900)
    for i, item in enumerate(["下载错误清单", "在线修正字段", "重新上传", "生成导入报告"]):
        s.rect(x + w * 0.69 + 30, y + 246 + i * 70, w * 0.24, 48, fill=s.t["soft"], stroke=s.t["line"], rx=6)
        s.text(x + w * 0.69 + 54, y + 277 + i * 70, item, 16, weight=800)


def archive_list(s, a):
    x, y, w, h = a
    for i, f in enumerate(["学校", "年级", "班级", "风险", "最近体检"]):
        s.badge(x + i * 132, y, f, fill=s.t["panel"], color=s.t["muted"], w=112, rx=6)
    table(s, x, y + 58, w - 30, 590, ["姓名", "学校班级", "档案状态", "重点项目"], rows(), 52)


def archive_detail(s, a):
    x, y, w, h = a
    s.rect(x, y, 330, 650, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 28, y + 54, "陈小雨", 32, weight=900)
    s.text(x + 28, y + 92, "女 / 6岁 / 实验小学一(3)班", 17, s.t["muted"], 750)
    for i, item in enumerate(["一人一档", "家长已确认", "复查待预约", "近视风险"]):
        s.badge(x + 28, y + 136 + i * 48, item, color=[s.t["primary"], s.t["accent"], s.t["warn"], s.t["bad"]][i], w=136, rx=6)
    s.rect(x + 370, y, w - 400, 300, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 398, y + 44, "历次体检趋势", 22, weight=900)
    line_chart(s, x + 430, y + 100, w - 520, 150, [52, 54, 57, 60, 61, 65], s.t["primary"])
    s.rect(x + 370, y + 330, w - 400, 320, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 398, y + 376, "五健指标与复查记录", 22, weight=900)
    for i, item in enumerate(["营养 正常", "视力 异常", "脊柱 待复查", "口腔 干预", "心理 正常"]):
        s.badge(x + 400 + (i % 3) * 190, y + 420 + (i // 3) * 72, item, color=[s.t["accent"], s.t["bad"], s.t["warn"], s.t["primary"], s.t["accent"]][i], w=150, rx=6)


def merge(s, a):
    x, y, w, h = a
    s.rect(x + 90, y + 40, w - 210, 610, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 126, y + 92, "重复档案合并确认", 28, weight=900)
    table(s, x + 126, y + 130, w - 420, 330, ["字段", "档案A", "档案B", "保留策略"], [["姓名", "陈小雨", "陈小雨", "一致"], ["证件号", "3301****82", "3301****82", "一致"], ["班级", "一(3)班", "一(2)班", "人工确认"], ["家长电话", "138****2231", "139****5520", "保留最新"], ["既往史", "无", "过敏性鼻炎", "合并追加"]], 52)
    s.rect(x + 126, y + 500, w - 420, 88, fill=s.t["soft"], stroke=s.t["line"], rx=6)
    s.text(x + 154, y + 548, "合并后将保留历次体检、异常记录、家长通知和复查记录。", 17, s.t["muted"], 750)
    s.badge(x + w - 360, y + 524, "取消", fill=s.t["soft"], color=s.t["muted"], w=96, rx=6)
    s.badge(x + w - 250, y + 524, "确认合并", fill=s.t["primary"], color="#fff", w=120, rx=6)


def tasks(s, a):
    x, y, w, h = a
    table(s, x, y, w - 30, 360, ["任务名称", "覆盖人数", "进度", "状态"], rows("task"), 58)
    for i, item in enumerate(["任务进度", "异常分布", "同步状态"]):
        s.rect(x + i * (w - 60) / 3, y + 400, (w - 100) / 3, 220, fill=s.t["panel"], stroke=s.t["line"])
        s.text(x + i * (w - 60) / 3 + 24, y + 442, item, 22, weight=900)
        if i == 0:
            bars(s, x + 30, y + 486, (w - 160) / 3, 92, [62, 80, 44, 91], s.t["primary"])
        elif i == 1:
            for j, v in enumerate(["视力 36", "BMI 18", "口腔 42"]):
                s.badge(x + i * (w - 60) / 3 + 30, y + 484 + j * 44, v, color=[s.t["bad"], s.t["warn"], s.t["primary"]][j], w=120, rx=6)
        else:
            line_chart(s, x + i * (w - 60) / 3 + 30, y + 488, (w - 190) / 3, 80, [20, 44, 38, 62, 80], s.t["accent"])


def wizard(s, a):
    x, y, w, h = a
    steps = ["基础信息", "体检项目", "采集流程", "人员排班", "通知发布"]
    for i, step in enumerate(steps):
        cx = x + 80 + i * 220
        s.circle(cx, y + 54, 24, fill=s.t["primary"] if i < 3 else s.t["line"])
        s.text(cx, y + 61, str(i + 1), 16, "#fff", 900, anchor="middle")
        s.text(cx - 38, y + 96, step, 15, s.t["text"], 800)
        if i < 4:
            s.line(cx + 26, y + 54, cx + 190, y + 54, s.t["line"], 3)
    s.rect(x, y + 132, w * 0.58, 500, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 28, y + 180, "体检项目配置", 24, weight=900)
    for i, item in enumerate(["身高体重", "视力筛查", "脊柱体态", "口腔检查", "心理量表", "营养评估", "肺活量", "血压"]):
        s.badge(x + 34 + (i % 3) * 170, y + 222 + (i // 3) * 64, item, color=[s.t["primary"], s.t["accent"], s.t["warn"], s.t["bad"]][i % 4], w=138, rx=6)
    s.rect(x + w * 0.62, y + 132, w * 0.38 - 30, 500, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.62 + 28, y + 180, "科室与人员", 24, weight=900)
    for i, item in enumerate(["体检科 4人", "眼科 3人", "口腔科 2人", "心理评估 2人", "现场负责人 1人"]):
        s.text(x + w * 0.62 + 34, y + 232 + i * 56, item, 17, weight=760)


def rules(s, a):
    x, y, w, h = a
    table(s, x, y, w - 30, 520, ["项目", "年龄段", "性别", "阈值", "评价", "建议"], [["BMI", "6-12岁", "全部", "P85-P95", "超重风险", "营养干预"], ["裸眼视力", "4-6岁", "全部", "<4.8", "异常", "眼科复查"], ["脊柱侧弯", "7-15岁", "全部", "阳性", "高风险", "专科转诊"], ["龋齿", "0-6岁", "全部", "≥1", "干预", "口腔治疗"], ["心理量表", "6-15岁", "全部", "临界值", "待访谈", "心理评估"]], 58)


def qr(s, a):
    x, y, w, h = a
    s.rect(x, y, 360, 620, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 28, y + 44, "打印设置", 22, weight=900)
    for i, item in enumerate(["选择班级：一(3)班", "模板：二维码+条码", "纸张：A4 三列", "状态：未打印 46"]):
        s.text(x + 32, y + 98 + i * 52, item, 16, s.t["muted"], 750)
    s.badge(x + 32, y + 332, "批量生成", fill=s.t["primary"], color="#fff", w=128, rx=6)
    s.badge(x + 174, y + 332, "打印预览", fill=s.t["soft"], color=s.t["primary"], w=128, rx=6)
    s.rect(x + 400, y, w - 430, 620, fill=s.t["panel"], stroke=s.t["line"])
    for i in range(12):
        xx = x + 432 + (i % 4) * 185
        yy = y + 42 + (i // 4) * 170
        s.rect(xx, yy, 142, 128, fill=s.t["soft"], stroke=s.t["line"], rx=4)
        for r in range(5):
            for c in range(5):
                if (r * 3 + c + i) % 2 == 0:
                    s.rect(xx + 22 + c * 14, yy + 18 + r * 14, 10, 10, fill=s.t["text"], rx=1)
        s.text(xx + 71, yy + 108, f"一人一码 {i+1:02d}", 13, s.t["muted"], 700, anchor="middle")


def collection(s, a):
    x, y, w, h = a
    s.rect(x, y, 280, 650, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 24, y + 42, "待检队列", 22, weight=900)
    for i, item in enumerate(["陈小雨 一(3)", "李明轩 一(3)", "周安然 一(4)", "王子涵 二(1)", "赵一诺 二(1)", "孙嘉乐 三(2)"]):
        s.rect(x + 24, y + 78 + i * 72, 232, 54, fill=s.t["primary"] if i == 0 else s.t["soft"], rx=6)
        s.text(x + 44, y + 112 + i * 72, item, 16, "#fff" if i == 0 else s.t["text"], 800)
    s.rect(x + 310, y, w - 620, 650, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 340, y + 44, "采集站点进度", 22, weight=900)
    for i, item in enumerate(["身高体重", "视力", "口腔", "脊柱", "心理", "营养"]):
        s.rect(x + 340 + (i % 2) * 230, y + 88 + (i // 2) * 120, 190, 84, fill=s.t["soft"], stroke=s.t["line"], rx=6)
        s.text(x + 360 + (i % 2) * 230, y + 122 + (i // 2) * 120, item, 18, weight=900)
        s.text(x + 360 + (i % 2) * 230, y + 152 + (i // 2) * 120, ["已完成 82%", "排队 12人", "异常 6人"][i % 3], 15, s.t["muted"], 700)
    s.rect(x + w - 280, y, 250, 650, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w - 252, y + 44, "设备状态", 22, weight=900)
    for i, item in enumerate(["身高体重仪 在线", "视力表 在线", "血压计 在线", "肺活量 离线", "扫码枪 在线"]):
        s.text(x + w - 248, y + 96 + i * 58, item, 15, s.t["bad"] if "离线" in item else s.t["accent"], 800)


def entry(s, a):
    x, y, w, h = a
    s.rect(x, y, w - 30, 92, fill=s.t["soft"], stroke=s.t["line"])
    s.text(x + 28, y + 56, "陈小雨  女 / 6岁 / 实验小学一(3)班", 24, weight=900)
    s.badge(x + w - 190, y + 30, "一人一档", fill=s.t["primary"], color="#fff", w=126, rx=6)
    fields = ["身高 118.2cm", "体重 24.1kg", "BMI 17.2", "裸眼视力 4.6", "口腔 龋齿2颗", "脊柱 阴性", "心理量表 待访谈", "营养 正常", "血压 96/62"]
    for i, f in enumerate(fields):
        xx = x + (i % 3) * ((w - 70) / 3)
        yy = y + 130 + (i // 3) * 138
        s.rect(xx, yy, (w - 120) / 3, 104, fill=s.t["panel"], stroke=s.t["line"])
        s.text(xx + 20, yy + 38, f.split()[0], 16, s.t["muted"], 750)
        s.text(xx + 20, yy + 74, " ".join(f.split()[1:]), 24, s.t["bad"] if "4.6" in f or "龋齿" in f else s.t["text"], 900)
    s.rect(x, y + 558, w - 30, 92, fill="#fff7e8" if s.t["bg"] != "#06111f" else s.t["soft"], stroke=s.t["warn"])
    s.text(x + 28, y + 612, "范围校验：裸眼视力低于阈值，口腔龋齿需生成干预建议。", 18, s.t["warn"], 850)


def sync(s, a):
    x, y, w, h = a
    for i, m in enumerate([("本地暂存", "128", "条"), ("待上传", "64", "条"), ("冲突记录", "6", "条"), ("最近同步", "09:42", "")]):
        metric(s, x + i * (w - 40) / 4, y, (w - 80) / 4, *m, color=[s.t["warn"], s.t["primary"], s.t["bad"], s.t["accent"]][i])
    table(s, x, y + 150, w - 30, 500, ["学生", "项目", "冲突字段", "处理方式"], [["陈小雨", "视力", "裸眼视力", "保留复核值"], ["李明轩", "BMI", "体重", "人工确认"], ["周安然", "口腔", "龋齿数", "保留最新"], ["王子涵", "档案", "班级", "合并后上传"]], 62)


def devices(s, a):
    x, y, w, h = a
    devices = [("身高体重仪", "在线", "COM3"), ("视力表", "在线", "蓝牙"), ("血压计", "在线", "USB"), ("肺活量设备", "离线", "未连接"), ("扫码枪", "在线", "USB"), ("本地数据库", "正常", "SQLite")]
    for i, (name, state, port) in enumerate(devices):
        xx = x + (i % 3) * ((w - 70) / 3)
        yy = y + (i // 3) * 230
        s.rect(xx, yy, (w - 110) / 3, 184, fill=s.t["panel"], stroke=s.t["line"])
        s.text(xx + 26, yy + 46, name, 24, weight=900)
        s.text(xx + 26, yy + 86, port, 16, s.t["muted"], 750)
        s.badge(xx + 26, yy + 120, state, color=s.t["bad"] if state == "离线" else s.t["accent"], w=96, rx=6)


def review(s, a):
    x, y, w, h = a
    table(s, x, y, w * 0.58, 560, ["学生", "异常项", "规则", "状态"], [["陈小雨", "视力 4.6", "低于4.8", "待复核"], ["李明轩", "BMI P90", "超重风险", "待通知"], ["周安然", "龋齿2颗", "口腔干预", "已通知"], ["王子涵", "心理量表", "临界值", "待访谈"]], 62)
    s.rect(x + w * 0.62, y, w * 0.38 - 30, 560, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.62 + 28, y + 46, "复核意见", 24, weight=900)
    s.para(x + w * 0.62 + 28, y + 94, "系统命中异常规则后，医生可补充复核意见、生成异常名单并推送家长复查建议。", 30)
    for i, item in enumerate(["确认异常", "转眼科复查", "家长通知", "生成名单"]):
        s.badge(x + w * 0.62 + 30, y + 206 + i * 64, item, color=[s.t["bad"], s.t["warn"], s.t["accent"], s.t["primary"]][i], w=138, rx=6)


def paper(s, a):
    x, y, w, h = a
    s.rect(x, y, w * 0.38, 620, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 28, y + 46, "纸质表单识别/补登", 24, weight=900)
    for i in range(8):
        s.rect(x + 42 + (i % 2) * 170, y + 92 + (i // 2) * 96, 128, 68, fill=s.t["soft"], stroke=s.t["line"], rx=4)
        s.text(x + 106 + (i % 2) * 170, y + 132 + (i // 2) * 96, f"表单 {i+1}", 15, s.t["muted"], 800, anchor="middle")
    s.rect(x + w * 0.42, y, w * 0.58 - 30, 620, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.42 + 28, y + 46, "快速补录", 24, weight=900)
    table(s, x + w * 0.42 + 28, y + 82, w * 0.5, 450, ["字段", "纸质值", "系统建议", "状态"], [["身高", "118.2", "118.2", "已确认"], ["体重", "24.1", "24.1", "已确认"], ["视力", "4.6", "异常", "待复核"], ["口腔", "龋齿2", "干预", "待确认"]], 58)


def followup(s, a):
    x, y, w, h = a
    cols = [("未联系", s.t["warn"]), ("已通知", s.t["primary"]), ("已预约", s.t["accent"]), ("已完成", s.t["muted"])]
    for c, (name, color) in enumerate(cols):
        xx = x + c * ((w - 50) / 4)
        s.rect(xx, y, (w - 95) / 4, 620, fill=s.t["panel"], stroke=s.t["line"])
        s.text(xx + 22, y + 44, name, 22, color, 900)
        for i in range(4):
            s.rect(xx + 18, y + 78 + i * 118, (w - 170) / 4, 86, fill=s.t["soft"], stroke=s.t["line"], rx=6)
            s.text(xx + 36, y + 112 + i * 118, ["陈小雨", "李明轩", "周安然", "王子涵"][i], 16, weight=850)
            s.text(xx + 36, y + 140 + i * 118, ["视力复查", "BMI干预", "口腔治疗", "心理访谈"][i], 14, s.t["muted"], 700)


def five(s, a):
    x, y, w, h = a
    items = [("营养", "BMI/生长发育", s.t["accent"]), ("视力", "裸眼/屈光筛查", s.t["primary"]), ("脊柱", "体态/侧弯筛查", s.t["warn"]), ("口腔", "龋齿/牙列/牙周", s.t["bad"]), ("心理", "量表/访谈/风险", s.t["primary"])]
    for i, (name, desc, color) in enumerate(items):
        xx = x + (i % 3) * ((w - 70) / 3)
        yy = y + (i // 3) * 260
        s.rect(xx, yy, (w - 110) / 3, 210, fill=s.t["panel"], stroke=s.t["line"])
        s.circle(xx + 56, yy + 64, 34, fill=color, opacity=0.95)
        s.text(xx + 110, yy + 58, name, 28, weight=900)
        s.text(xx + 110, yy + 94, desc, 16, s.t["muted"], 750)
        line_chart(s, xx + 32, yy + 126, (w - 210) / 3, 52, [20 + i * 3, 42, 36 + i * 4, 58, 66], color)


def specialty(s, a):
    x, y, w, h = a
    s.rect(x, y, w * 0.62, 620, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 28, y + 46, "视力专题详情", 26, weight=900)
    line_chart(s, x + 52, y + 110, w * 0.54, 210, [5.0, 4.9, 4.8, 4.7, 4.6, 4.8], s.t["primary"])
    table(s, x + 40, y + 370, w * 0.54, 190, ["班级", "筛查人数", "异常率", "复查计划"], [["一(1)班", "46", "12%", "眼科"], ["一(2)班", "44", "9%", "观察"], ["一(3)班", "48", "18%", "复查"]], 46)
    s.rect(x + w * 0.66, y, w * 0.34 - 30, 620, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.66 + 28, y + 46, "干预建议", 24, weight=900)
    for i, item in enumerate(["减少近距离用眼", "预约眼科复查", "家长端推送报告", "30天后随访"]):
        s.badge(x + w * 0.66 + 30, y + 98 + i * 64, item, color=[s.t["primary"], s.t["warn"], s.t["accent"], s.t["bad"]][i], w=170, rx=6)


def parent_form(s, a):
    x, y, w, h = a
    phone_x = x + 40
    s.rect(phone_x, y, 360, 650, fill=s.t["dark"], rx=34)
    s.rect(phone_x + 26, y + 36, 308, 580, fill="#fffdf8" if s.t["bg"] != "#06111f" else s.t["panel"], rx=22)
    s.text(phone_x + 58, y + 92, "信息确认", 24, weight=900)
    for i, item in enumerate(["基础信息", "联系方式", "既往史", "过敏史", "知情同意"]):
        s.rect(phone_x + 58, y + 138 + i * 80, 244, 52, fill=s.t["soft"], stroke=s.t["line"], rx=8)
        s.text(phone_x + 78, y + 171 + i * 80, item, 16, weight=850)
    s.rect(x + 450, y, w - 510, 650, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 480, y + 52, "家长填报状态", 26, weight=900)
    table(s, x + 480, y + 96, w - 580, 430, ["项目", "内容", "状态"], [["基础信息", "姓名/性别/出生日期", "已确认"], ["联系方式", "手机号/家庭住址", "已确认"], ["既往史", "哮喘/过敏", "已填写"], ["知情同意", "电子签名", "已确认"]], 62)


def parent_report(s, a):
    x, y, w, h = a
    s.rect(x, y, 410, 650, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 30, y + 54, "陈小雨的体检报告", 26, weight=900)
    for i, item in enumerate(["营养 正常", "视力 异常", "脊柱 正常", "口腔 干预", "心理 待访谈"]):
        s.badge(x + 34, y + 110 + i * 68, item, color=[s.t["accent"], s.t["bad"], s.t["accent"], s.t["warn"], s.t["primary"]][i], w=150, rx=6)
    s.rect(x + 450, y, w - 480, 300, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 482, y + 50, "历次趋势", 24, weight=900)
    line_chart(s, x + 510, y + 104, w - 590, 140, [56, 60, 64, 63, 68, 72], s.t["primary"])
    s.rect(x + 450, y + 334, w - 480, 316, fill="#fff8e8" if s.t["bg"] != "#06111f" else s.t["soft"], stroke=s.t["warn"])
    s.text(x + 482, y + 384, "医生建议", 24, s.t["warn"], 900)
    s.para(x + 482, y + 426, "建议两周内完成眼科复查，控制连续近距离用眼时间，按家长端健康教育内容进行家庭干预。", 62)


def education(s, a):
    x, y, w, h = a
    cats = ["近视防控", "口腔护理", "营养运动", "心理行为"]
    for i, c in enumerate(cats):
        s.badge(x + i * 150, y, c, color=[s.t["primary"], s.t["bad"], s.t["accent"], s.t["warn"]][i], w=126, rx=6)
    for i in range(8):
        xx = x + (i % 4) * ((w - 60) / 4)
        yy = y + 70 + (i // 4) * 250
        s.rect(xx, yy, (w - 100) / 4, 210, fill=s.t["panel"], stroke=s.t["line"])
        s.rect(xx, yy, (w - 100) / 4, 86, fill=[s.t["soft"], "#fff2e8", "#eef9e8", "#f7efff"][i % 4], rx=8)
        s.text(xx + 22, yy + 124, ["户外活动建议", "刷牙与涂氟", "均衡饮食", "情绪观察"][i % 4], 18, weight=900)
        s.text(xx + 22, yy + 158, "关联异常项 / 已读状态", 14, s.t["muted"], 700)
        s.badge(xx + 22, yy + 174, ["未读", "已读", "收藏"][i % 3], color=[s.t["bad"], s.t["accent"], s.t["primary"]][i % 3], w=78, h=26, rx=6)


def interfaces(s, a):
    x, y, w, h = a
    systems = [["HIS", "REST", "OAuth2", "启用"], ["LIS", "文件交换", "Token", "启用"], ["PACS", "DICOM", "专线", "待联调"], ["统一认证", "OIDC", "SSO", "启用"], ["短信平台", "HTTP", "签名", "启用"]]
    table(s, x, y, w * 0.66, 560, ["系统", "接口类型", "认证方式", "状态"], systems, 62)
    s.rect(x + w * 0.70, y, w * 0.30 - 30, 560, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.70 + 28, y + 46, "接口详情", 24, weight=900)
    for i, item in enumerate(["地址白名单", "字段映射", "失败重试", "调用审计", "二次扩展"]):
        s.text(x + w * 0.70 + 34, y + 98 + i * 58, "✓ " + item, 17, s.t["accent"], 800)


def exchange(s, a):
    x, y, w, h = a
    for i, m in enumerate([("导入批次", "18", ""), ("匹配率", "96.8%", ""), ("失败记录", "27", ""), ("回传结果", "1,204", "")]):
        metric(s, x + i * (w - 40) / 4, y, (w - 80) / 4, *m, color=[s.t["primary"], s.t["accent"], s.t["bad"], s.t["warn"]][i])
    table(s, x, y + 150, w - 30, 500, ["时间", "方向", "系统", "结果"], [["09:42", "导入", "LIS", "成功"], ["09:36", "导出", "HIS", "成功"], ["09:28", "回传", "PACS", "失败"], ["09:10", "同步", "统一认证", "成功"], ["08:58", "通知", "短信平台", "成功"]], 58)


def referral(s, a):
    x, y, w, h = a
    stages = ["异常发现", "医生建议", "预约挂号", "专科复查", "结果回传"]
    for i, st in enumerate(stages):
        cx = x + 90 + i * 240
        s.circle(cx, y + 92, 34, fill=[s.t["bad"], s.t["warn"], s.t["primary"], s.t["accent"], s.t["muted"]][i])
        s.text(cx, y + 101, str(i + 1), 19, "#fff", 900, anchor="middle")
        s.text(cx - 40, y + 148, st, 16, weight=850)
        if i < 4:
            s.line(cx + 38, y + 92, cx + 200, y + 92, s.t["line"], 4)
    table(s, x, y + 220, w - 30, 390, ["儿童", "异常项", "建议科室", "预约状态", "回传"], [["陈小雨", "视力", "眼科", "已预约", "待回传"], ["李明轩", "BMI", "营养门诊", "待确认", "未回传"], ["周安然", "龋齿", "口腔科", "已就诊", "已回传"], ["王子涵", "心理", "心理评估", "已预约", "待回传"]], 58)


def analytics(s, a):
    x, y, w, h = a
    for i, m in enumerate([("覆盖率", "96.4%", ""), ("完成率", "82.1%", ""), ("异常率", "12.8%", ""), ("复查率", "74.8%", "")]):
        metric(s, x + i * (w - 40) / 4, y, (w - 80) / 4, *m, color=[s.t["primary"], s.t["accent"], s.t["bad"], s.t["warn"]][i])
    s.rect(x, y + 150, w * 0.62, 500, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 28, y + 198, "学校/班级异常风险", 24, weight=900)
    bars(s, x + 70, y + 260, w * 0.52, 230, [32, 44, 58, 26, 72, 51], s.t["primary"])
    s.rect(x + w * 0.66, y + 150, w * 0.34 - 30, 500, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.66 + 28, y + 198, "关键指标", 24, weight=900)
    for i, item in enumerate(["近视率 18.6%", "超重肥胖 9.4%", "脊柱异常 3.2%", "龋齿干预 12.1%", "心理风险 2.8%"]):
        s.text(x + w * 0.66 + 36, y + 250 + i * 58, item, 18, [s.t["primary"], s.t["warn"], s.t["bad"], s.t["accent"], s.t["bad"]][i], 850)


def dispatch(s, a):
    x, y, w, h = a
    for i, m in enumerate([("采集点位", "8", ""), ("排队人数", "126", ""), ("漏项预警", "19", ""), ("设备在线", "24/25", "")]):
        metric(s, x + i * (w - 40) / 4, y, (w - 80) / 4, *m, color=[s.t["primary"], s.t["warn"], s.t["bad"], s.t["accent"]][i])
    s.rect(x, y + 150, w * 0.58, 500, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 28, y + 198, "现场点位", 24, weight=900)
    for i in range(8):
        s.circle(x + 90 + (i % 4) * 160, y + 290 + (i // 4) * 150, 42, fill=[s.t["accent"], s.t["primary"], s.t["warn"], s.t["bad"]][i % 4], opacity=0.85)
        s.text(x + 90 + (i % 4) * 160, y + 300 + (i // 4) * 150, str(i + 1), 24, "#fff", 900, anchor="middle")
    s.rect(x + w * 0.62, y + 150, w * 0.38 - 30, 500, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.62 + 28, y + 198, "实时异常流", 24, weight=900)
    for i, item in enumerate(["视力站漏项 6人", "肺活量设备离线", "二(1)班排队过长", "同步队列积压128"]):
        s.badge(x + w * 0.62 + 32, y + 250 + i * 68, item, color=[s.t["bad"], s.t["bad"], s.t["warn"], s.t["primary"]][i], w=210, rx=6)


def readonly(s, a):
    x, y, w, h = a
    s.text(x + w / 2, y + 56, "儿童青少年五健体检工作汇报", 36, s.t["text"], 900, anchor="middle")
    s.badge(x + w / 2 - 70, y + 86, "只读脱敏展示", fill=s.t["bad"], color="#fff", w=140, rx=6)
    for i, m in enumerate([("覆盖学校", "42"), ("体检儿童", "18,426"), ("完成率", "82.1%"), ("复查闭环", "74.8%")]):
        metric(s, x + 80 + i * 290, y + 160, 250, *m, color=[s.t["primary"], s.t["accent"], s.t["warn"], s.t["bad"]][i])
    s.rect(x + 80, y + 330, w - 190, 270, fill=s.t["panel"], stroke=s.t["line"])
    line_chart(s, x + 130, y + 400, w - 300, 130, [20, 36, 48, 64, 71, 82], s.t["primary"])


def backup(s, a):
    x, y, w, h = a
    s.rect(x, y, w * 0.45, 620, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + 28, y + 48, "私有化部署环境", 24, weight=900)
    for i, item in enumerate(["内网地址：10.12.8.24", "数据库：主从高可用", "操作系统：Linux/Windows", "虚拟化：VMware/麒麟", "安全：权限/日志/加密"]):
        s.text(x + 34, y + 104 + i * 62, item, 17, weight=760)
    s.rect(x + w * 0.49, y, w * 0.51 - 30, 620, fill=s.t["panel"], stroke=s.t["line"])
    s.text(x + w * 0.49 + 28, y + 48, "备份与恢复", 24, weight=900)
    table(s, x + w * 0.49 + 28, y + 88, w * 0.42, 380, ["时间", "类型", "校验", "状态"], [["00:30", "全量备份", "通过", "成功"], ["06:30", "增量备份", "通过", "成功"], ["12:30", "文件校验", "通过", "成功"], ["15:00", "恢复演练", "通过", "成功"]], 58)


CONTENT = {
    "portal": portal, "dashboard": dashboard, "permissions": permissions, "audit": audit, "students": students,
    "import": import_result, "archive_list": archive_list, "archive_detail": archive_detail, "merge": merge,
    "tasks": tasks, "wizard": wizard, "rules": rules, "qr": qr, "collection": collection, "entry": entry,
    "sync": sync, "devices": devices, "review": review, "paper": paper, "followup": followup, "five": five,
    "specialty": specialty, "parent_form": parent_form, "parent_report": parent_report, "education": education,
    "interfaces": interfaces, "exchange": exchange, "referral": referral, "analytics": analytics, "dispatch": dispatch,
    "readonly": readonly, "backup": backup,
}


DETAILS = {
    "P01": ("统一认证与角色选择", ["医院管理员：杭州市第一人民医院", "学校管理员：实验小学", "医护采集端：动态码 672914", "家长端：短信验证码登录"]),
    "P03": ("权限编辑 - 科室医生", ["数据范围：本科室 + 本人任务", "允许：档案查看、单人采集、异常复核", "禁止：批量导出、接口配置、备份恢复", "保存后写入操作日志并触发审计"]),
    "P06": ("错误行修正", ["第 23 行：身份证号位数不正确", "第 41 行：学校编码未匹配", "第 58 行：出生日期晚于入学日期", "支持逐条修正、跳过或重新导入"]),
    "P09": ("档案合并确认", ["主档案：陈小雨 3301********0821", "冲突字段：学校、班级、家长电话", "保留历次体检、随访、转诊记录", "合并后原档案进入可追溯归档"]),
    "P11": ("项目选择弹窗", ["必检：身高体重、视力、口腔、脊柱", "选检：血压、肺活量、心理问卷", "按年龄段自动禁用不适用项目", "下一步分配科室与采集人员"]),
    "P12": ("规则编辑 - 视力预警", ["适用：6-12 岁 / 男女通用", "裸眼视力 < 4.8 标记异常", "双眼差值 >= 0.2 标记复核", "建议文案随报告同步到家长端"]),
    "P15": ("异常值确认", ["身高 128.5 cm，体重 38.2 kg", "BMI 超重：超过同年龄 P85", "漏项：左眼矫正视力未录入", "确认后进入异常复核队列"]),
    "P16": ("同步冲突处理", ["本地记录：09:41 采集员张医生修改", "服务器记录：09:39 设备自动回传", "策略：保留最新值并记录差异", "网络恢复后自动重试"]),
    "P18": ("复核意见", ["异常项：脊柱侧弯筛查阳性", "复核结论：建议 2 周内专科复查", "通知对象：家长、班主任、校医", "生成随访计划并进入追踪台账"]),
    "P20": ("随访记录详情", ["最近联系：短信已读，电话未接通", "复查预约：市儿童医院骨科 07-08", "家长反馈：已收到报告，待预约", "下次提醒：3 天后自动触发"]),
    "P23": ("家长确认提示", ["既往史：哮喘史，已核对", "过敏史：青霉素过敏", "监护人电子签名：李女士", "提交后锁定，需医院端退回才可修改"]),
    "P26": ("接口详情 / 字段映射", ["HIS：GET /api/student/identity", "LIS：POST /api/exam/result", "PACS：影像检查号按 studentId 匹配", "测试结果：200 OK，字段 28/28 通过"]),
    "P28": ("转诊单详情", ["建议科室：眼科 / 儿童保健科", "预约状态：已推送，待医院确认", "回传字段：就诊时间、诊断、处理建议", "逾期未就诊自动进入随访提醒"]),
    "P31": ("汇报安全模式", ["脱敏：姓名、证件号、联系电话", "只读：隐藏新增、修改、导出入口", "授权：会议临时链接 2 小时有效", "水印：杭州市卫健委会议查看"]),
    "P32": ("恢复演练详情", ["备份文件：full_20260702_0030.bak", "校验：SHA256 通过", "恢复环境：隔离测试库 10.12.8.66", "耗时：11 分 42 秒，演练成功"]),
}


def detail_overlay(s, theme_key, page, area):
    code = page[0]
    if code not in DETAILS:
        return
    title, lines = DETAILS[code]
    x, y, w, h = area
    t = s.t
    if theme_key == "A":
        ox, oy, ow, oh = x + w - 470, y + 84, 440, 330
        s.rect(ox, oy, ow, oh, fill="#f4f4f4", stroke="#6b7280", rx=2, sw=2)
        s.rect(ox, oy, ow, 34, fill="#d8e7fb", stroke="#6b7280", rx=0)
        s.text(ox + 16, oy + 23, title, 15, "#111827", 850)
        s.text(ox + ow - 22, oy + 23, "×", 17, "#111827", 850, anchor="middle")
        for i, line in enumerate(lines):
            s.text(ox + 24, oy + 72 + i * 42, "■ " + line, 14, "#1f2937", 700)
        s.rect(ox + ow - 172, oy + oh - 52, 68, 30, fill="#e5e7eb", stroke="#9ca3af", rx=2)
        s.text(ox + ow - 138, oy + oh - 32, "取消", 13, "#111827", 700, anchor="middle")
        s.rect(ox + ow - 94, oy + oh - 52, 68, 30, fill=t["primary"], stroke="#1d4ed8", rx=2)
        s.text(ox + ow - 60, oy + oh - 32, "确定", 13, "#fff", 800, anchor="middle")
    elif theme_key == "B":
        ox, oy, ow, oh = x + w - 424, y - 6, 424, 640
        s.rect(ox, oy, ow, oh, fill="#fff", stroke=t["line"], rx=8)
        s.text(ox + 26, oy + 44, title, 21, t["text"], 900)
        s.text(ox + ow - 30, oy + 44, "×", 22, t["muted"], 800, anchor="middle")
        for i, line in enumerate(lines):
            yy = oy + 92 + i * 72
            s.rect(ox + 24, yy - 28, ow - 48, 48, fill=t["soft"], stroke=t["line"], rx=6)
            s.text(ox + 42, yy + 2, line, 14, t["text"], 700)
        s.badge(ox + 26, oy + oh - 64, "保存并写入审计日志", fill=t["primary"], color="#fff", w=156, h=34, rx=6)
    elif theme_key == "C":
        ox, oy, ow, oh = x + w - 430, y + 40, 398, 292
        s.rect(ox, oy, ow, oh, fill="#fff", stroke=t["line"], rx=18)
        s.text(ox + 26, oy + 46, title, 22, t["text"], 900)
        for i, line in enumerate(lines[:4]):
            s.text(ox + 28, oy + 92 + i * 38, line, 15, t["muted"], 700)
        s.badge(ox + 28, oy + oh - 56, "已同步到家长端", fill="#fff2e8", color=t["accent"], w=142)
    else:
        ox, oy, ow, oh = x + w - 500, y + 44, 468, 330
        s.rect(ox, oy, ow, oh, fill="#ffffff", stroke="#1f2937", rx=6)
        s.text(ox + 24, oy + 46, title, 22, "#111827", 900)
        for i, line in enumerate(lines[:4]):
            s.line(ox + 24, oy + 78 + i * 48, ox + ow - 24, oy + 78 + i * 48, "#e5e7eb")
            s.text(ox + 24, oy + 110 + i * 48, line, 15, "#374151", 700)
        s.badge(ox + ow - 154, oy + oh - 58, "确认处理", fill=t["dark"], color="#fff", w=112, h=34, rx=4)


def render(theme_key, page) -> str:
    s = SVG(THEMES[theme_key])
    area = frame(s, theme_key, page)
    kind = page[3]
    if kind == "portal":
        portal(s, area, theme_key)
    else:
        CONTENT[kind](s, area)
    detail_overlay(s, theme_key, page, area)
    return s.end()


def clean():
    OUT.mkdir(exist_ok=True)
    SVG_OUT.mkdir(exist_ok=True)
    for theme in THEMES.values():
        d = OUT / theme["dir"]
        d.mkdir(parents=True, exist_ok=True)
        for p in d.glob("*.png"):
            p.unlink()
        sd = SVG_OUT / theme["dir"]
        sd.mkdir(parents=True, exist_ok=True)
        for p in sd.glob("*.svg"):
            p.unlink()


def convert(svg: Path, png: Path):
    tmp = png.parent / "_qltmp"
    tmp.mkdir(exist_ok=True)
    for p in tmp.iterdir():
        p.unlink()
    result = subprocess.run(["qlmanage", "-t", "-s", "1440", "-o", str(tmp), str(svg)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    candidates = list(tmp.glob("*.png"))
    if result.returncode != 0 or not candidates:
        raise RuntimeError(f"qlmanage failed for {svg}\n{result.stdout}\n{result.stderr}")
    shutil.move(str(candidates[0]), str(png))
    for p in tmp.iterdir():
        p.unlink()
    tmp.rmdir()


def main():
    clean()
    count = 0
    for key, theme in THEMES.items():
        svg_dir = SVG_OUT / theme["dir"]
        png_dir = OUT / theme["dir"]
        for page in PAGES:
            code, title, _, _ = page
            name = f"{code}-{title.replace('/', '-')}"
            svg = svg_dir / f"{name}.svg"
            png = png_dir / f"{name}.png"
            svg.write_text(render(key, page), encoding="utf-8")
            convert(svg, png)
            count += 1
    print(f"generated_png={count}")
    for theme in THEMES.values():
        print(f'{theme["dir"]}: {len(list((OUT / theme["dir"]).glob("*.png")))}')


if __name__ == "__main__":
    main()
