#!/usr/bin/env python3
"""Gate 3: 16:9 overflow (flex/grid-safe), SVG/image integrity, and strict offline check."""

import argparse
import json
import re
import sys
from pathlib import Path

OVERFLOW_TOLERANCE_PX = 2
MINOR_OVERFLOW_PX = 40

# Static scan patterns for external resources (ignores XML namespaces like xmlns="http://www.w3.org/2000/svg")
EXTERNAL_ATTR_RE = re.compile(
    r"""<(?:script|link|img|iframe|source|video|audio|embed|object)\b[^>]*?\b(?:src|href|data)\s*=\s*["']((?:https?:)?//[^"']+)["']""",
    re.IGNORECASE,
)
EXTERNAL_CSS_URL_RE = re.compile(
    r"""(?:@import\s+(?:url\()?["']?|url\(\s*["']?)((?:https?:)?//[^)"'\s]+)""",
    re.IGNORECASE,
)
SLIDE_TAG_RE = re.compile(r"""<section\b[^>]*class\s*=\s*["'][^"']*\bslide\b[^"']*["']""", re.IGNORECASE)


def static_scan(html_text: str):
    violations = set()
    for m in EXTERNAL_ATTR_RE.finditer(html_text):
        violations.add(m.group(1))
    for m in EXTERNAL_CSS_URL_RE.finditer(html_text):
        violations.add(m.group(1))
    slide_count = len(SLIDE_TAG_RE.findall(html_text))
    return sorted(violations), slide_count


def main():
    parser = argparse.ArgumentParser(description="Gate 3: HTML slide render and offline compliance check")
    parser.add_argument("html_path", help="待檢查的 HTML 檔案路徑")
    parser.add_argument("--state", help="state.json 路徑，用於判斷該頁是否已做過 CSS 微調", default=None)
    parser.add_argument("--static-only", action="store_true", help="僅執行靜態離線與結構檢查（不啟動 Chromium）")
    args = parser.parse_args()

    html_path = Path(args.html_path).resolve()
    if not html_path.exists():
        print(json.dumps({"gate": "render", "passed": False, "error": f"找不到檔案: {html_path}"}, ensure_ascii=False))
        sys.exit(1)

    html_text = html_path.read_text(encoding="utf-8")
    static_violations, static_slide_count = static_scan(html_text)

    if args.static_only:
        html_fix_pages = []
        if static_slide_count == 0:
            html_fix_pages.append({"page": 0, "issues": ["找不到任何 <section class='slide'> 元素"]})
        if static_violations:
            html_fix_pages.append({"page": 0, "issues": [f"違反離線規範（靜態掃描），包含外部資源：{static_violations}"]})
        passed = len(html_fix_pages) == 0
        report = {
            "gate": "render",
            "mode": "static_only",
            "passed": passed,
            "routing_action": "deliver" if passed else "fix_html",
            "total_slides": static_slide_count,
            "css_tweak_pages": [],
            "html_fix_pages": html_fix_pages,
            "failed_pages": [],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(0 if passed else 1)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            json.dumps(
                {
                    "gate": "render",
                    "passed": False,
                    "error": "未安裝 playwright。請執行 `pip3 install playwright && playwright install chromium`，或暫時加上 `--static-only` 執行靜態檢查。",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)

    tweaked_pages = set()
    if args.state and Path(args.state).exists():
        state = json.loads(Path(args.state).read_text(encoding="utf-8"))
        tweaked_pages = {int(p) for p in state.get("css_tweaked_pages", [])}

    console_errors = []
    runtime_offline_violations = set(static_violations)
    css_tweak_pages = []
    html_fix_pages = []
    revise_draft_pages = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.on("pageerror", lambda err: console_errors.append(f"pageerror: {err}"))
        page.on("console", lambda msg: console_errors.append(f"console.error: {msg.text}") if msg.type == "error" else None)

        # Strictly block and record any external http/https network request (true offline test)
        def handle_route(route):
            url = route.request.url
            if url.startswith(("file://", "data:", "blob:")):
                route.continue_()
            else:
                runtime_offline_violations.add(url)
                route.abort()

        page.route("**/*", handle_route)
        page.goto(html_path.as_uri(), wait_until="load")
        page.wait_for_timeout(150)

        # Measure each slide by activating .active class (preserves display:flex / display:grid!)
        slides_info = page.evaluate(
            """(tol) => {
                const slides = Array.from(document.querySelectorAll('section.slide'));
                const saved = slides.map(el => ({
                    el,
                    className: el.className,
                    inlineDisplay: el.style.display,
                    inlineVisibility: el.style.visibility,
                    inlinePosition: el.style.position
                }));

                const results = slides.map((el, idx) => {
                    // Activate only target slide using .active class
                    slides.forEach(s => {
                        s.classList.remove('active');
                        if (s !== el) s.style.display = 'none';
                    });
                    el.style.display = '';
                    el.style.visibility = 'visible';
                    el.classList.add('active');

                    let forcedFallback = false;
                    if (getComputedStyle(el).display === 'none') {
                        el.style.display = 'flex';
                        forcedFallback = true;
                    }

                    const scrollOverflowY = Math.round(el.scrollHeight - el.clientHeight);
                    const scrollOverflowX = Math.round(el.scrollWidth - el.clientWidth);

                    // Also detect visible children overflowing slide bounds (even if overflow:hidden clips them)
                    const slideRect = el.getBoundingClientRect();
                    let childOverflowY = 0;
                    let childOverflowX = 0;
                    const descendants = el.querySelectorAll('*');
                    for (const child of descendants) {
                        if (
                            child.getAttribute('aria-hidden') === 'true' ||
                            child.dataset.decorative === 'true' ||
                            child.closest('[aria-hidden="true"], [data-decorative="true"]')
                        ) {
                            continue;
                        }
                        // Skip internal SVG primitives (check outer <svg> box instead)
                        if (child instanceof SVGElement && child.tagName.toLowerCase() !== 'svg') {
                            continue;
                        }
                        const cs = getComputedStyle(child);
                        if (cs.display === 'none' || cs.visibility === 'hidden' || Number(cs.opacity) === 0) {
                            continue;
                        }
                        const r = child.getBoundingClientRect();
                        if (r.width === 0 && r.height === 0) continue;
                        const dy = Math.round(r.bottom - slideRect.bottom);
                        const dx = Math.round(r.right - slideRect.right);
                        if (dy > childOverflowY) childOverflowY = dy;
                        if (dx > childOverflowX) childOverflowX = dx;
                    }

                    const overflowY = Math.max(scrollOverflowY, childOverflowY);
                    const overflowX = Math.max(scrollOverflowX, childOverflowX);

                    const brokenImgs = Array.from(el.querySelectorAll('img'))
                        .filter(img => !img.complete || img.naturalWidth === 0)
                        .map(img => img.getAttribute('src'));

                    const emptySvgs = Array.from(el.querySelectorAll('svg'))
                        .filter(svg => {
                            const rect = svg.getBoundingClientRect();
                            return rect.width === 0 || rect.height === 0;
                        }).length;

                    return {
                        page: Number(el.dataset.page || (idx + 1)),
                        computedDisplay: getComputedStyle(el).display,
                        forcedFallback,
                        overflowY,
                        overflowX,
                        brokenImgs,
                        emptySvgs,
                        hasOverflow: overflowY > tol || overflowX > tol
                    };
                });

                // Restore initial DOM state
                saved.forEach(({ el, className, inlineDisplay, inlineVisibility, inlinePosition }) => {
                    el.className = className;
                    el.style.display = inlineDisplay;
                    el.style.visibility = inlineVisibility;
                    el.style.position = inlinePosition;
                });

                return results;
            }""",
            OVERFLOW_TOLERANCE_PX,
        )

        browser.close()

    if not slides_info:
        html_fix_pages.append({"page": 0, "issues": ["找不到任何 <section class='slide'> 元素"]})
    else:
        for s in slides_info:
            page_num = int(s["page"])
            draft_issues = []
            html_issues = []
            minor_css_issues = []

            if s["hasOverflow"]:
                is_minor = s["overflowY"] <= MINOR_OVERFLOW_PX and s["overflowX"] <= OVERFLOW_TOLERANCE_PX
                if is_minor and page_num not in tweaked_pages:
                    minor_css_issues.append(f"微幅高度溢出 {s['overflowY']}px（建議微調本頁 CSS padding/行高一次）")
                else:
                    reason = "已微調過 CSS 仍溢出" if page_num in tweaked_pages else "溢出幅度過大或水平溢出"
                    draft_issues.append(
                        f"{reason}（高+{s['overflowY']}px、寬+{s['overflowX']}px），請退回逐頁稿精簡或拆頁"
                    )

            if s["brokenImgs"]:
                html_issues.append(f"圖片載入失敗：{s['brokenImgs']}")
            if s["emptySvgs"] > 0:
                html_issues.append(f"偵測到 {s['emptySvgs']} 個未正確繪製的空白 SVG")

            if draft_issues:
                revise_draft_pages.append({"page": page_num, "issues": draft_issues + html_issues})
            else:
                if minor_css_issues:
                    css_tweak_pages.append({"page": page_num, "issues": minor_css_issues})
                if html_issues:
                    html_fix_pages.append({"page": page_num, "issues": html_issues})

    if console_errors:
        html_fix_pages.append({"page": 0, "issues": [f"JS／Console 錯誤：{console_errors}"]})
    if runtime_offline_violations:
        html_fix_pages.append(
            {"page": 0, "issues": [f"違反離線規範，包含外部資源：{sorted(runtime_offline_violations)}"]}
        )

    passed = not css_tweak_pages and not html_fix_pages and not revise_draft_pages
    if passed:
        routing_action = "deliver"
    elif revise_draft_pages:
        routing_action = "revise_draft"
    else:
        routing_action = "fix_html"

    report = {
        "gate": "render",
        "mode": "playwright",
        "passed": passed,
        "routing_action": routing_action,
        "total_slides": len(slides_info),
        "css_tweak_pages": css_tweak_pages,
        "html_fix_pages": html_fix_pages,
        "failed_pages": revise_draft_pages,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
