"""Generate the 1024x1024 news infographic for Saturday 21 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1024, 1024
BG = (13, 27, 46)        # deep navy
PANEL = (24, 44, 66)     # panel navy
ACCENT = (255, 176, 32)  # amber
WHITE = (245, 245, 240)
MUTED = (176, 190, 205)
RED = (235, 87, 87)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
f_title = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 58)
f_date = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 46)
f_kicker = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 26)
f_head = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 30)
f_body = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 24)
f_foot = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 20)
f_num = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 34)

stories = [
    ("RUSSIA'S BIGGEST STRIKE",
     "400+ drones and 110 missiles hit Ukraine overnight; 8 killed in Kyiv, bridges wrecked - and two missiles came down in Poland."),
    ("AI STOCKS TUMBLE",
     "US shares fell 3.7% as an AI sell-off pushed the S&P 500 and the Dow into correction territory."),
    ("TRUMP TO EUROPE: DEFUND UKRAINE",
     "After his summit with Putin, Trump told European leaders to withhold funding from Ukraine."),
    ("ANTHROPIC'S $2TN DEBUT",
     "The AI lab opened trading on Wall Street as a roughly $2 trillion company."),
    ("COP31 RUNS OVERTIME",
     "Climate talks in Antalya ran past deadline as nearly 200 nations failed to agree on fossil fuels."),
    ("CANCER PILL BREAKTHROUGH",
     "A trial pill made pancreatic tumours undetectable in 1 in 12 patients."),
]

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Header
d.text((48, 36), "THE WORLD IN ONE DAY", font=f_kicker, fill=ACCENT)
d.text((48, 72), "Saturday, 21 November 2026", font=f_date, fill=WHITE)
d.rectangle([48, 140, 976, 146], fill=ACCENT)

y = 168
for i, (head, body) in enumerate(stories, 1):
    # number chip
    d.ellipse([48, y + 4, 100, y + 56], fill=ACCENT)
    num = str(i)
    nw = d.textlength(num, font=f_num)
    d.text((48 + (52 - nw) / 2, y + 8), num, font=f_num, fill=BG)
    # headline
    d.text((122, y), head, font=f_head, fill=WHITE)
    # body, wrapped
    lines = textwrap.wrap(body, width=62)
    by = y + 40
    for ln in lines:
        d.text((122, by), ln, font=f_body, fill=MUTED)
        by += 32
    y = by + 22

# Footer
d.rectangle([48, 962, 976, 964], fill=PANEL)
d.text((48, 974), "Six stories from 21 November 2026  |  make.fun news-image-20261121", font=f_foot, fill=MUTED)

img.save("entry.png", "PNG")
print("saved entry.png", img.size)
