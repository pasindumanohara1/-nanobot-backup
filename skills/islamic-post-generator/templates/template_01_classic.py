"""
Template 01: Classic Elegance
- Navy + Gold color scheme
- Rounded card with double border
- Bismillah header, diamond separators
- Clean, traditional Islamic look

EDIT THESE to customize:
  TITLE_TEXT    - Main title
  ARABIC_TEXT   - Arabic content
  MAIN_TEXT     - Main English text
  REFERENCE     - Source reference
  ENGAGEMENT    - Call-to-action question
  HASHTAGS      - Hashtag string
  BG_TOP/BG_BOTTOM/ACCENT - Colors
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import os

# ====== EDITABLE CONTENT ======
TITLE_TEXT = "QURAN VERSE OF THE DAY"
ARABIC_TEXT = "أَلَا بِذِكْرِ ٱللَّهِ تَطْمَئِنُّ ٱلْقُلُوبُ"
MAIN_TEXT = '"Verily, in the remembrance of Allah do hearts find rest."'
REFERENCE = "Quran 13:28"
ENGAGEMENT = "💬 Which verse touches your heart today?"
HASHTAGS = "#Quran #VerseOfTheDay #IslamicReminder"

# ====== COLORS (EDITABLE) ======
BG_TOP = (10, 25, 55)
BG_BOTTOM = (25, 55, 95)
ACCENT = (212, 175, 55)
TEXT = (255, 255, 255)
SUBTEXT = (180, 200, 220)
CARD = (20, 40, 75)

# ====== FONTS ======
def get_font(size, bold=False):
    if bold:
        paths = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf"]
    else:
        paths = ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf",
                 "C:/Windows/Fonts/calibri.ttf"]
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


def draw_deco_line(draw, y, W, accent):
    lw = 120
    draw.line([((W - lw) // 2, y), ((W + lw) // 2, y)], fill=accent, width=3)
    cx, cy = W // 2, y
    draw.polygon([(cx, cy - 6), (cx + 6, cy), (cx, cy + 6), (cx - 6, cy)], fill=accent)


def generate(output_path=None):
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H))
    draw_gradient(img, BG_TOP, BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    # Card
    cm = 50
    draw.rounded_rectangle([cm, 60, W - cm, H - 60], radius=25, outline=ACCENT, width=3)
    draw.rounded_rectangle([cm + 10, 70, W - cm - 10, H - 70], radius=20, outline=ACCENT, width=1)

    y = 100
    cw = W - (cm + 30) * 2
    margin = cm + 30

    # Bismillah
    y = draw_text_centered(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", get_font(32), ACCENT, W)
    y += 15
    draw_deco_line(draw, y + 5, W, ACCENT)
    y += 30

    # Title badge
    y = draw_text_centered(draw, y, "📖  " + TITLE_TEXT, get_font(22, bold=True), ACCENT, W)
    y += 20

    # Arabic
    ar_font = get_font(54)
    for line in wrap_text(ARABIC_TEXT, ar_font, cw, draw):
        y = draw_text_centered(draw, y, line, ar_font, TEXT, W)
    y += 20

    draw_deco_line(draw, y + 5, W, ACCENT)
    y += 25

    # Main text
    tr_font = get_font(34)
    for line in wrap_text(MAIN_TEXT, tr_font, cw, draw):
        y = draw_text_centered(draw, y, line, tr_font, SUBTEXT, W)
    y += 20

    # Reference
    y = draw_text_centered(draw, y, REFERENCE, get_font(28, bold=True), ACCENT, W)
    y += 30

    # Engagement
    y = max(y, H - 160)
    eq_font = get_font(22)
    for line in wrap_text(ENGAGEMENT, eq_font, cw, draw):
        y = draw_text_centered(draw, y, line, eq_font, SUBTEXT, W)
    y += 10
    y = draw_text_centered(draw, y, HASHTAGS, get_font(18), ACCENT, W)

    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "..",
            "islamic_post_classic_{}.jpg".format(
                datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y%m%d_%H%M%S')))
    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    path = generate()
    print("Saved: {}".format(path))
