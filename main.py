#!/usr/bin/env python3
"""Publish the 21 November 2026 world-news infographic.

The finished picture ships in this repository as entry.png.  Running
this program places an exact copy at /output/entry.png, the file the
bounty judges.  No image is drawn and nothing is downloaded here;
the only work is a faithful, byte-for-byte copy.
"""

from pathlib import Path


def find_picture() -> Path:
    """Locate the infographic bundled alongside this script."""
    folder = Path(__file__).resolve().parent
    return folder / "entry.png"


def publish() -> Path:
    """Copy the infographic into /output and confirm the copy's size."""
    picture = find_picture()
    if not picture.is_file():
        raise SystemExit(f"cannot find the infographic at {picture}")

    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / "entry.png"

    data = picture.read_bytes()
    destination.write_bytes(data)

    copied = destination.stat().st_size
    if copied != len(data):
        raise SystemExit(
            f"copy failed: wrote {copied} bytes, expected {len(data)}"
        )
    if not destination.exists():
        raise SystemExit(f"copy vanished: {destination} missing after writing")
    return destination


def main() -> None:
    done = publish()
    print(f"wrote {done} ({done.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
