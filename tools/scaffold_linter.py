#!/usr/bin/env python3
"""
mAIntAIn Styles scaffold linter.
Checks fixed house rules against a client's site folder:
  1. .btn / .btn-* / .mobile-order-btn / .mobile-call-btn border-radius == 7px
     (also catches compound selectors like ".nav-cta .btn" - fixed 2026-08-03,
     a real .nav-cta .btn{border-radius:6px} rule slipped past the old regex)
  2. .hero-frame is 340px square (width:340px + height:340px OR aspect-ratio:1/1)
  3. No "pulse" animation referenced anywhere (keyframes or animation property)

Usage: python scaffold_linter.py /path/to/client/site
Exit 0 = clean pass (prints files/rules checked). Exit 1 = violations found.
"""
import sys
import re
from pathlib import Path

CANONICAL_RADIUS = 7
CANONICAL_SIZE = 340

BTN_RULE_RE = re.compile(
    r'(?P<selector>[^{}]*?\.(?:btn(?:-[a-zA-Z0-9_-]+)?|mobile-(?:order|call)-btn)(?:\s*[,:][^{}]*)?\s*\{)(?P<decl>[^}]*)\}',
    re.DOTALL | re.IGNORECASE
)
RADIUS_RE = re.compile(r'border-radius\s*:\s*(\d+(?:\.\d+)?)\s*px', re.IGNORECASE)

HERO_FRAME_RE = re.compile(r'\.hero-frame\s*\{(?P<decl>[^}]*)\}', re.DOTALL | re.IGNORECASE)
WIDTH_RE = re.compile(r'width\s*:\s*(\d+(?:\.\d+)?)\s*px', re.IGNORECASE)
HEIGHT_RE = re.compile(r'height\s*:\s*(\d+(?:\.\d+)?)\s*px', re.IGNORECASE)
ASPECT_RE = re.compile(r'aspect-ratio\s*:\s*1\s*/\s*1', re.IGNORECASE)

PULSE_RE = re.compile(r'pulse', re.IGNORECASE)


def get_style_blocks(html_path: Path):
    try:
        content = html_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return [], f"ERROR reading {html_path}: {e}"
    blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
    return blocks, None


def check_btn_radius(html_path: Path, blocks):
    issues, checked = [], 0
    for block in blocks:
        for m in BTN_RULE_RE.finditer(block):
            selector = m.group('selector').strip()
            decl = m.group('decl')
            rm = RADIUS_RE.search(decl)
            if rm:
                checked += 1
                val = float(rm.group(1))
                if abs(val - CANONICAL_RADIUS) > 1e-9:
                    issues.append(f"{html_path}: {selector} border-radius {val}px (expected {CANONICAL_RADIUS}px)")
    return issues, checked


def check_hero_frame(html_path: Path, blocks):
    issues, checked = [], 0
    for block in blocks:
        for m in HERO_FRAME_RE.finditer(block):
            decl = m.group('decl')
            checked += 1
            wm = WIDTH_RE.search(decl)
            has_width = wm and abs(float(wm.group(1)) - CANONICAL_SIZE) < 1e-9
            hm = HEIGHT_RE.search(decl)
            has_height = hm and abs(float(hm.group(1)) - CANONICAL_SIZE) < 1e-9
            has_aspect = bool(ASPECT_RE.search(decl))
            if not has_width:
                issues.append(f"{html_path}: .hero-frame missing width:{CANONICAL_SIZE}px")
            if not (has_height or has_aspect):
                issues.append(f"{html_path}: .hero-frame missing height:{CANONICAL_SIZE}px or aspect-ratio:1/1")
    return issues, checked


def check_no_pulse(html_path: Path, blocks):
    issues = []
    for block in blocks:
        if PULSE_RE.search(block):
            for m in PULSE_RE.finditer(block):
                snippet = block[max(0, m.start()-30):m.start()+30].replace('\n', ' ')
                issues.append(f"{html_path}: 'pulse' reference found: ...{snippet}...")
    return issues


def main():
    if len(sys.argv) != 2:
        print("Usage: python scaffold_linter.py <client-site-folder>")
        sys.exit(1)
    site_dir = Path(sys.argv[1])
    if not site_dir.is_dir():
        print(f"Error: {site_dir} is not a directory")
        sys.exit(1)

    # Admin Styles is a separate internal tool with its own design rules — not the public site
    html_files = [f for f in site_dir.rglob('*.html') if 'admin_styles' not in f.name.lower()]
    if not html_files:
        print("No HTML files found.")
        sys.exit(0)

    all_issues = []
    btn_checked = 0
    hero_checked = 0
    files_with_style = 0

    for f in html_files:
        blocks, err = get_style_blocks(f)
        if err:
            print(err)
            continue
        if not blocks:
            continue
        files_with_style += 1
        issues, n = check_btn_radius(f, blocks)
        all_issues.extend(issues)
        btn_checked += n
        issues, n = check_hero_frame(f, blocks)
        all_issues.extend(issues)
        hero_checked += n
        all_issues.extend(check_no_pulse(f, blocks))

    if all_issues:
        print("Scaffold rule violations found:")
        for line in all_issues:
            print(" ", line)
        print()
        print(f"({files_with_style} files with <style> blocks scanned, "
              f"{btn_checked} button rules checked, {hero_checked} hero-frame rules checked)")
        sys.exit(1)
    else:
        print(f"All scaffold rules pass. {files_with_style} files with <style> blocks scanned, "
              f"{btn_checked} button rules checked, {hero_checked} hero-frame rules checked.")
        sys.exit(0)


if __name__ == '__main__':
    main()
