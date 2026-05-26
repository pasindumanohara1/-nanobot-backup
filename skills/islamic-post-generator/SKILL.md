---
name: islamic-post-generator
description: Generate Islamic engagement posts (Quran verses, Hadith, Dhikr, Dua, reminders) for social media. Trigger when the user wants to create Islamic/religious content for posting.
---

# Islamic Post Generator with Images

Generate beautiful Islamic content **with images** for social media posts.

## Usage

```powershell
cd "C:\Users\pasindu\.nanobot\workspace\skills\islamic-post-generator"
python generate_post.py [type]
```

## Post Types

| Type | Argument | Description |
|------|----------|-------------|
| Random | (none) | Randomly picks a type |
| Quran Verse | `quran` | Arabic text + translation + reference |
| Hadith | `hadith` | Hadith text + source + narrator |
| Dhikr | `dhikr` | Arabic dhikr + transliteration + meaning + count |
| Dua | `dua` | Arabic dua + transliteration + meaning + source |
| Reminder | `reminder` | Islamic reminders about charity, patience, gratitude, etc. |
| Prayer Times | `prayer` | Today's prayer times from AlAdhan API (Colombo, Sri Lanka) |

## APIs Used

- **AlAdhan API** (`https://api.aladhan.com/v1/`) — Prayer times, Hijri date conversion
  - Calculation method: Muslim World League (method=2)
  - Default location: Colombo, Sri Lanka (6.9271, 79.8612)

## Image Generation

Each post generates a **1080x1080px JPEG image** with:
- Beautiful gradient backgrounds (5 color themes: Navy, Green, Purple, Maroon, Teal)
- Islamic-style decorative borders with gold accents
- Bismillah header
- Proper Arabic text rendering
- Footer with date and hashtags

## Output

The script writes to `output.json` in the skill directory:
- `post_type`: Type of post
- `caption`: Full formatted caption (Telegram markdown)
- `image_path`: Path to generated JPEG image
- `prayer_info`: Prayer times data (if applicable)
- `timestamp`: Current IST time

## Posting to Telegram

After generating, read `output.json` and use OWL's `message` tool:
- `content`: the `caption` value
- `media`: array with the `image_path` value
- `channel`: `telegram`
- `chat_id`: target channel/chat ID

## Content Database

Built-in database includes:
- 12 Quran verses (Arabic + English translation)
- 10 Hadith from Bukhari, Muslim, and other sources
- 7 Dhikr with counts
- 6 Dua from Quran and Sunnah
- 8 Islamic reminders

## Extending

Edit `generate_post.py` to add more content to the respective lists, or add new color themes in `THEMES`.
