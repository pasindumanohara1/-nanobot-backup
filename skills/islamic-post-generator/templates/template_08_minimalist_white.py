"""
Template 08: Minimalist White
- Clean white/light background
- Single accent color (teal)
- Lots of whitespace
- Modern, clean, Instagram-worthy

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
BG_TOP = (245, 245, 248)
BG_BOTTOM = (235, 235, 240)
ACCENT = (20, 140, 130)
TEXT = (30, 30, 40)
SUBTEXT = (100, 100, 110)
CARD = (255, 255, 255)


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

    # Subtle shadow card
    cm = 60
    card_top = 100
    card_bottom = H - 100

    # Shadow
    for offset in range(1, 8):
        alpha = 30 - offset * 3
        draw.rounded_rectangle(
            [cm + offset, card_top + offset, W - cm + offset, H - cm + offset],
            radius=20, fill=(200, 200, 205))

    # White card
    draw.rounded_rectangle([cm, card_top, W - cm, card_bottom], radius=20, fill=CARD, outline=ACCENT, width=2)

    # Top accent line
    draw.rectangle([cm, card_top, W - cm, card_top + 6], fill=ACCENT)

    y = card_top + 40
    cw = W - (cm + 40) * 2

    # Bismillah
    y = draw_text_centered(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", get_font(28), ACCENT, W)
    y += 25

    # Thin separator
    draw.line([(W // 2 - 60, y), (W // 2 + 60, y)], fill=ACCENT, width=2)
    y += 25

    # Title
    y = draw_text_centered(draw, y, "🕌  " + TITLE_TEXT, get_font(24, bold=True), ACCENT, W)
    y += 30

    # Arabic
    if ARABIC_TEXT:
        ar_font = get_font(52)
        for line in wrap_text(ARABIC_TEXT, ar_font, cw, draw):
            y = draw_text_centered(draw, y, line, ar_font, TEXT, W)
        y += 25
        draw.line([(W // 2 - 50, y), (W // 2 + 50, y)], fill=ACCENT, width=1)
        y += 25

    # Main text
    tr_font = get_font(32)
    for line in wrap_text(MAIN_TEXT, tr_font, cw, draw):
        y = draw_text_centered(draw, y, line, tr_font, TEXT, W)
    y += 25

    # Reference
    y = draw_text_centered(draw, y, REFERENCE, get_font(24, bold=True), ACCENT, W)
    y += 10
    y = draw_text_centered(draw, y, "👤 Prophet Muhammad ﷺ", get_font(22), SUBTEXT, W)

    # Bottom
    y = max(y + 30, card_bottom - 120)
    draw.line([(W // 2 - 60, y), (W // 2 + 60, y)], fill=ACCENT, width=1)
    y += 15

    eq_font = get_font(20)
    for line in wrap_text(ENGAGEMENT, eq_font, cw, draw):
        y = draw_text_centered(draw, y, line, eq_font, SUBTEXT, W)
    y += 10
    y = draw_text_centered(draw, y, HASHTAGS, get_font(16), ACCENT, W)

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..",
            "islamic_post_minimal_{}.jpg".format(
                datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y%m%d_%H%M%S')))
    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    path = generate()
    print("Saved: {}".format(path))
