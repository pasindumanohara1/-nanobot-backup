"""
Template 04: Purple Elegance
- Rich purple gradient
- Crescent moon & star decorations
- Royal, majestic feel
- Gold + white text

EDIT THESE to customize:
  TITLE_TEXT, ARABIC_TEXT, MAIN_TEXT, REFERENCE, ENGAGEMENT, HASHTAGS
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import os, math

# ====== EDITABLE CONTENT ======
TITLE_TEXT = "DUA OF THE DAY"
ARABIC_TEXT = "رَبِّ زِدْنِى عِلْمًا"
MAIN_TEXT = '"My Lord, increase me in knowledge."'
REFERENCE = "Quran 20:114"
ENGAGEMENT = "💬 Save this dua and share it with someone who needs it!"
HASHTAGS = "#Dua #IslamicReminder #Quran"

# ====== COLORS ======
BG_TOP = (35, 10, 55)
BG_BOTTOM = (65, 30, 95)
ACCENT = (255, 200, 100)
TEXT = (255, 255, 255)
SUBTEXT = (210, 190, 220)
CARD = (48, 18, 72)


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


def draw_crescent(draw, cx, cy, r, color):
    """Draw a crescent moon."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    draw.ellipse([cx - r + r // 3, cy - r - r // 5, cx + r + r // 3, cy + r - r // 5], fill=BG_TOP)


def draw_star(draw, cx, cy, size, color):
    """Draw a 6-pointed star."""
    points = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 2
        points.append((cx + int(size * math.cos(angle)), cy + int(size * math.sin(angle))))
        angle += math.pi / 6
        points.append((cx + int(size * 0.4 * math.cos(angle)), cy + int(size * 0.4 * math.sin(angle))))
    draw.polygon(points, fill=color)


def generate(output_path=None):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H))
    draw_gradient(img, BG_TOP, BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    # Scattered stars
    random_positions = [(120, 100), (900, 150), (200, 950), (850, 900), (540, 80), (100, 540), (980, 540)]
    for sx, sy in random_positions:
        draw_star(draw, sx, sy, 12, (*ACCENT, 60))

    # Crescent top center
    draw_crescent(draw, W // 2, 100, 35, ACCENT)

    # Card
    cm = 50
    draw.rounded_rectangle([cm, 140, W - cm, H - 60], radius=30, outline=ACCENT, width=3)

    y = 175
    cw = W - (cm + 30) * 2

    # Bismillah
    y = draw_text_centered(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", get_font(30), ACCENT, W)
    y += 20

    # Star separator
    draw_star(draw, W // 2, y + 8, 10, ACCENT)
    y += 25

    # Title
    y = draw_text_centered(draw, y, "🤲  " + TITLE_TEXT, get_font(24, bold=True), ACCENT, W)
    y += 25

    # Arabic
    ar_font = get_font(52)
    for line in wrap_text(ARABIC_TEXT, ar_font, cw, draw):
        y = draw_text_centered(draw, y, line, ar_font, TEXT, W)
    y += 20

    # Star separator
    draw_star(draw, W // 2, y + 8, 8, ACCENT)
    y += 20

    # Main text
    tr_font = get_font(32)
    for line in wrap_text(MAIN_TEXT, tr_font, cw, draw):
        y = draw_text_centered(draw, y, line, tr_font, SUBTEXT, W)
    y += 20

    # Reference
    y = draw_text_centered(draw, y, REFERENCE, get_font(26, bold=True), ACCENT, W)
    y += 30

    # Bottom
    y = max(y, H - 160)
    draw_star(draw, W // 2, y + 8, 8, ACCENT)
    y += 20

    eq_font = get_font(22)
    for line in wrap_text(ENGAGEMENT, eq_font, cw, draw):
        y = draw_text_centered(draw, y, line, eq_font, SUBTEXT, W)
    y += 10
    y = draw_text_centered(draw, y, HASHTAGS, get_font(18), ACCENT, W)

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..",
            "islamic_post_purple_{}.jpg".format(
                datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y%m%d_%H%M%S')))
    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    path = generate()
    print("Saved: {}".format(path))
