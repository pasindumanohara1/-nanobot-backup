"""
Template 06: Maroon Warmth
- Deep maroon/wine red gradient
- Warm cream + gold accents
- Cozy, warm Islamic feel
- Ornate corner decorations

EDIT THESE to customize:
  TITLE_TEXT, ARABIC_TEXT, MAIN_TEXT, REFERENCE, ENGAGEMENT, HASHTAGS
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import os, math

# ====== EDITABLE CONTENT ======
TITLE_TEXT = "QURAN VERSE OF THE DAY"
ARABIC_TEXT = "فَإِنَّ مَعَ ٱلْعُسْرِ يُسْرًا"
MAIN_TEXT = '"Indeed, with hardship comes ease."'
REFERENCE = "Quran 94:5"
ENGAGEMENT = "💬 Which verse touches your heart today?"
HASHTAGS = "#Quran #VerseOfTheDay #IslamicReminder"

# ====== COLORS ======
BG_TOP = (55, 10, 10)
BG_BOTTOM = (95, 25, 25)
ACCENT = (255, 220, 150)
TEXT = (255, 255, 255)
SUBTEXT = (230, 200, 190)
CARD = (72, 18, 18)


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


def draw_ornate_corner(draw, cx, cy, size, color, flip_x=False, flip_y=False):
    """Draw an ornate corner decoration."""
    sx = -1 if flip_x else 1
    sy = -1 if flip_y else 1
    # Curved line
    for angle_step in range(0, 90, 3):
        a1 = math.radians(angle_step)
        a2 = math.radians(angle_step + 3)
        r1 = size
        r2 = size - 3
        x1 = cx + int(sx * r1 * math.cos(a1))
        y1 = cy + int(sy * r1 * math.sin(a1))
        x2 = cx + int(sx * r2 * math.cos(a2))
        y2 = cy + int(sy * r2 * math.sin(a2))
        draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
    # Small circle at corner
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)


def generate(output_path=None):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H))
    draw_gradient(img, BG_TOP, BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    # Warm radial glow in center
    for r in range(400, 0, -2):
        alpha = int(30 * (1 - r / 400))
        draw.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                     fill=(min(255, BG_TOP[0] + alpha), BG_TOP[1], BG_TOP[2]))

    # Ornate corners
    cm = 40
    draw_ornate_corner(draw, cm + 5, cm + 5, 40, ACCENT, False, False)
    draw_ornate_corner(draw, W - cm - 5, cm + 5, 40, ACCENT, True, False)
    draw_ornate_corner(draw, cm + 5, H - cm - 5, 40, ACCENT, False, True)
    draw_ornate_corner(draw, W - cm - 5, H - cm - 5, 40, ACCENT, True, True)

    # Border
    draw.rectangle([cm, cm, W - cm, H - cm], outline=ACCENT, width=3)
    draw.rectangle([cm + 12, cm + 12, W - cm - 12, H - cm - 12], outline=(*ACCENT, 80), width=1)

    y = 85
    cw = W - (cm + 40) * 2

    # Bismillah
    y = draw_text_centered(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", get_font(30), ACCENT, W)
    y += 20

    # Decorative line with circles
    draw.line([(W // 2 - 100, y), (W // 2 + 100, y)], fill=ACCENT, width=2)
    draw.ellipse([W // 2 - 5, y - 5, W // 2 + 5, y + 5], fill=ACCENT)
    y += 25

    # Title
    y = draw_text_centered(draw, y, "📖  " + TITLE_TEXT, get_font(24, bold=True), ACCENT, W)
    y += 25

    # Arabic — large
    ar_font = get_font(58)
    for line in wrap_text(ARABIC_TEXT, ar_font, cw, draw):
        y = draw_text_centered(draw, y, line, ar_font, TEXT, W)
    y += 20

    # Separator
    draw.line([(W // 2 - 80, y), (W // 2 + 80, y)], fill=ACCENT, width=2)
    draw.ellipse([W // 2 - 4, y - 4, W // 2 + 4, y + 4], fill=ACCENT)
    y += 20

    # Main text
    tr_font = get_font(34)
    for line in wrap_text(MAIN_TEXT, tr_font, cw, draw):
        y = draw_text_centered(draw, y, line, tr_font, SUBTEXT, W)
    y += 20

    # Reference
    y = draw_text_centered(draw, y, REFERENCE, get_font(28, bold=True), ACCENT, W)
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

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..",
            "islamic_post_maroon_{}.jpg".format(
                datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y%m%d_%H%M%S')))
    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    path = generate()
    print("Saved: {}".format(path))
