"""
Template 10: Calligraphy Style
- Warm parchment/cream background
- Large decorative Arabic calligraphy area
- Gold frame with Islamic arch motifs
- Elegant, manuscript-inspired look

EDIT THESE to customize:
  TITLE_TEXT, ARABIC_TEXT, MAIN_TEXT, REFERENCE, ENGAGEMENT, HASHTAGS
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import os, math

# ====== EDITABLE CONTENT ======
TITLE_TEXT = "DUA OF THE DAY"
ARABIC_TEXT = "رَبَّنَا آتِنَا فِى ٱلدُّنْيَا حَسَنَةً وَفِى ٱلْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ ٱلنَّارِ"
MAIN_TEXT = '"Our Lord, give us good in this world and good in the Hereafter, and save us from the Fire."'
REFERENCE = "Quran 2:201"
ENGAGEMENT = "💬 Save this dua and share it with someone who needs it!"
HASHTAGS = "#Dua #IslamicReminder #Quran"

# ====== COLORS ======
BG_TOP = (235, 220, 190)
BG_BOTTOM = (210, 190, 155)
ACCENT = (140, 100, 30)
ACCENT2 = (180, 140, 60)
TEXT = (50, 35, 15)
SUBTEXT = (100, 80, 50)
CARD = (245, 235, 215)


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


def draw_arch(draw, cx, y_top, width, height, color, width_line=3):
    """Draw an Islamic pointed arch."""
    # Left pillar
    draw.line([(cx - width // 2, y_top + height), (cx - width // 2, y_top + 30)], fill=color, width=width_line)
    # Right pillar
    draw.line([(cx + width // 2, y_top + height), (cx + width // 2, y_top + 30)], fill=color, width=width_line)
    # Arch (two arcs meeting at top)
    for angle in range(0, 91, 2):
        rad = math.radians(angle)
        # Left arc
        lx = cx - int(width // 2 * math.cos(rad))
        ly = y_top + 30 - int(25 * math.sin(rad))
        # Right arc
        rx = cx + int(width // 2 * math.cos(rad))
        ry = y_top + 30 - int(25 * math.sin(rad))
        if angle > 0:
            draw.line([(prev_lx, prev_ly), (lx, ly)], fill=color, width=width_line)
            draw.line([(prev_rx, prev_ry), (rx, ry)], fill=color, width=width_line)
        prev_lx, prev_ly = lx, ly
        prev_rx, prev_ry = rx, ry
    # Point at top
    draw.polygon([(cx, y_top - 5), (cx - 8, y_top + 10), (cx + 8, y_top + 10)], fill=color)


def draw_frame(draw, x1, y1, x2, y2, color, accent):
    """Draw ornate Islamic frame."""
    # Outer frame
    draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
    # Inner frame
    draw.rectangle([x1 + 6, y1 + 6, x2 - 6, y2 - 6], outline=accent, width=1)
    # Corner ornaments
    cs = 20
    for cx, cy in [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]:
        draw.rectangle([cx - cs // 2, cy - cs // 2, cx + cs // 2, cy + cs // 2], fill=color)


def generate(output_path=None):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H))
    draw_gradient(img, BG_TOP, BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    # Subtle texture pattern (dots)
    for x in range(0, W, 20):
        for y in range(0, H, 20):
            draw.ellipse([x, y, x + 1, y + 1], fill=(*ACCENT, 15))

    # Main frame
    fm = 40
    draw_frame(draw, fm, fm, W - fm, H - fm, ACCENT, ACCENT2)

    # Top arch decoration
    draw_arch(draw, W // 2, fm + 10, 200, 50, ACCENT)

    y = fm + 75
    cw = W - (fm + 45) * 2

    # Bismillah — large and prominent
    y = draw_text_centered(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", get_font(34), ACCENT, W)
    y += 20

    # Decorative line
    draw.line([(W // 2 - 120, y), (W // 2 - 10, y)], fill=ACCENT, width=2)
    draw.ellipse([W // 2 - 6, y - 6, W // 2 + 6, y + 6], fill=ACCENT)
    draw.line([(W // 2 + 10, y), (W // 2 + 120, y)], fill=ACCENT, width=2)
    y += 25

    # Title
    y = draw_text_centered(draw, y, "🤲  " + TITLE_TEXT, get_font(24, bold=True), ACCENT, W)
    y += 25

    # Arabic calligraphy area — in a framed box
    ar_box_top = y
    ar_font = get_font(48)
    ar_lines = wrap_text(ARABIC_TEXT, ar_font, cw - 20, draw)
    for line in ar_lines:
        y = draw_text_centered(draw, y, line, ar_font, TEXT, W)
    ar_box_bottom = y + 15

    # Frame around Arabic
    draw_frame(draw, fm + 25, ar_box_top - 10, W - fm - 25, ar_box_bottom, ACCENT2, ACCENT)
    y += 25

    # Separator
    draw.line([(W // 2 - 80, y), (W // 2 - 10, y)], fill=ACCENT, width=2)
    draw.ellipse([W // 2 - 5, y - 5, W // 2 + 5, y + 5], fill=ACCENT)
    draw.line([(W // 2 + 10, y), (W // 2 + 80, y)], fill=ACCENT, width=2)
    y += 20

    # Main text (translation)
    tr_font = get_font(30)
    for line in wrap_text(MAIN_TEXT, tr_font, cw, draw):
        y = draw_text_centered(draw, y, line, tr_font, SUBTEXT, W)
    y += 15

    # Reference
    y = draw_text_centered(draw, y, REFERENCE, get_font(24, bold=True), ACCENT, W)
    y += 25

    # Bottom arch
    y = max(y + 10, H - 170)
    draw_arch(draw, W // 2, y, 160, 40, ACCENT)
    y += 55

    eq_font = get_font(20)
    for line in wrap_text(ENGAGEMENT, eq_font, cw, draw):
        y = draw_text_centered(draw, y, line, eq_font, SUBTEXT, W)
    y += 8
    y = draw_text_centered(draw, y, HASHTAGS, get_font(16), ACCENT, W)

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..",
            "islamic_post_calligraphy_{}.jpg".format(
                datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y%m%d_%H%M%S')))
    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    path = generate()
    print("Saved: {}".format(path))
