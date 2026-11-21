#!/usr/bin/env python3
"""Paint the one-day world-news poster for Saturday 21 November 2026.

The poster is a single 1024x1024 PNG: a navy field, an amber kicker
and rule, six numbered stories, and a small footer. It reads nothing
from disk except the DejaVu typefaces and writes entry.png beside
this script. Everything about the day is baked into the STORIES
table below, so the output is the same on every run.
"""

from PIL import Image, ImageDraw, ImageFont

# --- canvas and palette -------------------------------------------------
SIDE = 1024
DEEP_NAVY = (13, 27, 46)
AMBER = (242, 169, 0)
PAPER = (255, 255, 255)
SOFT_GREY = (154, 167, 184)
FAINT_LINE = (45, 66, 92)

FONT_FOLDER = "/usr/share/fonts/truetype/dejavu/"
BOLD_FACE = FONT_FOLDER + "DejaVuSans-Bold.ttf"
PLAIN_FACE = FONT_FOLDER + "DejaVuSans.ttf"

# --- the day, in six items ----------------------------------------------
# Each item is (headline, body). The body is wrapped to fit the column.
STORIES = [
    (
        "RUSSIA'S BIGGEST STRIKE",
        "400+ drones and 110 missiles hit Ukraine overnight; 8 killed "
        "in Kyiv, bridges wrecked - and two missiles came down in Poland.",
    ),
    (
        "AI STOCKS TUMBLE",
        "US shares fell 3.7% as an AI sell-off pushed the S&P 500 and "
        "the Dow into correction territory.",
    ),
    (
        "TRUMP TO EUROPE: DEFUND UKRAINE",
        "After his summit with Putin, Trump told European leaders to "
        "withhold funding from Ukraine.",
    ),
    (
        "ANTHROPIC'S $2TN DEBUT",
        "The AI lab opened trading on Wall Street as a roughly $2 "
        "trillion company.",
    ),
    (
        "COP31 RUNS OVERTIME",
        "Climate talks in Antalya ran past deadline as nearly 200 "
        "nations failed to agree on fossil fuels.",
    ),
    (
        "CANCER PILL BREAKTHROUGH",
        "A trial pill made pancreatic tumours undetectable in 1 in 12 "
        "patients.",
    ),
]

KICKER_LINE = "THE WORLD IN ONE DAY"
DATE_LINE = "Saturday, 21 November 2026"
FOOTER_LINE = "Six stories from 21 November 2026  |  make.fun news-image-20261121"


def load_face(path, size):
    """Open one DejaVu face at the requested point size."""
    return ImageFont.truetype(path, size)


def fold_sentence(pen, sentence, face, limit_px):
    """Break a sentence into lines that each fit inside limit_px."""
    words = sentence.split()
    rows = []
    current = ""
    for word in words:
        attempt = (current + " " + word).strip()
        if pen.textlength(attempt, font=face) <= limit_px:
            current = attempt
        else:
            if current:
                rows.append(current)
            current = word
    if current:
        rows.append(current)
    return rows


def paint_header(pen):
    """Kicker, big date, and the amber rule across the page."""
    kicker_face = load_face(BOLD_FACE, 30)
    date_face = load_face(BOLD_FACE, 52)
    pen.text((48, 44), KICKER_LINE, font=kicker_face, fill=AMBER)
    pen.text((48, 80), DATE_LINE, font=date_face, fill=PAPER)
    pen.rectangle([48, 140, 976, 145], fill=AMBER)


def paint_story(pen, index, headline, body, top):
    """One numbered block. Returns the y coordinate just below it."""
    number_face = load_face(BOLD_FACE, 30)
    head_face = load_face(BOLD_FACE, 33)
    body_face = load_face(PLAIN_FACE, 27)

    # Amber disc with the story number, centred on its middle.
    disc_left, disc_top, disc_diam = 48, top, 56
    pen.ellipse(
        [disc_left, disc_top, disc_left + disc_diam, disc_top + disc_diam],
        fill=AMBER,
    )
    pen.text(
        (disc_left + disc_diam / 2, disc_top + disc_diam / 2),
        str(index),
        font=number_face,
        fill=DEEP_NAVY,
        anchor="mm",
    )

    # Headline sits level with the disc; body wraps beneath it.
    text_x = 122
    pen.text((text_x, top + 6), headline, font=head_face, fill=PAPER)
    body_rows = fold_sentence(pen, body, body_face, 976 - text_x)
    line_y = top + 50
    for row in body_rows:
        pen.text((text_x, line_y), row, font=body_face, fill=SOFT_GREY)
        line_y += 33
    return line_y


def paint_footer(pen):
    """Thin rule and the small closing line at the bottom."""
    foot_face = load_face(PLAIN_FACE, 22)
    pen.rectangle([48, 956, 976, 957], fill=FAINT_LINE)
    pen.text((48, 970), FOOTER_LINE, font=foot_face, fill=SOFT_GREY)


def build_poster():
    """Compose the whole poster and return it as a PIL image."""
    sheet = Image.new("RGB", (SIDE, SIDE), DEEP_NAVY)
    pen = ImageDraw.Draw(sheet)
    paint_header(pen)
    cursor = 170
    for position, (headline, body) in enumerate(STORIES, start=1):
        cursor = paint_story(pen, position, headline, body, cursor)
        cursor += 12  # breathing room before the next numbered block
    paint_footer(pen)
    return sheet


def main():
    poster = build_poster()
    poster.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
