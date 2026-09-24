---
name: srt-to-text
description: Extract subtitle text from SRT subtitle files into plain .txt files, stripping the indices, timestamps, and formatting tags so only the dialogue remains. Use this skill whenever the user wants to extract content from a subtitle file (.srt), pull the text out of subtitles, save subtitle content to a txt file, or convert subtitles to plain text — even if they don't say "SRT" explicitly. Phrases like "把字幕内容提取出来", "extract subtitles", "get the dialogue from this .srt" should all trigger it.
---

# SRT to Text

Extract just the dialogue from an SRT subtitle file and save it as plain text. Each subtitle block becomes one paragraph in the output, separated by a blank line.

## When to use

The user has an `.srt` file (or several) and wants the *text content* — without the sequence numbers, timestamps, or styling tags. Common phrasings:

- "extract the subtitles from this srt file"
- "把这个字幕文件的内容提取出来"
- "save the subtitle text to a txt file"
- "convert this srt to plain text"
- "get just the dialogue from movie.srt"

If the user gives you a path that ends in `.srt` and asks for "content", "text", or "dialogue", that's the signal.

## How to do it

Run the bundled script. It is the source of truth — don't reimplement the parsing inline, because edge cases (encoding detection, ASS-style override tags, mixed line endings) are easy to miss and the script already handles them.

```bash
python3 <skill-dir>/scripts/extract.py <input.srt> [-o <output.txt>]
```

`<skill-dir>` is the directory containing this SKILL.md.

**Default output path**: same directory as the input, same base name, `.txt` extension. Only pass `-o` if the user specified a different output location or filename.

**Multiple files**: if the user wants several SRTs converted, run the script once per file. The script intentionally takes a single file so that errors on one file don't silently skip others.

## What the script handles

- Multi-line subtitles within a block — merged into one line with spaces between
- HTML-style tags (`<i>`, `<b>`, `<font color="red">`, etc.) — stripped
- ASS/SSA override tags (`{\an8}`, `{\pos(...)}`, etc.) — stripped
- UTF-8 (with/without BOM), UTF-16, GBK, Windows-1252 — auto-detected
- `,` or `.` as the millisecond separator in timestamps
- CRLF, LF, or CR line endings

## After running

The script prints the output path and the number of subtitle blocks extracted. Pass that information along to the user so they know where the file landed and roughly how much was captured.

## Edge cases worth flagging

- **Wrong format**: if the file is `.vtt`, `.ass`, or `.ssa` rather than `.srt`, the script may still produce something but it won't be reliable. Tell the user and ask whether they want a different approach.
- **Existing output**: the script overwrites the destination silently. If you can see that the target `.txt` already exists and looks like real content, mention it before running so the user can rename or back it up.
- **Non-existent input**: the script exits with an error message; relay that to the user rather than retrying blindly.
