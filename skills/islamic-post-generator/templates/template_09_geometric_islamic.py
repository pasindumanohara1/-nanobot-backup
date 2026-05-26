"""
Template 09: Geometric Islamic
- Dark background with Islamic geometric star patterns
- 8-pointed star (khatam) grid overlay
- Rich gold + emerald accents
- Traditional Islamic art inspired

EDIT THESE to customize:
  TITLE_TEXT, ARABIC_TEXT, MAIN_TEXT, REFERENCE, ENGAGEMENT, HASHTAGS
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import os, math

# ====== EDITABLE CONTENT ======
TITLE_TEXT = "DHIKR OF THE DAY"
ARABIC_TEXT = "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِٱللَّهِ"
MAIN_TEXT = "La hawla wa la quwwata illa billah\nThere is no power nor strength except with Allah"
REFERENCE = "🔢 Repeat 100 times"
ENGAGEMENT = "💬 Tag someone who needs this dhikr today!"
HASHTAGS = "#Dhikr #RemembranceOfAllah #IslamicReminder"

# ====== COLORS ======
BG_TOP = (12, 18, 15)
BG_BOTTOM = (25, 35, 28)
ACCENT = (200, 170, 60)
ACCENT2 = (80, 180, 130)
TEXT = (255, 255, 255)
SUBTEXT = (180, 200, 185)
CARD = (18, 28, 22)


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


def draw_8pointed_star(draw, cx, cy, outer_r, inner_r, color):
    """Draw an 8-pointed star (classic Islamic geometric pattern)."""
    points = []
    for i in range(16):
        angle = math.pi / 8 * i - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        points.append((cx + int(r * math.cos(angle)), cy + int(r * math.sin(angle))))
    draw.polygon(points, fill=color)


def draw_geometric_border(draw, W, H, margin, color):
    """Draw Islamic geometric pattern along borders."""
    spacing = 50
    # Top and bottom
    for x in range(margin + 25, W - margin - 20, spacing):
        draw_8pointed_star(draw, x, margin + 10, 12, 5, color)
        draw_8pointed_star(draw, x, H - margin - 10, 12, 5, color)
    # Left and right
    for y in range(margin + 25, H - margin - 20, spacing):
        draw_8pointed_star(draw, margin + 10, y, 12, 5, color)
        draw_8pointed_star(draw, W - margin - 10, y, 12, 5, color)


def generate(output_path=None):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H))
    draw_gradient(img, BG_TOP, BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    # Scattered geometric stars in background
    for gx in range(40, W, 80):
        for gy in range(40, H, 80):
            draw_8pointed_star(draw, gx, gy, 15, 6, (*ACCENT, 25))

    # Border pattern
    bm = 35
    draw.rectangle([bm, bm, W - bm, H - bm], outline=ACCENT, width=2)
    draw.rectangle([bm + 8, bm + 8, W - bm - 8, H - bm - 8], outline=ACCENT2, width=1)
    draw_geometric_border(draw, W, bm, bm, ACCENT)

    # Corner stars
    for cx, cy in [(bm + 20, bm + 20), (W - bm - 20, bm + 20),
                   (bm + 20, H - bm - 20), (W - bm - 20, H - bm - 20)]:
        draw_8pointed_star(draw, cx, cy, 25, 10, ACCENT)

    y = 80
    cw = W - (bm + 40) * 2

    # Bismillah
    y = draw_text_centered(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", get_font(30), ACCENT, W)
    y += 20

    # Star separator
    draw_8pointed_star(draw, W // 2, y + 10, 12, 5, ACCENT)
    y += 25

    # Title
    y = draw_text_centered(draw, y, "🤲  " + TITLE_TEXT, get_font(24, bold=True), ACCENT, W)
    y += 25

    # Arabic — very large
    ar_font = get_font(58)
    for line in wrap_text(ARABIC_TEXT, ar_font, cw, draw):
        y = draw_text_centered(draw, y, line, ar_font, TEXT, W)
    y += 20

    # Star separator
    draw_8pointed_star(draw, W // 2, y + 8, 10, 4, ACCENT2)
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
    draw_8pointed_star(draw, W // 2, y + 8, 10, 4, ACCENT)
    y += 20

    eq_font = get_font(22)
    for line in wrap_text(ENGAGEMENT, eq_font, cw, draw):
        y = draw_text_centered(draw, y, line, eq_font, SUBTEXT, W)
    y += 10
    y = draw_text_centered(draw, y, HASHTAGS, get_font(18), ACCENT, W)

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..",
            "islamic_post_geometric_{}.jpg".format(
                datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y%m%d_%H%M%S')))
    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    path = generate()
    print("Saved: {}".format(path))
