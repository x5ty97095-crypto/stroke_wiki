#!/usr/bin/env python3
"""Gate 2: Programmatic numeric/COR grounding + AI semantic audit verification."""

import json
import re
import sys
from pathlib import Path

# Strip commas inside numbers (e.g., 3,648 -> 3648) before matching
COMMA_IN_NUM_RE = re.compile(r"(?<=\d),(?=\d{3}(?!\d))")

# CJK-safe numeric pattern using ASCII digit lookarounds instead of \b:
# 1) Percentages (e.g., 5%, 35%, 1.18%)
# 2) Decimals (e.g., 4.5, 0.25, 0.9)
# 3) Multi-digit integers >= 2 digits (e.g., 24, 80, 180, 3648)
# 4) Single-digit numbers immediately followed by clinical units (e.g., 6h, 4 小時, 5 mg, 7 天)
NUM_PATTERN = re.compile(
    r"(?<![0-9.])(?:"
    r"\d+(?:\.\d+)?%"
    r"|\d+\.\d+"
    r"|\d{2,}"
    r"|\d(?=\s*(?:h|hr|hrs|d|wk|mg|ug|mcg|ml|iu|mmhg|cm|mm)(?![a-zA-Z])|\s*(?:小時|天|週|月|年|分|歲|劑))"
    r")(?![0-9.])",
    re.IGNORECASE,
)

# Capture AHA/TSGS Class of Recommendation tokens (e.g., COR 1, COR 2a, COR 3, Class IIb)
COR_PATTERN = re.compile(r"\b(?:COR|Class)\s*(1|2a|2b|3|I{1,3}[ab]?)\b", re.IGNORECASE)

# Strip hex color strings like #1e293b or #fff from visual text
HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")

# Keys in visual_data that carry styling/layout metadata rather than slide text
NON_CONTENT_KEYS = {
    "id",
    "type",
    "layout",
    "color",
    "colors",
    "fill",
    "stroke",
    "bg",
    "background",
    "width",
    "height",
    "x",
    "y",
    "rx",
    "ry",
    "fontsize",
    "font_size",
    "style",
    "class",
    "classname",
    "viewbox",
    "icon",
}


def normalize_text(text: str) -> str:
    if not text:
        return ""
    s = text.replace("\u2212", "-")  # Unicode minus -> ASCII hyphen
    s = HEX_COLOR_RE.sub(" ", s)
    # Iteratively strip thousand separators (handles 1,234,567)
    while True:
        new_s = COMMA_IN_NUM_RE.sub("", s)
        if new_s == s:
            break
        s = new_s
    return s


def extract_numbers(text: str) -> set:
    norm = normalize_text(text)
    nums = set()
    for m in NUM_PATTERN.finditer(norm):
        token = m.group(0)
        # Keep percentage distinct and also record bare numeric value so "35%" matches "35%" or "35"
        nums.add(token)
        if token.endswith("%"):
            nums.add(token[:-1])
    return nums


def extract_strict_numbers(text: str) -> set:
    """Extract raw matched numeric tokens from a slide (without expanding % to bare)."""
    norm = normalize_text(text)
    return {m.group(0) for m in NUM_PATTERN.finditer(norm)}


def normalize_cor_level(raw: str) -> str:
    val = raw.strip().lower()
    roman_map = {"i": "1", "iia": "2a", "iib": "2b", "iii": "3"}
    return roman_map.get(val, val)


def extract_cor_levels(text: str) -> set:
    return {normalize_cor_level(m.group(1)) for m in COR_PATTERN.finditer(text or "")}


def extract_visual_text(obj) -> str:
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, list):
        return " ".join(extract_visual_text(item) for item in obj)
    if isinstance(obj, dict):
        parts = []
        for k, v in obj.items():
            if str(k).strip().lower() in NON_CONTENT_KEYS:
                continue
            parts.append(extract_visual_text(v))
        return " ".join(parts)
    return ""


def parse_page_num(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return val


def main():
    if len(sys.argv) < 4:
        print(
            json.dumps(
                {
                    "gate": "fidelity",
                    "passed": False,
                    "error": "用法: gate2_fidelity.py <02_evidence_cards.json> <05_slides_draft.json> <05b_semantic_audit.json>",
                },
                ensure_ascii=False,
            )
        )
        sys.exit(1)

    cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    slides = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    audits = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))

    card_map = {str(c["id"]): c for c in cards if "id" in c}
    audit_map = {parse_page_num(a.get("page")): a for a in audits}
    failed_pages = []

    for slide in slides:
        page = parse_page_num(slide.get("page"))
        slide_type = str(slide.get("type", "content")).strip().lower()

        # Cover pages are exempt from clinical grounding checks
        if slide_type == "cover":
            continue

        slide_text = " ".join(
            [
                str(slide.get("title", "")),
                " ".join(str(b) for b in (slide.get("bullets") or [])),
                extract_visual_text(slide.get("visual_data")),
            ]
        )

        # Pure divider section slides without clinical content or numbers are exempt
        if slide_type == "section" and not slide.get("bullets") and not slide.get("visual_data") and not extract_strict_numbers(slide_text):
            continue

        ev_ids = [str(eid) for eid in (slide.get("evidence_ids") or [])]
        issues = []

        # 1. Citation IDs & footer checks
        if not ev_ids:
            issues.append("[程式] 本頁（content/summary）缺少 evidence_ids 引用")
        invalid_ids = [eid for eid in ev_ids if eid not in card_map]
        if invalid_ids:
            issues.append(f"[程式] 引用了不存在的證據卡 ID：{invalid_ids}")

        if slide_type == "content" and not str(slide.get("citation_footer", "")).strip():
            issues.append("[程式] 內容頁缺少頁尾出處（citation_footer 為空）")

        # 2. Numeric & COR/LOE grounding against cited evidence cards
        valid_ev_text = " ".join(
            " ".join(
                [
                    str(card_map[eid].get("claim", "")),
                    str(card_map[eid].get("quote", "")),
                    str(card_map[eid].get("citation", "")),
                    str(card_map[eid].get("cor_loe", "")),
                ]
            )
            for eid in ev_ids
            if eid in card_map
        )

        ev_numbers = extract_numbers(valid_ev_text)
        slide_numbers = extract_strict_numbers(slide_text)
        ungrounded_nums = sorted(
            n for n in slide_numbers if n not in ev_numbers and (n.rstrip("%") not in ev_numbers)
        )
        if ungrounded_nums:
            issues.append(f"[程式] 以下數值未出現在所引用的證據卡中：{ungrounded_nums}")

        ev_cors = extract_cor_levels(valid_ev_text)
        slide_cors = extract_cor_levels(slide_text)
        ungrounded_cors = sorted(slide_cors - ev_cors)
        if ungrounded_cors:
            issues.append(f"[程式] 以下建議等級（COR/Class）未出現在所引用的證據卡中：{ungrounded_cors}")

        # 3. AI semantic audit verification
        audit = audit_map.get(page)
        if audit is None:
            issues.append("[AI審查] 缺少本頁的語意忠實度審查紀錄")
        elif not audit.get("passed", False):
            for ai_issue in audit.get("issues") or ["語意審查未通過"]:
                issues.append(f"[AI審查] {ai_issue}")

        if issues:
            failed_pages.append({"page": page, "type": slide_type, "issues": issues})

    passed = len(failed_pages) == 0
    report = {
        "gate": "fidelity",
        "passed": passed,
        "checked_slides": len([s for s in slides if str(s.get("type", "content")).lower() != "cover"]),
        "failed_pages": failed_pages,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
