"""
Islamic Engagement Post Generator with Images
Uses AlAdhan API for prayer times, Hijri dates, and generates beautiful images.
Designed for maximum engagement — big text, bold visuals, scroll-stopping design.
"""

import json
import random
import sys
import os
import urllib.request
from datetime import datetime, timezone, timedelta

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

IST = timezone(timedelta(hours=5, minutes=30))
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ====== API CONFIG ======
ALADHAN_BASE = "https://api.aladhan.com/v1"
DEFAULT_LAT = 6.9271
DEFAULT_LON = 79.8612
CALCULATION_METHOD = 2

# ====== QURAN VERSES ======
QURAN_VERSES = [
    {"surah": "Al-Baqarah", "ayah": 286, "arabic": "لَا يُكَلِّفُ ٱللَّهُ نَفْسًا إِلَّا وُسْعَهَا", "translation": "Allah does not burden a soul beyond that it can bear.", "reference": "Quran 2:286"},
    {"surah": "Ar-Ra'd", "ayah": 28, "arabic": "أَلَا بِذِكْرِ ٱللَّهِ تَطْمَئِنُّ ٱلْقُلُوبُ", "translation": "Verily, in the remembrance of Allah do hearts find rest.", "reference": "Quran 13:28"},
    {"surah": "Al-Imran", "ayah": 139, "arabic": "وَلَا تَهِنُوا وَلَا تَحْزَنُوا وَأَنتُمُ ٱلْأَعْلَوْنَ", "translation": "Do not lose heart, nor fall into despair, for you shall prevail if you are truly believers.", "reference": "Quran 3:139"},
    {"surah": "At-Talaq", "ayah": 3, "arabic": "وَمَن يَتَوَكَّلْ عَلَى ٱللَّهِ فَهُوَ حَسْبُهُ", "translation": "And whoever relies upon Allah – then He is sufficient for him.", "reference": "Quran 65:3"},
    {"surah": "Al-Baqarah", "ayah": 152, "arabic": "فَٱذْكُرُونِىٓ أَذْكُرْكُمْ", "translation": "So remember Me; I will remember you.", "reference": "Quran 2:152"},
    {"surah": "Al-Ankabut", "ayah": 69, "arabic": "وَٱلَّذِينَ جَٰهَدُوا فِينَا لَنَهْدِيَنَّهُمْ سُبُلَنَا", "translation": "And those who strive for Us – We will surely guide them to Our ways.", "reference": "Quran 29:69"},
    {"surah": "Az-Zumar", "ayah": 53, "arabic": "لَا تَقْنَطُوا۟ مِن رَّحْمَةِ ٱللَّهِ", "translation": "Do not despair of the mercy of Allah.", "reference": "Quran 39:53"},
    {"surah": "Ash-Sharh", "ayah": 5, "arabic": "فَإِنَّ مَعَ ٱلْعُسْرِ يُسْرًا", "translation": "Indeed, with hardship comes ease.", "reference": "Quran 94:5"},
    {"surah": "Al-Baqarah", "ayah": 156, "arabic": "إِنَّا لِلَّهِ وَإِنَّآ إِلَيْهِ رَٰجِعُونَ", "translation": "Indeed, to Allah we belong and to Him we shall return.", "reference": "Quran 2:156"},
    {"surah": "Al-Baqarah", "ayah": 255, "arabic": "ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلْحَىُّ ٱلْقَيُّومُ", "translation": "Allah – there is no deity except Him, the Ever-Living, the Sustainer.", "reference": "Quran 2:255"},
    {"surah": "An-Nahl", "ayah": 97, "arabic": "مَنْ عَمِلَ صَٰلِحًا مِّن ذَكَرٍ أَوْ أُنثَىٰ وَهُوَ مُؤْمِنٌ", "translation": "Whoever does righteousness while a believer – We will grant them a good life.", "reference": "Quran 16:97"},
    {"surah": "Al-Mujadila", "ayah": 11, "arabic": "يَرْفَعِ ٱللَّهُ ٱلَّذِينَ ءَامَنُوا۟ مِنكُمْ وَٱلَّذِينَ أُوتُوا۟ ٱلْعِلْمَ دَرَجَٰتٍ", "translation": "Allah will raise those who have believed among you and those who were given knowledge by degrees.", "reference": "Quran 58:11"},
]

# ====== HADITH ======
HADITH_COLLECTION = [
    {"text": "The best among you are those who have the best manners and character.", "source": "Sahih al-Bukhari 3559"},
    {"text": "None of you truly believes until he loves for his brother what he loves for himself.", "source": "Sahih al-Bukhari 13"},
    {"text": "The strong person is not the one who can wrestle someone else down. The strong person is the one who can control himself when he is angry.", "source": "Sahih al-Bukhari 6114"},
    {"text": "Whoever believes in Allah and the Last Day, let him speak good or remain silent.", "source": "Sahih al-Bukhari 6018"},
    {"text": "Make things easy and do not make them difficult. Give glad tidings and do not repel people.", "source": "Sahih al-Bukhari 69"},
    {"text": "The world is a prison for the believer and a paradise for the disbeliever.", "source": "Sahih Muslim 2956"},
    {"text": "Verily, actions are judged by intentions, and everyone will get what they intended.", "source": "Sahih al-Bukhari 1"},
    {"text": "The most beloved of deeds to Allah are those that are most consistent, even if they are small.", "source": "Sahih al-Bukhari 6464"},
    {"text": "Whoever removes a worldly hardship from a believer, Allah will remove one of his hardships on the Day of Resurrection.", "source": "Sahih Muslim 2959"},
    {"text": "He who eats his fill while his neighbor goes without food is not a believer.", "source": "Al-Adab Al-Mufrad 112"},
]

# ====== DHIKR ======
DHIKR_COLLECTION = [
    {"arabic": "سُبْحَانَ ٱللَّهِ", "transliteration": "SubhanAllah", "meaning": "Glory be to Allah", "count": 33},
    {"arabic": "ٱلْحَمْدُ لِلَّهِ", "transliteration": "Alhamdulillah", "meaning": "All praise is due to Allah", "count": 33},
    {"arabic": "ٱللَّهُ أَكْبَرُ", "transliteration": "Allahu Akbar", "meaning": "Allah is the Greatest", "count": 34},
    {"arabic": "لَآ إِلَٰهَ إِلَّآ ٱللَّهُ", "transliteration": "La ilaha illallah", "meaning": "There is no god but Allah", "count": 100},
    {"arabic": "أَسْتَغْفِرُ ٱللَّهَ", "transliteration": "Astaghfirullah", "meaning": "I seek forgiveness from Allah", "count": 100},
    {"arabic": "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِٱللَّهِ", "transliteration": "La hawla wa la quwwata illa billah", "meaning": "There is no power nor strength except with Allah", "count": 100},
    {"arabic": "سُبْحَانَ ٱللَّهِ وَبِحَمْدِهِ", "transliteration": "SubhanAllahi wa bihamdihi", "meaning": "Glory be to Allah and His is the praise", "count": 100},
]

# ====== DUA ======
DUA_COLLECTION = [
    {"arabic": "رَبَّنَا آتِنَا فِى ٱلدُّنْيَا حَسَنَةً وَفِى ٱلْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ ٱلنَّارِ", "transliteration": "Rabbana atina fid-dunya hasanatan wa fil-akhirati hasanatan wa qina adhaban-nar", "meaning": "Our Lord, give us good in this world and good in the Hereafter, and save us from the Fire.", "source": "Quran 2:201"},
    {"arabic": "رَبِّ ٱشْرَحْ لِى صَدْرِى وَيَسِّرْ لِىٓ أَمْرِى", "transliteration": "Rabbi shrah li sadri wa yassir li amri", "meaning": "My Lord, expand for me my chest and ease for me my task.", "source": "Quran 20:25-26"},
    {"arabic": "رَبِّ زِدْنِى عِلْمًا", "transliteration": "Rabbi zidni ilma", "meaning": "My Lord, increase me in knowledge.", "source": "Quran 20:114"},
    {"arabic": "رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا", "transliteration": "Rabbana la tuzigh quloobana ba'da idh hadaytana", "meaning": "Our Lord, let not our hearts deviate after You have guided us.", "source": "Quran 3:8"},
    {"arabic": "ٱللَّهُمَّ إِنِّىٓ أَسْأَلُكَ ٱلْهُدَىٰ وَٱلتُّقَىٰ وَٱلْعَفَافَ وَٱلْغِنَىٰ", "transliteration": "Allahumma inni as'aluka al-huda wa at-tuqa wa al-'afafa wa al-ghina", "meaning": "O Allah, I ask You for guidance, piety, chastity, and self-sufficiency.", "source": "Sahih Muslim 2721"},
    {"arabic": "ٱللَّهُمَّ أَعِنِّى عَلَىٰ ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ", "transliteration": "Allahumma a'inni 'ala dhikrika wa shukrika wa husni 'ibadatik", "meaning": "O Allah, help me to remember You, be grateful to You, and worship You in the best manner.", "source": "Sunan Abu Dawud 1522"},
]

# ====== ISLAMIC REMINDERS ======
ISLAMIC_REMINDERS = [
    {"title": "Give Sadaqah Today", "text": "The shade of a believer on the Day of Resurrection will be their charity. Give in charity today — even a smile is charity!", "emoji": "💛"},
    {"title": "Power of Istighfar", "text": "Make istighfar a habit. Whoever makes it frequently, Allah will provide a way out of every difficulty and provision from where they don't expect.", "emoji": "🤲"},
    {"title": "Send Salawat", "text": "Send blessings upon the Prophet ﷺ — every time you send salawat, Allah sends blessings upon you 10 times!", "emoji": "💚"},
    {"title": "Be Grateful", "text": "Allah says: 'If you are grateful, I will surely increase you in blessing.' Start your day with Alhamdulillah!", "emoji": "🌙"},
    {"title": "Have Patience", "text": "When you face hardship, remember: Allah does not burden a soul beyond what it can bear. Relief is coming.", "emoji": "✨"},
    {"title": "Read Quran Daily", "text": "Make Quran part of your daily routine. Even one ayah! The Prophet ﷺ said: 'The best of you are those who learn the Quran and teach it.'", "emoji": "📖"},
    {"title": "Never Stop Making Dua", "text": "Dua is the weapon of the believer. Allah is near and responsive — call upon Him with hope and sincerity.", "emoji": "🤲"},
    {"title": "Don't Miss Fajr", "text": "The one who prays Fajr is under the protection of Allah. The Prophet ﷺ said: 'Whoever prays Fajr is under the guarantee of Allah.'", "emoji": "🌅"},
]

# ====== ENGAGEMENT QUESTIONS ======
ENGAGEMENT_QUESTIONS = [
    "💬 Which verse touches your heart today? Comment below!",
    "💬 How do you apply this in your daily life? Share below!",
    "💬 Tag someone who needs to see this!",
    "💬 Save this and share it with someone who needs it!",
    "💬 Which prayer do you never miss? Comment below!",
    "💬 What's your favorite dhikr? Let us know!",
    "💬 Share this and spread the barakah!",
    "💬 Double tap if you agree! ❤️",
    "💬 Share this with someone who needs this reminder!",
    "💬 What's your favorite Quran verse? Tell us below!",
]

# ====== COLOR THEMES (more vibrant) ======
THEMES = [
    {"bg_top": (10, 25, 55), "bg_bottom": (25, 55, 95), "accent": (212, 175, 55), "text": (255, 255, 255), "subtext": (180, 200, 220), "card": (20, 40, 75)},
    {"bg_top": (15, 45, 25), "bg_bottom": (35, 80, 45), "accent": (255, 215, 0), "text": (255, 255, 255), "subtext": (180, 220, 180), "card": (25, 60, 35)},
    {"bg_top": (40, 15, 55), "bg_bottom": (70, 35, 95), "accent": (255, 200, 100), "text": (255, 255, 255), "subtext": (210, 190, 220), "card": (55, 25, 75)},
    {"bg_top": (55, 10, 10), "bg_bottom": (95, 25, 25), "accent": (255, 220, 150), "text": (255, 255, 255), "subtext": (230, 190, 190), "card": (75, 18, 18)},
    {"bg_top": (8, 35, 45), "bg_bottom": (18, 65, 75), "accent": (120, 210, 190), "text": (255, 255, 255), "subtext": (180, 220, 210), "card": (15, 50, 60)},
    {"bg_top": (30, 10, 50), "bg_bottom": (55, 20, 80), "accent": (200, 150, 255), "text": (255, 255, 255), "subtext": (200, 180, 220), "card": (42, 15, 65)},
]


def api_get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}


def get_prayer_times(lat=DEFAULT_LAT, lon=DEFAULT_LON):
    now_ist = datetime.now(IST)
    date_str = now_ist.strftime("%d-%m-%Y")
    url = f"{ALADHAN_BASE}/timings/{date_str}?latitude={lat}&longitude={lon}&method={CALCULATION_METHOD}"
    data = api_get(url)
    if "error" in data:
        return None
    try:
        timings = data["data"]["timings"]
        hijri = data["data"]["date"]["hijri"]
        return {
            "fajr": timings["Fajr"].split()[0],
            "sunrise": timings["Sunrise"].split()[0],
            "dhuhr": timings["Dhuhr"].split()[0],
            "asr": timings["Asr"].split()[0],
            "maghrib": timings["Maghrib"].split()[0],
            "isha": timings["Isha"].split()[0],
            "hijri_date": "{} {} {} AH".format(hijri['day'], hijri['month']['en'], hijri['year']),
        }
    except (KeyError, IndexError):
        return None


def get_font(size, bold=False):
    """Try to load a nice font, fallback to default."""
    if bold:
        font_paths = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]
    else:
        font_paths = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/tahoma.ttf",
        ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()


def draw_gradient(img, top_color, bottom_color):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        ratio = y / h
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def draw_rounded_rect(draw, xy, radius, fill, outline=None, outline_width=2):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=outline_width)


def draw_text_with_shadow(draw, pos, text, font, fill, shadow_color=(0,0,0), offset=3):
    """Draw text with a shadow for better readability."""
    x, y = pos
    # Shadow
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
    # Main text
    draw.text((x, y), text, font=font, fill=fill)


def draw_centered_text(draw, y, text, font, fill, w, shadow=True):
    """Draw horizontally centered text. Returns new y position."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (w - tw) // 2
    if shadow:
        draw_text_with_shadow(draw, (x, y), text, font, fill)
    else:
        draw.text((x, y), text, font=font, fill=fill)
    return y + th + 4


def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def draw_decorative_line(draw, y, w, accent):
    """Draw a decorative centered line."""
    line_w = 120
    x1 = (w - line_w) // 2
    x2 = x1 + line_w
    draw.line([(x1, y), (x2, y)], fill=accent, width=3)
    # Diamond in center
    cx, cy = w // 2, y
    draw.polygon([(cx, cy - 6), (cx + 6, cy), (cx, cy + 6), (cx - 6, cy)], fill=accent)


def generate_image(post_type, data, prayer_info=None):
    """Generate a beautiful, engaging Islamic-themed image."""
    if not HAS_PILLOW:
        return None

    W, H = 1080, 1080
    theme = random.choice(THEMES)
    img = Image.new("RGB", (W, H))
    draw_gradient(img, theme["bg_top"], theme["bg_bottom"])
    draw = ImageDraw.Draw(img)

    # Subtle geometric pattern overlay
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    for i in range(-H, W + H, 60):
        ov_draw.line([(i, 0), (i + H, H)], fill=(*theme["accent"], 15), width=1)
    img.paste(Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), overlay).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)

    # Main content card
    card_margin = 50
    card_top = 60
    card_bottom = H - 60
    card_color = (*theme["card"], 180)
    draw_rounded_rect(draw, [card_margin, card_top, W - card_margin, card_bottom], radius=25,
                      fill=None, outline=theme["accent"], outline_width=3)

    # Inner border
    inner_m = card_margin + 10
    draw_rounded_rect(draw, [inner_m, card_top + 10, W - inner_m, card_bottom - 10], radius=20,
                      fill=None, outline=(*theme["accent"], 100), outline_width=1)

    y = card_top + 40
    margin = card_margin + 30
    content_width = W - margin * 2

    # ====== BISMILLAH ======
    bism_font = get_font(32)
    y = draw_centered_text(draw, y, "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", bism_font, theme["accent"], W)
    y += 15

    # Decorative line
    draw_decorative_line(draw, y + 5, W, theme["accent"])
    y += 30

    # ====== CONTENT BY TYPE ======

    if post_type == "quran_verse":
        # Type badge
        badge_font = get_font(22, bold=True)
        badge_text = "📖  QURAN VERSE OF THE DAY"
        y = draw_centered_text(draw, y, badge_text, badge_font, theme["accent"], W)
        y += 20

        # Arabic text — LARGE
        ar_font = get_font(54)
        ar_lines = wrap_text(data["arabic"], ar_font, content_width, draw)
        for line in ar_lines:
            y = draw_centered_text(draw, y, line, ar_font, theme["text"], W)
        y += 25

        # Decorative separator
        draw_decorative_line(draw, y + 5, W, theme["accent"])
        y += 25

        # Translation — large and readable
        tr_font = get_font(34)
        tr_lines = wrap_text(f'"{data["translation"]}"', tr_font, content_width, draw)
        for line in tr_lines:
            y = draw_centered_text(draw, y, line, tr_font, theme["subtext"], W)
        y += 20

        # Reference — bold
        ref_font = get_font(28, bold=True)
        y = draw_centered_text(draw, y, data["reference"], ref_font, theme["accent"], W)

    elif post_type == "hadith":
        # Type badge
        badge_font = get_font(22, bold=True)
        y = draw_centered_text(draw, y, "🕌  HADITH OF THE DAY", badge_font, theme["accent"], W)
        y += 20

        # Decorative line
        draw_decorative_line(draw, y + 5, W, theme["accent"])
        y += 25

        # Hadith text — large
        ht_font = get_font(36)
        ht_lines = wrap_text(f'"{data["text"]}"', ht_font, content_width, draw)
        for line in ht_lines:
            y = draw_centered_text(draw, y, line, ht_font, theme["text"], W)
        y += 25

        # Decorative separator
        draw_decorative_line(draw, y + 5, W, theme["accent"])
        y += 25

        # Source
        src_font = get_font(28, bold=True)
        y = draw_centered_text(draw, y, "📌 " + data["source"], src_font, theme["accent"], W)
        y += 10
        y = draw_centered_text(draw, y, "👤 Prophet Muhammad ﷺ", src_font, theme["subtext"], W)

    elif post_type == "dhikr":
        # Type badge
        badge_font = get_font(22, bold=True)
        y = draw_centered_text(draw, y, "🤲  DHIKR OF THE DAY", badge_font, theme["accent"], W)
        y += 20

        # Arabic dhikr — VERY LARGE
        ar_font = get_font(72)
        y = draw_centered_text(draw, y, data["arabic"], ar_font, theme["text"], W)
        y += 25

        # Transliteration — large
        tr_font = get_font(40)
        y = draw_centered_text(draw, y, data["transliteration"], tr_font, theme["accent"], W)
        y += 15

        # Meaning
        mn_font = get_font(30)
        y = draw_centered_text(draw, y, data["meaning"], mn_font, theme["subtext"], W)
        y += 30

        # Count badge — big and bold
        cnt_font = get_font(36, bold=True)
        y = draw_centered_text(draw, y, "🔢  Repeat " + str(data["count"]) + " times", cnt_font, theme["accent"], W)

    elif post_type == "dua":
        # Type badge
        badge_font = get_font(22, bold=True)
        y = draw_centered_text(draw, y, "🤲  DUA OF THE DAY", badge_font, theme["accent"], W)
        y += 20

        # Arabic dua — large
        ar_font = get_font(50)
        ar_lines = wrap_text(data["arabic"], ar_font, content_width, draw)
        for line in ar_lines:
            y = draw_centered_text(draw, y, line, ar_font, theme["text"], W)
        y += 20

        # Transliteration
        tr_font = get_font(26)
        tr_lines = wrap_text(data["transliteration"], tr_font, content_width, draw)
        for line in tr_lines:
            y = draw_centered_text(draw, y, line, tr_font, theme["subtext"], W)
        y += 15

        # Meaning
        mn_font = get_font(30)
        mn_lines = wrap_text(data["meaning"], mn_font, content_width, draw)
        for line in mn_lines:
            y = draw_centered_text(draw, y, line, mn_font, theme["text"], W)
        y += 15

        # Source
        src_font = get_font(26, bold=True)
        y = draw_centered_text(draw, y, "📌 " + data["source"], src_font, theme["accent"], W)

    elif post_type == "reminder":
        # Emoji big
        emoji_font = get_font(60)
        y = draw_centered_text(draw, y, data.get("emoji", "✨"), emoji_font, theme["text"], W)
        y += 10

        # Title — LARGE and bold
        title_font = get_font(44, bold=True)
        title_lines = wrap_text(data["title"], title_font, content_width, draw)
        for line in title_lines:
            y = draw_centered_text(draw, y, line, title_font, theme["accent"], W)
        y += 20

        # Decorative line
        draw_decorative_line(draw, y + 5, W, theme["accent"])
        y += 25

        # Reminder text — large and readable
        rm_font = get_font(32)
        rm_lines = wrap_text(data["text"], rm_font, content_width, draw)
        for line in rm_lines:
            y = draw_centered_text(draw, y, line, rm_font, theme["text"], W)

    elif post_type == "prayer_times":
        # Type badge
        badge_font = get_font(22, bold=True)
        y = draw_centered_text(draw, y, "🕌  TODAY'S PRAYER TIMES", badge_font, theme["accent"], W)
        y += 15

        # Hijri date
        if prayer_info:
            hj_font = get_font(26)
            y = draw_centered_text(draw, y, prayer_info.get("hijri_date", ""), hj_font, theme["subtext"], W)
        y += 20

        # Decorative line
        draw_decorative_line(draw, y + 5, W, theme["accent"])
        y += 25

        # Prayer times — large table
        if prayer_info:
            prayers = [
                ("🌙 Fajr", prayer_info.get("fajr", "--")),
                ("🌅 Sunrise", prayer_info.get("sunrise", "--")),
                ("☀️ Dhuhr", prayer_info.get("dhuhr", "--")),
                ("🌤️ Asr", prayer_info.get("asr", "--")),
                ("🌇 Maghrib", prayer_info.get("maghrib", "--")),
                ("🌑 Isha", prayer_info.get("isha", "--")),
            ]
            pt_font = get_font(34, bold=True)
            for name, time in prayers:
                text = f"{name}    {time}"
                y = draw_centered_text(draw, y, text, pt_font, theme["text"], W)
                y += 12

    # ====== ENGAGEMENT SECTION ======
    y = max(y + 25, card_bottom - 100)

    # Engagement question
    eq = random.choice(ENGAGEMENT_QUESTIONS)
    eq_font = get_font(22)
    eq_lines = wrap_text(eq, eq_font, content_width, draw)
    for line in eq_lines:
        y = draw_centered_text(draw, y, line, eq_font, theme["subtext"], W, shadow=False)
    y += 10

    # Hashtags
    tag_font = get_font(18)
    tags = "#IslamicReminder #Quran #Hadith #Muslim"
    y = draw_centered_text(draw, y, tags, tag_font, (*theme["accent"], 150), W, shadow=False)

    # Save
    filename = "islamic_post_{}_{}.jpg".format(
        post_type, datetime.now(IST).strftime('%Y%m%d_%H%M%S'))
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath, "JPEG", quality=95)
    return filepath


def generate_caption(post_type, data, prayer_info=None):
    """Generate text caption for the post."""
    if post_type == "quran_verse":
        return (
            "📖 *Quran Verse of the Day*\n\n"
            f"_{data['translation']}_\n\n"
            f"📌 {data['reference']}\n\n"
            "💬 Which verse touches your heart today? Share below!\n\n"
            "#Quran #VerseOfTheDay #IslamicReminder"
        )
    elif post_type == "hadith":
        return (
            "🕌 *Hadith of the Day*\n\n"
            f"_{data['text']}_\n\n"
            f"📌 {data['source']}\n"
            "👤 Prophet Muhammad ﷺ\n\n"
            "💬 How do you apply this hadith in your daily life?\n\n"
            "#Hadith #Sunnah #IslamicReminder"
        )
    elif post_type == "dhikr":
        return (
            "🤲 *Dhikr of the Day*\n\n"
            f"_{data['transliteration']}_\n"
            f"Meaning: {data['meaning']}\n\n"
            f"🔢 Repeat: {data['count']} times\n\n"
            "💬 Tag someone who needs this dhikr today!\n\n"
            "#Dhikr #RemembranceOfAllah #IslamicReminder"
        )
    elif post_type == "dua":
        return (
            "🤲 *Dua of the Day*\n\n"
            f"_{data['transliteration']}_\n\n"
            f"Meaning: _{data['meaning']}_\n\n"
            f"📌 {data['source']}\n\n"
            "💬 Save this dua and share it with someone who needs it!\n\n"
            "#Dua #IslamicReminder #Quran"
        )
    elif post_type == "reminder":
        return (
            f"{data.get('emoji', '✨')} *{data['title']}*\n\n"
            f"{data['text']}\n\n"
            "💬 Share this reminder and spread the barakah!\n\n"
            "#IslamicReminder #Muslim #Deen"
        )
    elif post_type == "prayer_times":
        lines = ["🕌 *Today's Prayer Times*\n"]
        if prayer_info:
            lines.append("📅 {}\n".format(prayer_info.get('hijri_date', '')))
            lines.append("```")
            lines.append("{:<14} │ {:<8}".format("Prayer", "Time"))
            lines.append("─────────────────────")
            for name in ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]:
                key = name.lower()
                lines.append("{:<14} │ {:<8}".format(name, prayer_info.get(key, '--')))
            lines.append("```")
        lines.append("\n💬 Which prayer do you never miss? Comment below!\n")
        lines.append("#PrayerTimes #Salah #IslamicReminder")
        return "\n".join(lines)
    return ""


POST_TYPES = ["quran_verse", "hadith", "dhikr", "dua", "reminder", "prayer_times"]


def generate_post(post_type=None, lat=DEFAULT_LAT, lon=DEFAULT_LON):
    """Generate a complete Islamic post with image and caption."""
    if post_type is None:
        post_type = random.choice(POST_TYPES)

    data = None
    prayer_info = None

    if post_type == "quran_verse":
        data = random.choice(QURAN_VERSES)
    elif post_type == "hadith":
        data = random.choice(HADITH_COLLECTION)
    elif post_type == "dhikr":
        data = random.choice(DHIKR_COLLECTION)
    elif post_type == "dua":
        data = random.choice(DUA_COLLECTION)
    elif post_type == "reminder":
        data = random.choice(ISLAMIC_REMINDERS)
    elif post_type == "prayer_times":
        prayer_info = get_prayer_times(lat, lon)
        data = {}

    image_path = generate_image(post_type, data, prayer_info)
    caption = generate_caption(post_type, data, prayer_info)

    return {
        "post_type": post_type,
        "caption": caption,
        "image_path": image_path,
        "prayer_info": prayer_info,
        "timestamp": datetime.now(IST).strftime("%Y-%m-%d %H:%M IST"),
    }


def main():
    post_type = None
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower().replace("-", "_")
        type_map = {"quran": "quran_verse", "verse": "quran_verse", "prayer": "prayer_times", "prayertimes": "prayer_times"}
        post_type = type_map.get(arg, arg if arg in POST_TYPES else None)

    post = generate_post(post_type)

    output_path = os.path.join(OUTPUT_DIR, "output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)

    try:
        print("Type: {}".format(post['post_type']))
        print("Time: {}".format(post['timestamp']))
        if post.get('image_path'):
            print("Image: {}".format(post['image_path']))
        print("\n--- CAPTION ---")
        print(post['caption'])
        print("--- END ---")
    except UnicodeEncodeError:
        print("Type: {}".format(post['post_type']))
        print("Image: {}".format(post.get('image_path', 'N/A')))
        print("Output: {}".format(output_path))


if __name__ == "__main__":
    main()
