from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "yt_dlp is required. Run `py -3.11 -m pip install yt-dlp` and try again."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research" / "manifest.json"
DEFAULT_OUTPUT_DIR = ROOT / "research" / "youtube-transcripts"
DEFAULT_LANGS = ("en-orig", "en")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "video"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def manifest_items() -> list[dict]:
    return load_manifest().get("youtube_videos", [])


def output_stem(item: dict) -> str:
    return f"{slugify(item['expert'])}--{slugify(item['title'])}"


def select_items(items: list[dict], expert: str | None, video_id: str | None) -> list[dict]:
    selected = items

    if expert:
        expert_lower = expert.lower()
        selected = [item for item in selected if item["expert"].lower() == expert_lower]

    if video_id:
        selected = [item for item in selected if item["video_id"] == video_id]

    return selected


def available_auto_captions(url: str) -> dict[str, list[dict]]:
    options = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": False,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
    return info.get("automatic_captions") or {}


def pick_language(captions: dict[str, list[dict]], preferred: tuple[str, ...]) -> str | None:
    for lang in preferred:
        if captions.get(lang):
            return lang
    return None


def download_caption(url: str, output_dir: Path, stem: str, language: str, sub_format: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    template = str(output_dir / f"{stem}.%(ext)s")
    options = {
        "skip_download": True,
        "writeautomaticsub": True,
        "writesubtitles": False,
        "subtitleslangs": [language],
        "subtitlesformat": sub_format,
        "outtmpl": template,
        "quiet": False,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return output_dir / f"{stem}.{language}.{sub_format}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download YouTube automatic captions for videos in research/manifest.json.",
    )
    parser.add_argument(
        "--expert",
        help="Only download captions for a single expert name from the manifest.",
    )
    parser.add_argument(
        "--video-id",
        help="Only download captions for a single YouTube video ID from the manifest.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to write .srt files into. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--sub-format",
        default="srt",
        help="Subtitle format to request from yt-dlp. Default: srt",
    )
    parser.add_argument(
        "--langs",
        default=",".join(DEFAULT_LANGS),
        help="Comma-separated language preference order. Default: en-orig,en",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Only report available automatic caption languages without downloading.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    preferred_langs = tuple(part.strip() for part in args.langs.split(",") if part.strip())
    items = select_items(manifest_items(), args.expert, args.video_id)

    if not items:
        print("No matching videos found in research/manifest.json", file=sys.stderr)
        raise SystemExit(1)

    successes = 0
    failures = 0

    for item in items:
        stem = output_stem(item)
        print(f"\n[{item['expert']}] {item['title']}")
        print(f"URL: {item['url']}")

        try:
            captions = available_auto_captions(item["url"])
        except Exception as exc:  # pragma: no cover - network/tool failure
            failures += 1
            print(f"Failed to inspect captions: {exc}", file=sys.stderr)
            continue

        if not captions:
            failures += 1
            print("No automatic captions found.", file=sys.stderr)
            continue

        available = ", ".join(sorted(captions.keys()))
        print(f"Available auto-captions: {available}")

        language = pick_language(captions, preferred_langs)
        if not language:
            failures += 1
            print(
                f"No preferred language found. Wanted one of: {', '.join(preferred_langs)}",
                file=sys.stderr,
            )
            continue

        print(f"Selected language: {language}")

        if args.list_only:
            successes += 1
            continue

        try:
            output_path = download_caption(
                url=item["url"],
                output_dir=args.output_dir,
                stem=stem,
                language=language,
                sub_format=args.sub_format,
            )
        except Exception as exc:  # pragma: no cover - network/tool failure
            failures += 1
            print(f"Download failed: {exc}", file=sys.stderr)
            continue

        successes += 1
        print(f"Wrote: {output_path}")

    print(
        f"\nDone. Successful items: {successes}. Failed items: {failures}.",
    )


if __name__ == "__main__":
    main()
