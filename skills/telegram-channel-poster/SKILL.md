---
name: telegram-channel-poster
description: Generate movie/TV show posts from IMDB or TMDB IDs using the fb_post_maker script, then post them with banner images to a Telegram channel. Trigger when the user provides an IMDB/TMDB ID and wants it posted to their Telegram channel.
---

# Telegram Channel Poster

Generate formatted movie/TV posts and publish them to a Telegram channel with banner images.

## Workflow

1. **Get the ID** — User provides an IMDB ID (e.g., `tt1234567`) or TMDB ID (e.g., `1339713`).
2. **Run the post generator** — Execute `scripts/generate_post.py` with the ID.
3. **Read the output** — The script writes results to `output.json` in the working directory.
4. **Post to Telegram** — Use OWL's `message` tool to send the post text + banner image to the channel.

## Key Paths

- **Script**: `C:\Users\pasindu\Desktop\automation\fb_post_maker\scripts\generate_post.py`
- **Working directory**: `C:\Users\pasindu\Desktop\automation\fb_post_maker`
- **Banner folder**: `C:\Users\pasindu\Desktop\automation\fb_post_maker\fb_banners\`
- **Output file**: `C:\Users\pasindu\Desktop\automation\fb_post_maker\output.json`
- **Telegram channel ID**: `-1003809102397`

## Running the Script

```powershell
cd "C:\Users\pasindu\Desktop\automation\fb_post_maker"
python scripts\generate_post.py <ID>
```

The script will:
1. For **numeric IDs** (e.g., `1339713`): Try direct TMDB lookup first (movie, then TV)
2. For **tt-prefixed IDs** (e.g., `tt1234567`): Try IMDB external lookup via TMDB `/find` endpoint
3. As fallback, numeric IDs are also tried as IMDB (`tt<ID>`)
4. Download the banner image to `fb_banners/` as `<tmdb_id>_<type>.jpg`
5. Write `output.json` with `post_text`, `image`, `title`, `year`, `rating`, `media_type`, `tmdb_id`

**Important:** Numeric TMDB IDs are now tried directly first. Previously they were incorrectly prefixed with `tt` which could return wrong results (e.g., TMDB `1339713` → "Obsession (2026)" was incorrectly resolved as "CSI: NY").

## Posting to Telegram

After getting `output.json`:

1. Read the file
2. Call OWL's `message` tool with:
   - `content`: the `post_text` value
   - `channel`: `telegram`
   - `chat_id`: `-1003809102397`
   - `media`: array with the `image` path

## Important Notes

- Banner images are saved as `<tmdb_id>_<type>.jpg` in the `fb_banners/` folder
- The watch link format is: `https://www.vidbanda.duckdns.org/details/<type>/<tmdb_id>`
- Always post both the text and the banner image together
- The script handles Windows Unicode output issues with a safe print fallback
