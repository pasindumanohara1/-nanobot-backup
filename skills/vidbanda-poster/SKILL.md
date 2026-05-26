---
name: vidbanda-poster
description: Generate movie/TV poster banner and post to Telegram channel using TMDB/IMDB IDs. Trigger when the user provides a TMDB or IMDB ID and wants a movie/TV post created and published to their Telegram channel.
---

# Vidbanda Movie Poster

Generate formatted movie/TV posts with banner images and publish to Telegram.

## Workflow

1. **Get the ID** — User provides an IMDB ID (`tt1234567`) or TMDB ID (`1339713`).
2. **Run the generator** — Execute `generate_post.py` with the ID.
3. **Read output** — Script writes `output.json` in the working directory.
4. **Post to Telegram** — Use OWL's `message` tool to send text + banner image.

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

**ID resolution order:**
- **Numeric IDs** (e.g., `1339713`): Try TMDB direct lookup first (movie, then TV), then fall back to IMDB (`tt<ID>`)
- **tt-prefixed IDs** (e.g., `tt1234567`): Use TMDB `/find` endpoint for IMDB external lookup

The script downloads the banner to `fb_banners/<tmdb_id>_<type>.jpg` and writes `output.json` with `post_text`, `image`, `title`, `year`, `rating`, `media_type`, `tmdb_id`.

## Posting to Telegram

After getting `output.json`:

1. Read the file
2. Call OWL's `message` tool with:
   - `content`: the `post_text` value
   - `channel`: `telegram`
   - `chat_id`: `-1003809102397`
   - `media`: array with the `image` path

## Important Notes

- Watch link format: `https://www.vidbanda.duckdns.org/details/<type>/<tmdb_id>`
- Banner naming: `<tmdb_id>_<type>.jpg`
- Always post both text and banner image together
- Numeric TMDB IDs are tried directly first — previously they were incorrectly prefixed with `tt`, causing wrong matches (e.g., `1339713` → "CSI: NY" instead of "Obsession (2026)")
