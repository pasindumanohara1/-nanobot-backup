"""
Template 03: Green Nature
- Deep green gradient (like Islamic gardens)
- Leaf/organic decorative elements
- Fresh, calming feel
- White text on green

EDIT THESE to customize:
  TITLE_TEXT, ARABIC_TEXT, MAIN_TEXT, REFERENCE, ENGAGEMENT, HASHTAGS
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import os, math

# ====== EDITABLE CONTENT ======
TITLE_TEXT = "DHIKR OF THE DAY"
ARABIC_TEXT = "سُبْحَانَ ٱللَّهِ"
MAIN_TEXT = "SubhanAllah — Glory be to Allah"
REFERENCE = "🔢 Repeat 33 times"
ENGAGEMENT = "💬 Tag someone who needs this dhikr today!"
HASHTAGS = "#Dhikr #RemembranceOfAllah #IslamicReminder"

# ====== COLORS ======
BG_TOP = (10, 40, 20)
BG_BOTTOM = (30, 80, 40)
ACCENT = (255, 215, 0)
TEXT = (255, 255, 255)
SUBTEXT = (180, 220, 180)
CARD = (18, 55, 28)


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


def draw_leaf_ornament(draw, cx, cy, size, color):
    """Draw a simple leaf shape."""
    points = []
    for i in range(20):
        angle = (i / 20) * math.pi
        r = size * (1 - abs(i - 10) / 10) * 0.5
        px = cx + int(r * math.cos(angle) * 0.4)
        py = cy + int(r * math.sin(angle))
        points.append((px, py))
    for i in range(20):
        angle = math.pi + (i / 20) * math.pi
        r = size * (1 - abs(i - 10) / 10) * 0.5
        px = cx + int(r * math.cos(angle) * 0.4)
        py = cy + int(r * math.sin(angle))
        points.append((px, py))
    if len(points) >= 3:
        draw.polygon(points, fill=color)


def generate(output_path=None):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H))
    draw_gradient(img, BG_TOP, BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    # Organic curved border
    cm = 45
    draw.rounded_rectangle([cm, 55, W - cm, H - 55], radius=40, outline=ACCENT, width=3)
    draw.rounded_rectangle([cm + 8, 63, W - cm - 8, H - 63], radius=35, outline=(*ACCENT, 60), width=1)

    # Leaf ornaments at corners
    leaf_color = (*ACCENT, 40)
    for lx, ly in [(cm + 20, cm + 20), (W - cm - 20, cm + 20),
                   (cm + 20, H - cm - 20), (W - cm - 20, H - cm - 20)]:
        draw_leaf_ornament(draw, lx, ly, 30, ACCENT)

    y = 90
    cw = W - (cm + 35) * 2
    margin = cm + 35

    # Bismillah
    y = draw_text_centered(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", get_font(30), ACCENT, W)
    y += 20

    # Decorative leaves separator
    for lx in range(W // 2 - 80, W // 2 + 81, 20):
        draw_leaf_ornament(draw, lx, y + 5, 8, ACCENT)
    y += 25

    # Title
    y = draw_text_centered(draw, y, "🤲  " + TITLE_TEXT, get_font(24, bold=True), ACCENT, W)
    y += 25

    # Arabic — very large
    ar_font = get_font(72)
    for line in wrap_text(ARABIC_TEXT, ar_font, cw, draw):
        y = draw_text_centered(draw, y, line, ar_font, TEXT, W)
    y += 20

    # Separator
    for lx in range(W // 2 - 60, W // 2 + 61, 15):
        draw_leaf_ornament(draw, lx, y + 3, 6, ACCENT)
    y += 20

    # Main text
    tr_font = get_font(34)
    for line in wrap_text(MAIN_TEXT, tr_font, cw, draw):
        y = draw_text_centered(draw, y, line, tr_font, SUBTEXT, W)
    y += 20

    # Reference
    y = draw_text_centered(draw, y, REFERENCE, get_font(28, bold=True), ACCENT, W)
    y += 30

    # Bottom engagement
    y = max(y, H - 160)
    for lx in range(W // 2 - 60, W // 2 + 61, 15):
        draw_leaf_ornament(draw, lx, y, 6, ACCENT)
    y += 15

    eq_font = get_font(22)
    for line in wrap_text(ENGAGEMENT, eq_font, cw, draw):
        y = draw_text_centered(draw, y, line, eq_font, SUBTEXT, W)
    y += 10
    y = draw_text_centered(draw, y, HASHTAGS, get_font(18), ACCENT, W)

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..",
            "islamic_post_green_{}.jpg".format(
                datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y%m%d_%H%M%S')))
    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    path = generate()
    print("Saved: {}".format(path))
