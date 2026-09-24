#!/usr/bin/env python3
"""Extract subtitle text from an SRT file into a plain .txt file.

Drops the sequence index and timestamp lines, merges multi-line subtitles
into a single line, and strips HTML-style and ASS/SSA override tags.
Output blocks are separated by a blank line.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HTML_TAG_RE = re.compile(r"<[^>]+>")
ASS_TAG_RE = re.compile(r"\{[^}]*\}")
TIMESTAMP_RE = re.compile(
    r"^\d{1,2}:\d{2}:\d{2}[,.]\d{1,3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[,.]\d{1,3}"
)


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "utf-16", "gbk", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace")


def extract_blocks(content: str) -> list[str]:
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    raw_blocks = re.split(r"\n\s*\n", content.strip())

    out: list[str] = []
    for block in raw_blocks:
        lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
        if not lines:
            continue
        if lines[0].isdigit():
            lines = lines[1:]
        if lines and TIMESTAMP_RE.match(lines[0]):
            lines = lines[1:]
        if not lines:
            continue
        text = " ".join(lines)
        text = HTML_TAG_RE.sub("", text)
        text = ASS_TAG_RE.sub("", text)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            out.append(text)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Input .srt file")
    parser.add_argument(
        "-o",
        "--output",
        help="Output .txt file (default: same directory and base name as input, .txt extension)",
    )
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.is_file():
        print(f"error: input file not found: {in_path}", file=sys.stderr)
        return 1

    out_path = Path(args.output) if args.output else in_path.with_suffix(".txt")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    content = read_text(in_path)
    blocks = extract_blocks(content)
    out_path.write_text("\n\n".join(blocks) + ("\n" if blocks else ""), encoding="utf-8")
    print(f"Extracted {len(blocks)} subtitle blocks to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
