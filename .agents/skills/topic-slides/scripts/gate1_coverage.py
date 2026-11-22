#!/usr/bin/env python3
"""Gate 1: Coverage, real-file existence, superseded-status guard, and citation check."""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_MIN_DOCS = 2
DEFAULT_MIN_CHARS = 800
DEFAULT_MIN_KEYWORD_RATIO = 0.7

TABLE_SEP_RE = re.compile(r"^\s*\|?(?:\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?\s*$", re.M)
FM_RE = re.compile(r"^---\n(.*?)\n---", re.S)
STATUS_RE = re.compile(r"^status:\s*[\"']?([a-zA-Z0-9_-]+)[\"']?\s*$", re.M)


def effective_char_count(text: str) -> int:
    cleaned = TABLE_SEP_RE.sub("", text)
    cleaned = re.sub(r"\s+", "", cleaned)
    return len(cleaned)


def check_frontmatter_status(file_path: Path) -> str:
    try:
        raw = file_path.read_text(encoding="utf-8")
    except OSError:
        return "unreadable"
    m = FM_RE.match(raw)
    if not m:
        return "unknown"
    sm = STATUS_RE.search(m.group(1))
    return sm.group(1).lower() if sm else "unknown"


def keyword_matched(kw_spec, full_text_lower: str) -> bool:
    if isinstance(kw_spec, list):
        variants = [str(v).strip().lower() for v in kw_spec if str(v).strip()]
    else:
        variants = [v.strip().lower() for v in str(kw_spec).split("|") if v.strip()]
    if not variants:
        return True
    return any(v in full_text_lower for v in variants)


def main():
    parser = argparse.ArgumentParser(description="Gate 1: Wiki retrieval coverage and provenance check")
    parser.add_argument("retrieved_json", help="Path to 01_retrieved.json")
    parser.add_argument("--workspace", default=".", help="Workspace root directory for verifying doc paths")
    parser.add_argument("--min-docs", type=int, default=DEFAULT_MIN_DOCS)
    parser.add_argument("--min-chars", type=int, default=DEFAULT_MIN_CHARS)
    parser.add_argument("--min-kw-ratio", type=float, default=DEFAULT_MIN_KEYWORD_RATIO)
    args = parser.parse_args()

    json_path = Path(args.retrieved_json)
    if not json_path.exists():
        print(json.dumps({"gate": "coverage", "passed": False, "error": f"找不到檔案: {json_path}"}, ensure_ascii=False))
        sys.exit(1)

    workspace = Path(args.workspace).resolve()
    data = json.loads(json_path.read_text(encoding="utf-8"))
    docs = data.get("docs", [])
    keywords = data.get("required_keywords", [])

    full_text = "\n".join(f"{d.get('title', '')}\n{d.get('content', '')}" for d in docs)
    full_text_lower = full_text.lower()
    total_chars = effective_char_count(full_text)

    reasons = []
    if len(docs) < args.min_docs:
        reasons.append(f"檢索篇數不足：{len(docs)} 篇（門檻：{args.min_docs} 篇）")
    if total_chars < args.min_chars:
        reasons.append(f"有效資料字數不足：{total_chars} 字（門檻：{args.min_chars} 字）")

    missing_kw = [kw for kw in keywords if not keyword_matched(kw, full_text_lower)]
    kw_ratio = 1.0
    if keywords:
        kw_ratio = (len(keywords) - len(missing_kw)) / len(keywords)
        if kw_ratio < args.min_kw_ratio:
            reasons.append(f"關鍵字覆蓋率不足（{kw_ratio:.0%}，門檻 {args.min_kw_ratio:.0%}），缺少：{missing_kw}")

    missing_files = []
    superseded_docs = []
    docs_without_citations = []

    for d in docs:
        doc_label = d.get("path") or d.get("id") or "<unknown>"
        raw_path = d.get("path", "").strip()
        if not raw_path:
            missing_files.append(doc_label)
        else:
            resolved = (workspace / raw_path).resolve()
            if not resolved.exists() or not resolved.is_file():
                missing_files.append(raw_path)
            else:
                fm_status = check_frontmatter_status(resolved)
                if fm_status == "superseded" and not d.get("historical_context", False):
                    superseded_docs.append(raw_path)

        citations = [str(c).strip() for c in (d.get("citations") or []) if str(c).strip()]
        if not citations:
            docs_without_citations.append(doc_label)

    if missing_files:
        reasons.append(f"以下 Wiki 檔案路徑不存在於工作區（疑似錯誤或幻覺路徑）：{missing_files}")
    if superseded_docs:
        reasons.append(
            f"以下檔案標記為 status: superseded（已取代舊版指引），請改用新版指引或明標 historical_context=true：{superseded_docs}"
        )
    if docs_without_citations:
        reasons.append(f"以下 Wiki 檔案未擷取到文獻出處（citations 為空）：{docs_without_citations}")

    passed = len(reasons) == 0
    report = {
        "gate": "coverage",
        "passed": passed,
        "doc_count": len(docs),
        "effective_chars": total_chars,
        "keyword_ratio": round(kw_ratio, 3),
        "missing_keywords": missing_kw,
        "missing_files": missing_files,
        "superseded_docs": superseded_docs,
        "docs_without_citations": docs_without_citations,
        "reasons": reasons,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
