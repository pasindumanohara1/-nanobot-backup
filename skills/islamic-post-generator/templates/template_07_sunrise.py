"""
Template 07: Sunrise Gradient
- Warm orange → pink → purple gradient (like Fajr sunrise)
- Horizontal layered feel
- Hopeful, uplifting mood
- White + warm gold text

EDIT THESE to customize:
  TITLE_TEXT, ARABIC_TEXT, MAIN_TEXT, REFERENCE, ENGAGEMENT, HASHTAGS
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import os

# ====== EDITABLE CONTENT ======
TITLE_TEXT = "PRAYER TIMES"
ARABIC_TEXT = ""
MAIN_TEXT = "Fajr: 4:45 AM  |  Dhuhr: 12:15 PM  |  Asr: 3:30 PM\nMaghrib: 6:20 PM  |  Isha: 7:45 PM"
REFERENCE = "📅 15 Ramadan 1447 AH — Colombo, Sri Lanka"
ENGAGEMENT = "💬 Which prayer do you never miss? Comment below!"
HASHTAGS = "#PrayerTimes #Salah #IslamicReminder"

# ====== COLORS ======
BG_TOP = (255, 140, 50)
BG_MID = (200, 60, 80)
BG_BOTTOM = (60, 20, 80)
ACCENT = (255, 230, 180)
TEXT = (255, 255, 255)
SUBTEXT = (255, 220, 200)
CARD = (80, 30, 60)


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


def draw_gradient(img, top, mid, bottom):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        ratio = y / h
        if ratio < 0.5:
            r = int(top[0] + (mid[0] - top[0]) * ratio * 2)
            g = int(top[1] + (mid[1] - top[1]) * ratio * 2)
            b = int(top[2] + (mid[2] - top[2]) * ratio * 2)
        else:
            r = int(mid[0] + (bottom[0] - mid[0]) * (ratio - 0.5) * 2)
            g = int(mid[1] + (bottom[1] - mid[1]) * (ratio - 0.5) * 2)
            b = int(mid[2] + (bottom[2] - mid[2]) * (ratio - 0.5) * 2)
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


def draw_sun_burst(draw, cx, cy, rays, length, color):
    """Draw sun burst lines."""
    import math
    for i in range(rays):
        angle = (2 * math.pi / rays) * i
        x2 = cx + int(length * math.cos(angle))
        y2 = cy + int(length * math.sin(angle))
        draw.line([(cx, cy), (x2, y2)], fill=color, width=2)


def generate(output_path=None):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H))
    draw_gradient(img, BG_TOP, BG_MID, BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    # Sun burst from top center
    draw_sun_burst(draw, W // 2, -20, 24, 300, (*ACCENT, 30))

    # Horizon line glow
    for x in range(W):
        for dy in range(-30, 30):
            y_pos = 200 + dy
            if 0 <= y_pos < H:
                alpha = max(0, 1 - abs(dy) / 30)
                r = min(255, BG_TOP[0] + int(40 * alpha))
                g = min(255, BG_TOP[1] + int(20 * alpha))
                b = BG_TOP[2]
                draw.point((x, y_pos), fill=(r, g, b))

    # Content card — frosted glass effect (semi-transparent dark overlay)
    cm = 50
    card_top = 80
    card_bottom = H - 80
    # Dark overlay for card
    for y in range(card_top, card_bottom):
        for x in range(cm, W - cm):
            # Simple rounded check
            if (x - cm < 25 or W - cm - x < 25 or y - card_top < 25 or card_bottom - y < 25):
                continue
            draw.point((x, y), fill=(40, 15, 45))

    draw.rounded_rectangle([cm, card_top, W - cm, card_bottom], radius=25, outline=ACCENT, width=3)

    y = 115
    cw = W - (cm + 35) * 2

    # Bismillah
    y = draw_text_centered(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", get_font(28), ACCENT, W)
    y += 20

    # Sun icon
    draw_sun_burst(draw, W // 2, y + 15, 8, 20, ACCENT)
    draw.ellipse([W // 2 - 12, y + 3, W // 2 + 12, y + 27], fill=ACCENT)
    y += 40

    # Title
    y = draw_text_centered(draw, y, "🌅  " + TITLE_TEXT, get_font(26, bold=True), ACCENT, W)
    y += 25

    # Arabic
    if ARABIC_TEXT:
        ar_font = get_font(54)
        for line in wrap_text(ARABIC_TEXT, ar_font, cw, draw):
            y = draw_text_centered(draw, y, line, ar_font, TEXT, W)
        y += 20

    # Main text
    tr_font = get_font(30)
    for line in wrap_text(MAIN_TEXT, tr_font, cw, draw):
        y = draw_text_centered(draw, y, line, tr_font, TEXT, W)
    y += 20

    # Reference
    y = draw_text_centered(draw, y, REFERENCE, get_font(24, bold=True), ACCENT, W)
    y += 30

    # Bottom
    y = max(y, H - 160)
    draw_sun_burst(draw, W // 2, y + 10, 6, 15, ACCENT)
    y += 25

    eq_font = get_font(22)
    for line in wrap_text(ENGAGEMENT, eq_font, cw, draw):
        y = draw_text_centered(draw, y, line, eq_font, SUBTEXT, W)
    y += 10
    y = draw_text_centered(draw, y, HASHTAGS, get_font(18), ACCENT, W)

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..",
            "islamic_post_sunrise_{}.jpg".format(
                datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y%m%d_%H%M%S')))
    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    path = generate()
    print("Saved: {}".format(path))
