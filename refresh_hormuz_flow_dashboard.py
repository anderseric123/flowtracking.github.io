#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from html import unescape
from pathlib import Path
from typing import Iterable


WORKDIR = Path(__file__).resolve().parent
OUTPUT_PATH = WORKDIR / "hormuz-flow-data.js"
BLOG_URL = "https://windward.ai/blog/"
REALTIME_DASHBOARD_URL = "https://hormuzstraitmonitor.com/api/dashboard"
REALTIME_SOURCE_NAME = "第三方监测数据"
CACHE_DIR = Path("/tmp/hormuz-flow-cache")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0 Safari/537.36"
CURL_BIN = "/usr/bin/curl"
MAX_POSTS = 6
EXTRA_URLS = [
    "https://windward.ai/blog/48-hours-into-the-iran-war/",
    "https://windward.ai/blog/one-week-into-the-iran-war/",
    "https://windward.ai/blog/march-8-maritime-intelligence-daily/",
]

TRACKED_SLUG_KEYWORDS = (
    "iran-war-maritime-intelligence-daily",
    "maritime-intelligence-daily",
    "48-hours-into-the-iran-war",
    "one-week-into-the-iran-war",
)

WORD_TO_NUMBER = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
    "hundred": 100,
}

MONTH_TO_NUMBER = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}

COMMODITY_BASELINES = [
    {
        "id": "crude_and_products",
        "name": "原油及成品油",
        "flowValue": 2100.0,
        "flowUnit": "万桶/日",
        "globalSeaborneSharePct": 30,
        "sourceHubs": "沙特、伊拉克、阿联酋、伊朗",
        "majorDestinations": "东亚、印度、欧洲",
        "sensitivity": 1.0,
    },
    {
        "id": "lng",
        "name": "液化天然气（LNG）",
        "flowValue": 1100.0,
        "flowUnit": "亿立方米/年",
        "globalSeaborneSharePct": 20,
        "sourceHubs": "卡塔尔、阿联酋",
        "majorDestinations": "东亚、欧洲",
        "sensitivity": 1.0,
    },
    {
        "id": "lpg",
        "name": "液化石油气（LPG）",
        "flowValue": 5000.0,
        "flowUnit": "万吨/年",
        "globalSeaborneSharePct": 30,
        "sourceHubs": "沙特、卡塔尔、阿联酋、科威特",
        "majorDestinations": "东亚",
        "sensitivity": 0.95,
    },
    {
        "id": "methanol",
        "name": "甲醇",
        "flowValue": 2000.0,
        "flowUnit": "万吨/年",
        "globalSeaborneSharePct": 60,
        "sourceHubs": "伊朗、沙特、阿联酋",
        "majorDestinations": "中国、欧洲、东南亚",
        "sensitivity": 0.9,
    },
    {
        "id": "fertilizers",
        "name": "化肥（尿素及磷肥）",
        "flowValue": 1800.0,
        "flowUnit": "万吨/年",
        "globalSeaborneSharePct": 25,
        "sourceHubs": "卡塔尔、沙特、阿联酋",
        "majorDestinations": "印度、南美、美国",
        "sensitivity": 0.8,
    },
    {
        "id": "aluminum",
        "name": "铝及铝制品",
        "flowValue": 700.0,
        "flowUnit": "万吨/年",
        "globalSeaborneSharePct": 15,
        "sourceHubs": "阿联酋、卡塔尔、阿曼、巴林",
        "majorDestinations": "全球制造中心",
        "sensitivity": 0.75,
    },
    {
        "id": "autos",
        "name": "汽车（核心为进口）",
        "flowValue": 300.0,
        "flowUnit": "万辆/年",
        "globalSeaborneSharePct": 5,
        "sourceHubs": "日本、韩国、德国、中国",
        "majorDestinations": "沙特、阿联酋",
        "sensitivity": 0.55,
    },
]

COMMODITY_REFERENCE_SOURCES = [
    "EIA",
    "IEA",
    "IGU",
    "Argus",
    "Vortexa",
    "IAI",
    "FAO",
    "OICA",
]

REALTIME_REFERENCE_SOURCES = [
    "第三方监测数据",
]


@dataclass
class TrafficPoint:
    trafficDate: str
    reportDate: str
    reportTitle: str
    sourceUrl: str
    crossings: float
    exact: bool
    note: str
    sevenDayAverage: float | None = None
    inbound: int | None = None
    outbound: int | None = None
    other: int | None = None
    sourceType: str = "windward"
    isRolling24h: bool = False


def run_curl(url: str) -> str:
    result = subprocess.run(
        [CURL_BIN, "-L", "--connect-timeout", "15", "--retry", "2", "--retry-delay", "2", "--max-time", "45", "-A", USER_AGENT, url],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def html_to_text(value: str) -> str:
    value = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", " ", value, flags=re.I)
    value = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return collapse_whitespace(unescape(value))


def extract_article_body(html: str) -> str:
    match = re.search(
        r'<div\s+class="article__body">(.*?)<div\s+class="article__aside article__aside--end">',
        html,
        flags=re.S,
    )
    return match.group(1) if match else html


def extract_urls(blog_html: str) -> list[str]:
    urls = re.findall(r'href="(https://windward\.ai/blog/[^"]+)"', blog_html)
    filtered = []
    for url in urls:
        if any(keyword in url for keyword in TRACKED_SLUG_KEYWORDS):
            filtered.append(url.rstrip("/"))
    deduped = []
    seen = set()
    for url in filtered + EXTRA_URLS:
        normalized = url.rstrip("/")
        if normalized not in seen:
            deduped.append(normalized + "/")
            seen.add(normalized)
    return deduped[:MAX_POSTS + len(EXTRA_URLS)]


def parse_iso_date(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def cache_path_for_url(url: str, cache_dir: Path) -> Path:
    slug = url.rstrip("/").split("/")[-1] or "blog"
    return cache_dir / f"{slug}.html"


def load_html(url: str, cache_dir: Path, use_cache: bool) -> str:
    cache_path = cache_path_for_url(url, cache_dir)
    if use_cache and cache_path.exists():
        return cache_path.read_text(encoding="utf-8")
    if use_cache:
        raise FileNotFoundError(f"Missing cached file for {url}")
    html = run_curl(url)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(html, encoding="utf-8")
    return html


def safe_float(value: object) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", "").strip())
        except ValueError:
            return None
    return None


def load_realtime_dashboard_payload(cache_dir: Path, use_cache: bool) -> dict | None:
    cache_path = cache_dir / "hormuzstraitmonitor-dashboard.json"
    if use_cache and cache_path.exists():
        raw = cache_path.read_text(encoding="utf-8")
    elif use_cache:
        raise FileNotFoundError("Missing cached file for realtime dashboard")
    else:
        raw = run_curl(REALTIME_DASHBOARD_URL)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(raw, encoding="utf-8")

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    if not isinstance(payload.get("data"), dict):
        return None
    return payload


def build_realtime_point(payload: dict) -> tuple[TrafficPoint | None, dict | None]:
    data = payload.get("data")
    if not isinstance(data, dict):
        return None, None

    ship_count = data.get("shipCount") if isinstance(data.get("shipCount"), dict) else {}
    oil_price = data.get("oilPrice") if isinstance(data.get("oilPrice"), dict) else {}
    stranded = data.get("strandedVessels") if isinstance(data.get("strandedVessels"), dict) else {}
    insurance = data.get("insurance") if isinstance(data.get("insurance"), dict) else {}
    throughput = data.get("throughput") if isinstance(data.get("throughput"), dict) else {}
    strait_status = data.get("straitStatus") if isinstance(data.get("straitStatus"), dict) else {}

    last24h = safe_float(ship_count.get("last24h"))
    current_transits = safe_float(ship_count.get("currentTransits"))
    normal_daily = safe_float(ship_count.get("normalDaily"))
    if last24h is None:
        return None, None

    last_updated_value = data.get("lastUpdated") or payload.get("timestamp")
    report_dt: date
    if isinstance(last_updated_value, str):
        try:
            report_dt = parse_iso_date(last_updated_value).date()
        except ValueError:
            report_dt = datetime.utcnow().date()
    else:
        report_dt = datetime.utcnow().date()

    baseline_desc = f"{normal_daily:g}" if normal_daily is not None else "N/A"
    current_desc = f"{current_transits:g}" if current_transits is not None else "N/A"
    note = f"{REALTIME_SOURCE_NAME}显示过去24小时通行为 {last24h:g}，当前在途 {current_desc}，常态日均约 {baseline_desc}。"

    point = TrafficPoint(
        trafficDate=report_dt.isoformat(),
        reportDate=report_dt.isoformat(),
        reportTitle=f"{REALTIME_SOURCE_NAME} Realtime Dashboard",
        sourceUrl="",
        crossings=last24h,
        exact=True,
        note=note,
        sevenDayAverage=normal_daily,
        sourceType="realtime",
        isRolling24h=True,
    )

    realtime_signals = {
        "lastUpdated": last_updated_value,
        "sourceName": REALTIME_SOURCE_NAME,
        "status": strait_status.get("status"),
        "statusDescription": strait_status.get("description"),
        "shipCountLast24h": ship_count.get("last24h"),
        "shipCountCurrentTransits": ship_count.get("currentTransits"),
        "shipCountNormalDaily": ship_count.get("normalDaily"),
        "shipCountPercentOfNormal": ship_count.get("percentOfNormal"),
        "strandedVesselsTotal": stranded.get("total"),
        "strandedVesselsChangeToday": stranded.get("changeToday"),
        "brentPrice": oil_price.get("brentPrice"),
        "brentChangePct24h": oil_price.get("changePercent24h"),
        "insuranceMultiplier": insurance.get("multiplier"),
        "throughputPercentOfNormal": throughput.get("percentOfNormal"),
        "referenceSources": REALTIME_REFERENCE_SOURCES,
    }
    return point, realtime_signals


def token_to_number(token: str | None) -> int | None:
    if token is None:
        return None
    token = token.strip().lower().replace(",", "")
    if not token:
        return None
    if token.isdigit():
        return int(token)
    if token in WORD_TO_NUMBER:
        return WORD_TO_NUMBER[token]
    if "-" in token:
        parts = [WORD_TO_NUMBER.get(part) for part in token.split("-")]
        if all(part is not None for part in parts):
            return int(sum(parts))
    if " " in token:
        parts = token.split()
        total = 0
        current = 0
        for part in parts:
            number = WORD_TO_NUMBER.get(part)
            if number is None:
                return None
            if number == 100:
                current = max(1, current) * number
            else:
                current += number
        total += current
        return total if total else None
    return None


def parse_month_day(text: str, year: int, default_month: int | None = None) -> date | None:
    match = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})", text, flags=re.I)
    if match:
        month = MONTH_TO_NUMBER[match.group(1).lower()]
        day = int(match.group(2))
        return date(year, month, day)
    if default_month is not None:
        match = re.search(r"\b(\d{1,2})\b", text)
        if match:
            return date(year, default_month, int(match.group(1)))
    return None


def find_first(text: str, patterns: Iterable[re.Pattern[str]]) -> re.Match[str] | None:
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            return match
    return None


def extract_hormuz_snippet(body_text: str) -> str:
    anchors = [
        "Crossings through the Strait of Hormuz",
        "Maritime traffic through the Strait of Hormuz",
        "Traffic data confirms the impact",
        "Windward analysis tracked just under",
        "Strait of Hormuz Traffic",
        "The Strait of Hormuz Is Closed",
        "Hormuz Traffic Collapses Further",
    ]
    positions = [body_text.find(anchor) for anchor in anchors if body_text.find(anchor) >= 0]
    if not positions:
        return body_text[:1200]
    start = min(positions)
    return body_text[start:start + 1400]


def extract_numbered_context(text: str, pattern: str) -> int | None:
    match = re.search(pattern, text, flags=re.I)
    if not match:
        return None
    return token_to_number(match.group(1))


def parse_daily_point(article_html: str, url: str) -> TrafficPoint | None:
    title_match = re.search(r"<title>([^<]+)</title>", article_html)
    date_match = re.search(r'"datePublished":"([^"]+)"', article_html)
    if not title_match or not date_match:
        return None

    report_title = collapse_whitespace(unescape(title_match.group(1).replace(" - Windward", "")))
    published = parse_iso_date(date_match.group(1))
    report_date = published.date()
    body_text = html_to_text(extract_article_body(article_html))
    snippet = extract_hormuz_snippet(body_text)

    if "just under" in snippet.lower() and "Hormuz transits in the past 24 hours" in snippet:
        match = re.search(r"just under\s+(\d+)\s+Hormuz transits in the past 24 hours", snippet, flags=re.I)
        if not match:
            return None
        approx_count = int(match.group(1)) - 1
        return TrafficPoint(
            trafficDate=report_date.isoformat(),
            reportDate=report_date.isoformat(),
            reportTitle=report_title,
            sourceUrl=url,
            crossings=approx_count,
            exact=False,
            note="过去24小时过境量约为 100 艘附近，Windward 表述为“just under 100”，这里按 99 记为近似值。"
        )

    count_match = find_first(
        snippet,
        [
            re.compile(r"Only\s+([A-Za-z0-9-]+)\s+(?:total\s+)?(?:vessel\s+)?crossings were recorded(?:\s+on\s+(March\s+\d{1,2}))?", re.I),
            re.compile(r"Only\s+([A-Za-z0-9-]+)\s+vessels crossed the Strait", re.I),
            re.compile(r"Only\s+([A-Za-z0-9-]+)\s+vessels transited the corridor", re.I),
            re.compile(r"A total of\s+([A-Za-z0-9-]+)\s+crossings were recorded", re.I),
            re.compile(r"with only\s+([A-Za-z0-9-]+)\s+total crossings recorded", re.I),
        ],
    )
    if not count_match:
        return None

    crossings = token_to_number(count_match.group(1))
    if crossings is None:
        return None

    traffic_date = parse_month_day(snippet, report_date.year)
    if traffic_date is None:
        traffic_date = report_date - timedelta(days=1)

    avg_match = find_first(
        snippet,
        [
            re.compile(r"(?:7-day|seven-day)(?: moving)? average of ([0-9.]+) crossings", re.I),
            re.compile(r"recent seven-day average of ([0-9.]+) crossings", re.I),
            re.compile(r"7-day average of ([0-9.]+) crossings", re.I),
        ],
    )

    inbound = extract_numbered_context(snippet, r"\(\s*([A-Za-z0-9-]+)\s+inbound")
    if inbound is None:
        inbound = extract_numbered_context(snippet, r"including\s+([A-Za-z0-9-]+)\s+inbound\s+and\s+[A-Za-z0-9-]+\s+outbound")
    outbound = extract_numbered_context(snippet, r"inbound\s+and\s+([A-Za-z0-9-]+)\s+outbound")
    if inbound is None:
        inbound = extract_numbered_context(snippet, r"([A-Za-z0-9-]+)\s+inbound,\s*[A-Za-z0-9-]+\s+outbound")
    if outbound is None:
        outbound = extract_numbered_context(snippet, r"[A-Za-z0-9-]+\s+inbound,\s*([A-Za-z0-9-]+)\s+outbound")

    other = extract_numbered_context(snippet, r"and\s+([A-Za-z0-9-]+)\s+additional transit")
    note = collapse_whitespace(snippet[:280])
    return TrafficPoint(
        trafficDate=traffic_date.isoformat(),
        reportDate=report_date.isoformat(),
        reportTitle=report_title,
        sourceUrl=url,
        crossings=float(crossings),
        exact=True,
        note=note,
        sevenDayAverage=float(avg_match.group(1)) if avg_match else None,
        inbound=inbound,
        outbound=outbound,
        other=other,
    )


def build_context_signals(article_texts: list[str]) -> dict[str, int | None]:
    joined = " ".join(article_texts)
    affected_vessels = extract_numbered_context(joined, r"more than\s+([\d,]+)\s+vessels experienced GPS and AIS interference")
    injected_zones = extract_numbered_context(joined, r"([A-Za-z0-9,-]+)\s+injected signal zones")
    denial_areas = extract_numbered_context(joined, r"([A-Za-z0-9,-]+)\s+denial areas")
    confirmed_strikes = extract_numbered_context(joined, r"([A-Za-z0-9,-]+)\s+vessels have been confirmed struck")
    return {
        "affectedVessels": affected_vessels,
        "injectedZones": injected_zones,
        "denialAreas": denial_areas,
        "confirmedStrikes": confirmed_strikes,
    }


def commodity_risk_level(score: float) -> str:
    if score >= 80:
        return "极高"
    if score >= 65:
        return "高"
    if score >= 50:
        return "中高"
    return "中"


def build_commodity_exposure(summary: dict) -> dict:
    latest_crossings = float(summary["latestCrossings"])
    week_avg = summary.get("sevenDayAverage")
    stress_ratio = 0.0

    if week_avg is not None and week_avg > 0:
        stress_ratio = max(0.0, min(1.0, 1.0 - (latest_crossings / float(week_avg))))
        stress_basis = f"按最新通行 {latest_crossings:g} 对比 7 日均值 {float(week_avg):g} 计算"
    else:
        collapse_pct = summary.get("collapseFromStartPct")
        collapse_ratio = abs(float(collapse_pct)) / 100 if collapse_pct is not None else 0.0
        stress_ratio = max(0.0, min(1.0, collapse_ratio))
        stress_basis = "7 日均值缺失，改用相对起点跌幅估算"

    items = []
    for base in COMMODITY_BASELINES:
        share_pct = float(base["globalSeaborneSharePct"])
        sensitivity = float(base["sensitivity"])
        risk_score = min(99.0, round(25 + stress_ratio * 60 + share_pct * 0.35 + sensitivity * 8, 1))
        estimated_at_risk_flow = round(float(base["flowValue"]) * stress_ratio, 2)
        items.append(
            {
                "id": base["id"],
                "name": base["name"],
                "flowValue": base["flowValue"],
                "flowUnit": base["flowUnit"],
                "globalSeaborneSharePct": base["globalSeaborneSharePct"],
                "sourceHubs": base["sourceHubs"],
                "majorDestinations": base["majorDestinations"],
                "riskScore": risk_score,
                "riskLevel": commodity_risk_level(risk_score),
                "estimatedAtRiskFlow": estimated_at_risk_flow,
                "estimatedAtRiskUnit": base["flowUnit"],
            }
        )

    items.sort(key=lambda item: (item["riskScore"], item["globalSeaborneSharePct"]), reverse=True)
    top = items[0]
    return {
        "stressPct": round(stress_ratio * 100, 1),
        "stressBasis": stress_basis,
        "topRiskCommodity": top["name"],
        "topRiskScore": top["riskScore"],
        "note": "品种流量与全球占比为行业公开估算口径（用于监控霍尔木兹重要性），不等同于实时海关结算。",
        "referenceSources": COMMODITY_REFERENCE_SOURCES,
        "items": items,
    }


def sort_points(points: list[TrafficPoint]) -> list[TrafficPoint]:
    return sorted(points, key=lambda item: item.trafficDate)


def point_quality_score(point: TrafficPoint) -> int:
    score = 0
    title_lower = point.reportTitle.lower()
    if "maritime intelligence daily" in title_lower:
        score += 8
    if point.exact:
        score += 4
    if point.sevenDayAverage is not None:
        score += 3
    if point.inbound is not None:
        score += 1
    if point.outbound is not None:
        score += 1
    if point.other is not None:
        score += 1
    return score


def dedupe_points(points: list[TrafficPoint]) -> list[TrafficPoint]:
    by_date: dict[str, TrafficPoint] = {}
    for point in points:
        current = by_date.get(point.trafficDate)
        if current is None:
            by_date[point.trafficDate] = point
            continue

        candidate_key = (
            point_quality_score(point),
            point.reportDate,
            point.reportTitle,
        )
        current_key = (
            point_quality_score(current),
            current.reportDate,
            current.reportTitle,
        )
        if candidate_key > current_key:
            by_date[point.trafficDate] = point
    return sorted(by_date.values(), key=lambda item: item.trafficDate)


def extract_report_date(article_html: str) -> date | None:
    date_match = re.search(r'"datePublished":"([^"]+)"', article_html)
    if not date_match:
        return None
    try:
        return parse_iso_date(date_match.group(1)).date()
    except ValueError:
        return None


def build_summary(points: list[TrafficPoint], latest_article_date: str | None) -> tuple[dict, list[str]]:
    if len(points) < 2:
        raise RuntimeError("可用于展示的有效数据点不足 2 个")

    latest = points[-1]
    prev = points[-2]
    oldest = points[0]
    day_over_day_pct = ((latest.crossings - prev.crossings) / prev.crossings) * 100 if prev.crossings else None
    gap_to_week_avg_pct = None
    if latest.sevenDayAverage:
        gap_to_week_avg_pct = ((latest.crossings - latest.sevenDayAverage) / latest.sevenDayAverage) * 100

    collapse_from_start_pct = None
    if oldest.crossings:
        collapse_from_start_pct = ((latest.crossings - oldest.crossings) / oldest.crossings) * 100

    status = "仍显著低于近一周常态"
    if latest.sevenDayAverage and latest.crossings >= latest.sevenDayAverage * 0.85:
        status = "接近近一周常态"
    elif latest.sevenDayAverage and latest.crossings < latest.sevenDayAverage * 0.3:
        status = "通行量仍处于冻结区间"

    latest_from_realtime = latest.sourceType == "realtime"
    latest_source_name = REALTIME_SOURCE_NAME if latest_from_realtime else "Windward 公开博客日报"

    caveats: list[str] = []
    if latest_from_realtime:
        caveats.append(
            f"最新可量化点来自{REALTIME_SOURCE_NAME}，更新日期 {latest.reportDate}，过去24小时通行为 {latest.crossings:g}。"
        )
        caveats.append("该值是截至抓取时点的过去24小时滚动口径，不等同于自然日结算值。")
    elif latest_article_date and latest_article_date > latest.reportDate:
        caveats.append(
            f"最新可抓取文章发布时间为 {latest_article_date}，但该文未给出可稳定抽取的新增 crossings 日值；当前最后一个可量化通行日仍是 {latest.trafficDate}（对应报告 {latest.reportDate}）。"
        )
    else:
        caveats.append(
            f"最新可抓取日报发布时间为 {latest.reportDate}，覆盖的霍尔木兹通行日是 {latest.trafficDate}，不是当前时点的原始 AIS 实时流。"
        )

    if oldest.exact is False:
        caveats.append("2026-03-01 的起始点来自 Windward 对“过去24小时”过境量的近似描述，不是完整日终结算值。")

    if latest.note.lower().find("no change compared to the previous day") >= 0 and latest.crossings != prev.crossings:
        caveats.append("2026-03-05 日报正文写有“no change compared to the previous day”，但相邻两日报抽取出的原始 crossings 为 4 和 5；仪表盘以原始数值为准。")

    return (
        {
            "latestArticleDate": latest_article_date,
            "latestTrafficDate": latest.trafficDate,
            "latestCrossings": latest.crossings,
            "previousTrafficDate": prev.trafficDate,
            "previousCrossings": prev.crossings,
            "dayOverDayPct": day_over_day_pct,
            "sevenDayAverage": latest.sevenDayAverage,
            "gapToWeekAveragePct": gap_to_week_avg_pct,
            "collapseFromStartPct": collapse_from_start_pct,
            "status": status,
            "latestReportDate": latest.reportDate,
            "latestReportTitle": latest.reportTitle,
            "latestSourceName": latest_source_name,
            "latestSourceUrl": latest.sourceUrl,
            "latestSourceType": latest.sourceType,
            "latestIsRolling24h": latest.isRolling24h,
        },
        caveats,
    )


def build_timeline(points: list[TrafficPoint]) -> list[dict]:
    items = []
    for point in points:
        crossings = float(point.crossings)
        message = f"{int(crossings) if crossings.is_integer() else crossings} 次通行"
        if point.sevenDayAverage:
            message += f"，对比 7 日均值 {point.sevenDayAverage:g}"
        items.append(
            {
                "trafficDate": point.trafficDate,
                "reportDate": point.reportDate,
                "title": message,
                "note": point.note,
                "sourceUrl": point.sourceUrl,
                "exact": point.exact,
            }
        )
    return items


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh Hormuz flow dashboard data from Windward public pages.")
    parser.add_argument("--use-cache", action="store_true", help="Only parse previously downloaded HTML files in the cache directory.")
    parser.add_argument("--cache-dir", type=Path, default=CACHE_DIR, help="Directory used to store or read cached HTML files.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    blog_html = load_html(BLOG_URL, args.cache_dir, args.use_cache)
    urls = extract_urls(blog_html)

    points: list[TrafficPoint] = []
    article_texts: list[str] = []
    article_dates: list[date] = []
    realtime_signals: dict | None = None
    for url in urls:
        try:
            article_html = load_html(url, args.cache_dir, args.use_cache)
        except FileNotFoundError:
            continue
        if "Page not found - Windward" in article_html:
            continue
        report_date = extract_report_date(article_html)
        if report_date is not None:
            article_dates.append(report_date)
        body_text = html_to_text(extract_article_body(article_html))
        article_texts.append(body_text)
        point = parse_daily_point(article_html, url)
        if point is not None:
            points.append(point)

    try:
        realtime_payload = load_realtime_dashboard_payload(args.cache_dir, args.use_cache)
    except FileNotFoundError:
        realtime_payload = None
    except subprocess.CalledProcessError:
        realtime_payload = None

    if realtime_payload is not None:
        realtime_point, realtime_signals = build_realtime_point(realtime_payload)
        if realtime_point is not None:
            points.append(realtime_point)

    points = dedupe_points(sort_points(points))
    latest_article_date = max(article_dates).isoformat() if article_dates else None
    summary, caveats = build_summary(points, latest_article_date)
    context_signals = build_context_signals(article_texts)
    commodity_exposure = build_commodity_exposure(summary)

    payload = {
        "generatedAt": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "source": {
            "name": "Windward + 第三方监测数据",
            "url": BLOG_URL,
            "method": "Windward 日报用于历史序列；第三方监测数据用于滚动24小时补点",
        },
        "summary": summary,
        "contextSignals": context_signals,
        "realtimeSignals": realtime_signals,
        "commodityExposure": commodity_exposure,
        "points": [asdict(point) for point in points],
        "timeline": build_timeline(points),
        "caveats": caveats,
    }

    OUTPUT_PATH.write_text(
        "window.HORMUZ_FLOW_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
