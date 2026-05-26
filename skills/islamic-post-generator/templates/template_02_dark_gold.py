"""
Template 02: Dark Gold Luxury
- Deep black background with gold accents
- Minimalist, premium feel
- Large Arabic calligraphy focus
- Thin elegant lines

EDIT THESE to customize:
  TITLE_TEXT, ARABIC_TEXT, MAIN_TEXT, REFERENCE, ENGAGEMENT, HASHTAGS
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import os

# ====== EDITABLE CONTENT ======
TITLE_TEXT = "HADITH OF THE DAY"
ARABIC_TEXT = ""
MAIN_TEXT = '"The best among you are those who have the best manners and character."'
REFERENCE = "Sahih al-Bukhari 3559"
ENGAGEMENT = "💬 How do you apply this hadith in your daily life?"
HASHTAGS = "#Hadith #Sunnah #IslamicReminder"

# ====== COLORS ======
BG_TOP = (8, 8, 12)
BG_BOTTOM = (20, 18, 25)
ACCENT = (212, 175, 55)
TEXT = (255, 255, 255)
SUBTEXT = (170, 170, 180)
CARD = (15, 14, 20)


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

    # Thin gold border
    border = 35
    draw.rectangle([border, border, W - border, H - border], outline=ACCENT, width=2)
    draw.rectangle([border + 8, border + 8, W - border - 8, H - border - 8], outline=(*ACCENT, 80), width=1)

    # Top gold line accent
    draw.line([(border + 20, border + 50), (W - border - 20, border + 50)], fill=ACCENT, width=2)

    y = border + 80
    cw = W - (border + 50) * 2

    # Bismillah
    y = draw_text_centered(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", get_font(30), ACCENT, W)
    y += 30

    # Thin separator
    draw.line([(W // 2 - 80, y), (W // 2 + 80, y)], fill=ACCENT, width=1)
    y += 30

    # Title
    y = draw_text_centered(draw, y, "🕌  " + TITLE_TEXT, get_font(24, bold=True), ACCENT, W)
    y += 30

    # Arabic (if any)
    if ARABIC_TEXT:
        ar_font = get_font(56)
        for line in wrap_text(ARABIC_TEXT, ar_font, cw, draw):
            y = draw_text_centered(draw, y, line, ar_font, TEXT, W)
        y += 25
        draw.line([(W // 2 - 60, y), (W // 2 + 60, y)], fill=ACCENT, width=1)
        y += 25

    # Main text
    tr_font = get_font(36)
    for line in wrap_text(MAIN_TEXT, tr_font, cw, draw):
        y = draw_text_centered(draw, y, line, tr_font, TEXT, W)
    y += 25

    # Reference
    y = draw_text_centered(draw, y, REFERENCE, get_font(28, bold=True), ACCENT, W)
    y += 10
    y = draw_text_centered(draw, y, "👤 Prophet Muhammad ﷺ", get_font(24), SUBTEXT, W)

    # Bottom section
    y = max(y + 30, H - 160)
    draw.line([(W // 2 - 80, y), (W // 2 + 80, y)], fill=ACCENT, width=1)
    y += 15

    eq_font = get_font(22)
    for line in wrap_text(ENGAGEMENT, eq_font, cw, draw):
        y = draw_text_centered(draw, y, line, eq_font, SUBTEXT, W)
    y += 10
    y = draw_text_centered(draw, y, HASHTAGS, get_font(18), ACCENT, W)

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..",
            "islamic_post_darkgold_{}.jpg".format(
                datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y%m%d_%H%M%S')))
    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    path = generate()
    print("Saved: {}".format(path))
