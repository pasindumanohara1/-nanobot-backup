"""
Template 05: Teal Modern
- Teal/turquoise gradient
- Modern geometric patterns
- Clean lines, contemporary feel
- White + mint accents

EDIT THESE to customize:
  TITLE_TEXT, ARABIC_TEXT, MAIN_TEXT, REFERENCE, ENGAGEMENT, HASHTAGS
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import os

# ====== EDITABLE CONTENT ======
TITLE_TEXT = "ISLAMIC REMINDER"
ARABIC_TEXT = ""
MAIN_TEXT = "The shade of a believer on the Day of Resurrection will be their charity. Give in charity today — even a smile is charity!"
REFERENCE = "💛 Sadaqah Reminder"
ENGAGEMENT = "💬 Share this reminder and spread the barakah!"
HASHTAGS = "#IslamicReminder #Sadaqah #Muslim"

# ====== COLORS ======
BG_TOP = (8, 35, 45)
BG_BOTTOM = (18, 65, 75)
ACCENT = (120, 210, 190)
TEXT = (255, 255, 255)
SUBTEXT = (180, 220, 210)
CARD = (15, 50, 60)


def get_font(size, bold=False):
    if bold:
        paths = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf"]
    else:
        paths = ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                continue
    return ImageFont.load_default()


def draw_gradient(img, top, bottom):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        r = int(top[0] + (bottom[0] - top[0]) * y / h)
        g = int(top[1] + (bottom[1] - top[1]) * y / h)
        b = int(top[2] + (bottom[2] - top[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def draw_text_centered(draw, y, text, font, fill, W):
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (W - (bbox[2] - bbox[0])) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return y + (bbox[3] - bbox[1]) + 4


def wrap_text(text, font, max_w, draw):
    lines, current = [], ""
    for word in text.split():
        test = f"{current} {word}".strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_w:
            current = test
        else:
            if current: lines.append(current)
            current = word
    if current: lines.append(current)
    return lines


def generate(output_path=None):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H))
    draw_gradient(img, BG_TOP, BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    # Geometric pattern — diagonal lines
    for i in range(-H, W + H, 30):
        draw.line([(i, 0), (i + H, H)], fill=(*ACCENT, 20), width=1)

    # Hexagonal card shape (approximated with rounded rect)
    cm = 55
    draw.rounded_rectangle([cm, 60, W - cm, H - 60], radius=15, outline=ACCENT, width=3)

    # Top accent bar
    draw.rectangle([cm, 60, W - cm, 68], fill=ACCENT)

    y = 100
    cw = W - (cm + 35) * 2

    # Bismillah
    y = draw_text_centered(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", get_font(28), ACCENT, W)
    y += 20

    # Geometric separator
    draw.line([(W // 2 - 100, y), (W // 2 + 100, y)], fill=ACCENT, width=2)
    draw.rectangle([W // 2 - 4, y - 4, W // 2 + 4, y + 4], fill=ACCENT)
    y += 25

    # Title
    y = draw_text_centered(draw, y, "✨  " + TITLE_TEXT, get_font(26, bold=True), ACCENT, W)
    y += 25

    # Arabic
    if ARABIC_TEXT:
        ar_font = get_font(56)
        for line in wrap_text(ARABIC_TEXT, ar_font, cw, draw):
            y = draw_text_centered(draw, y, line, ar_font, TEXT, W)
        y += 20
        draw.line([(W // 2 - 80, y), (W // 2 + 80, y)], fill=ACCENT, width=2)
        y += 20

    # Main text
    tr_font = get_font(32)
    for line in wrap_text(MAIN_TEXT, tr_font, cw, draw):
        y = draw_text_centered(draw, y, line, tr_font, TEXT, W)
    y += 20

    # Reference
    y = draw_text_centered(draw, y, REFERENCE, get_font(26, bold=True), ACCENT, W)
    y += 30

    # Bottom
    y = max(y, H - 160)
    draw.line([(W // 2 - 80, y), (W // 2 + 80, y)], fill=ACCENT, width=2)
    y += 15

    eq_font = get_font(22)
    for line in wrap_text(ENGAGEMENT, eq_font, cw, draw):
        y = draw_text_centered(draw, y, line, eq_font, SUBTEXT, W)
    y += 10
    y = draw_text_centered(draw, y, HASHTAGS, get_font(18), ACCENT, W)

    # Bottom accent bar
    draw.rectangle([cm, H - 68, W - cm, H - 60], fill=ACCENT)

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..",
            "islamic_post_teal_{}.jpg".format(
                datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y%m%d_%H%M%S')))
    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    path = generate()
    print("Saved: {}".format(path))
