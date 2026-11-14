#!/usr/bin/env python3
"""Build the redistributable LilyPatch font family.

Only font metadata changes; every glyph outline and every advance is kept
byte-for-byte from the upstream font.

Priority order is part of the manifest: WenYuan Sans SC, Source Han Sans SC,
Glow Sans SC. Sarasa Gothic is intentionally not shipped: its CJK glyphs are
almost identical to Source Han Sans.

For each font the changes are:
  * hhea / OS/2 typo / OS/2 win ascent+descent normalized to 880/-120 so a
    32 px GDI cell gives ~28 px ascent and 32 px full-width advance;
  * GB2312 and GBK code-page bits set so lfCharSet=134 selects it;
  * family / full / PostScript names changed to LilyPatch names, avoiding the
    upstream Reserved Font Names;
  * reproducible head.modified.

Inputs are downloaded into upstream/ and are not committed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from fontTools.ttLib import TTFont

# Order is the user-facing priority: WenYuan > Source Han > Glow.
TARGETS = [
    {
        "id": "wenyuan",
        "display_zh": "文源黑体（LilyPatch）",
        "features_zh": "基于思源优化，笔画更均匀",
        "input": "WenYuanSansSC-Regular.ttf",
        "output": "LilyPatchWenYuanSC-Regular.ttf",
        "family": "LilyPatch WenYuan Sans SC",
        "full": "LilyPatch WenYuan Sans SC Regular",
        "postscript": "LilyPatchWenYuanSC-Regular",
        "unique": "LilyPatch WenYuan Sans SC Regular 1.110;LPAT",
        "version": "Version 1.110;LilyPatch",
        "license": "LICENSE-WenYuan-OFL-1.1.txt",
    },
    {
        "id": "sans",
        "display_zh": "思源黑体（LilyPatch）",
        "features_zh": "标准思源黑体，字形规范",
        "input": "SourceHanSansSC-Regular.ttf",
        "output": "LilyPatchSansSC-Regular.ttf",
        "family": "LilyPatch Sans SC",
        "full": "LilyPatch Sans SC Regular",
        "postscript": "LilyPatchSansSC-Regular",
        "unique": "LilyPatch Sans SC Regular 2.005;LPAT",
        "version": "Version 2.005;LilyPatch",
        "license": "LICENSE-OFL-1.1.txt",
    },
    {
        "id": "glow",
        "display_zh": "未来荧黑（LilyPatch）",
        "features_zh": "更轻、更几何的现代黑体",
        "input": "GlowSansSC-Normal-Regular.otf",
        "output": "LilyPatchGlowSansSC-Regular.otf",
        "family": "LilyPatch Glow Sans SC",
        "full": "LilyPatch Glow Sans SC Regular",
        "postscript": "LilyPatchGlowSansSC-Regular",
        "unique": "LilyPatch Glow Sans SC Regular 0.93;LPAT",
        "version": "Version 0.93;LilyPatch",
        "license": "LICENSE-Glow-OFL-1.1.txt",
        # U+266A is drawn by the shared music-room note font; U+2500 is not
        # used by current translations after the TH07 dash correction.
        "allowed_missing": ["U+2500", "U+266A"],
    },
]


def set_name_records(font: TTFont, target: dict[str, str]) -> None:
    replacements = {
        1: target["family"],
        3: target["unique"],
        4: target["full"],
        5: target["version"],
        6: target["postscript"],
        16: target["family"],
        17: "Regular",
        18: target["full"],
        21: target["family"],
        22: "Regular",
    }
    for record in font["name"].names:
        if record.nameID in replacements:
            record.string = replacements[record.nameID]


def build(target: dict[str, str], input_path: Path, output_path: Path) -> None:
    font = TTFont(input_path)
    os2 = font["OS/2"]
    hhea = font["hhea"]

    # Upstreams use their own vertical metrics (commonly 1160/-288 or
    # 1000-scale equivalents). 880/-120 gives 28/4 px in a 32 px cell.
    hhea.ascent = 880
    hhea.descent = -120
    hhea.lineGap = 0
    os2.sTypoAscender = 880
    os2.sTypoDescender = -120
    os2.sTypoLineGap = 0
    os2.usWinAscent = 880
    os2.usWinDescent = 120
    os2.ulCodePageRange1 |= 0x40000  # GB2312
    os2.ulCodePageRange1 |= 0x80000  # GBK
    os2.achVendID = "LPAT"

    set_name_records(font, target)

    # Keep the build reproducible: fontTools otherwise stamps head.modified
    # with the current time, changing the file hash on every run.
    font["head"].modified = 0
    font.recalcTimestamp = False
    output_path.parent.mkdir(parents=True, exist_ok=True)
    font.save(output_path)


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, default=root / "upstream")
    parser.add_argument("--output", type=Path, default=root / "fonts")
    parser.add_argument(
        "--manifest", type=Path, default=root / "fonts" / "manifest.json"
    )
    args = parser.parse_args()

    items = []
    for target in TARGETS:
        src = args.upstream / target["input"]
        dst = args.output / target["output"]
        if not src.exists():
            raise SystemExit(f"missing upstream font: {src}")
        build(target, src, dst)
        item = {
            "id": target["id"],
            "display_zh": target["display_zh"],
            "features_zh": target["features_zh"],
            "input": target["input"],
            "output": target["output"],
            "family": target["family"],
            "postscript": target["postscript"],
            "format": "OTF" if dst.suffix.lower() == ".otf" else "TTF",
            "bytes": dst.stat().st_size,
            "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(),
            "license": target["license"],
        }
        if target.get("allowed_missing"):
            item["allowed_missing"] = target["allowed_missing"]
        items.append(item)
        print(f"{item['output']}  {item['bytes']} bytes  {item['sha256']}")

    manifest = {"order": [item["id"] for item in items], "fonts": items}
    args.manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
