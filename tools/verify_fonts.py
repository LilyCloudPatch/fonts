#!/usr/bin/env python3
"""Verify generated LilyPatch fonts without changing them."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"
MANIFEST = FONTS / "manifest.json"


def check_one(item: dict) -> list[str]:
    path = FONTS / item["output"]
    problems: list[str] = []
    if not path.exists():
        return [f"{path}: missing"]
    font = TTFont(path, lazy=True)
    os2 = font["OS/2"]
    hhea = font["hhea"]
    if font["name"].getDebugName(1) != item["family"]:
        problems.append(f"{path.name}: family={font['name'].getDebugName(1)!r}")
    if font["name"].getDebugName(6) != item["postscript"]:
        problems.append(f"{path.name}: postscript={font['name'].getDebugName(6)!r}")
    if hhea.ascent != 880 or hhea.descent != -120 or hhea.lineGap != 0:
        problems.append(f"{path.name}: hhea={hhea.ascent}/{hhea.descent}/{hhea.lineGap}")
    if os2.usWinAscent != 880 or os2.usWinDescent != 120:
        problems.append(f"{path.name}: win={os2.usWinAscent}/{os2.usWinDescent}")
    if os2.sTypoAscender != 880 or os2.sTypoDescender != -120:
        problems.append(f"{path.name}: typo={os2.sTypoAscender}/{os2.sTypoDescender}")
    if not (os2.ulCodePageRange1 & 0x40000):
        problems.append(f"{path.name}: GB2312 code-page bit missing")
    if not (os2.ulCodePageRange1 & 0x80000):
        problems.append(f"{path.name}: GBK code-page bit missing")
    if os2.fsType != 0:
        problems.append(f"{path.name}: fsType={os2.fsType}")
    if path.stat().st_size != item["bytes"]:
        problems.append(f"{path.name}: size {path.stat().st_size} != {item['bytes']}")
    cmap = font.getBestCmap()
    print(
        f"{item['id']}: {path.name} {path.stat().st_size} bytes, "
        f"glyphs={len(font.getGlyphOrder())}, cmap={len(cmap)}, "
        f"hhea={hhea.ascent}/{hhea.descent}, win={os2.usWinAscent}/{os2.usWinDescent}"
    )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=Path, help="optional UTF-8 text to check")
    args = parser.parse_args()

    if not MANIFEST.exists():
        print("FAIL\n  fonts/manifest.json missing")
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    problems: list[str] = []
    for item in manifest.get("fonts", []):
        problems.extend(check_one(item))

    if args.text:
        chars = {ch for ch in args.text.read_text(encoding="utf-8") if ch not in "\t\n\r"}
        for item in manifest.get("fonts", []):
            cmap = TTFont(FONTS / item["output"], lazy=True).getBestCmap()
            allowed = {int(value[2:], 16) for value in item.get("allowed_missing", [])}
            missing = sorted({ch for ch in chars if ord(ch) not in cmap and ord(ch) not in allowed})
            print(f"{item['id']}: text chars={len(chars)} missing={len(missing)}")
            for ch in missing[:50]:
                print(f"  U+{ord(ch):04X}")
            if missing:
                problems.append(f"{item['id']}: {len(missing)} characters missing")

    if problems:
        print("FAIL")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(f"OK order={','.join(manifest.get('order', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
