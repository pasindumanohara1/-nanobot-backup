#!/usr/bin/env python3
"""
Generate a movie/TV post from an IMDB or TMDB ID.
Writes output.json with post_text, image path, title, year, rating.

Usage:
    python generate_post.py <ID>

Examples:
    python generate_post.py tt22084616
    python generate_post.py 1304313
"""

import sys
import os
import json
import requests

# ====== CONFIGURATION ======
API_KEY = "aa4f947818d885e4addb8684a408dbaf"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYTRmOTQ3ODE4ZDg4NWU0YWRkYjg2ODRhNDA4ZGJhZiIsIm5iZiI6MTc0MjE2MDg1NC44NjMwMDAyLCJzdWIiOiI2N2Q3NDNkNjE5MTg2OGM1NGZmMWE3ZTgiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.XtAFXOqSCManan03Rq_6Iguf-Nkk8QaLQvgDFZXSHr8"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/original"
WATCH_BASE = "https://www.vidbanda.duckdns.org/details"
SAVE_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "fb_post_maker", "fb_banners")
SAVE_FOLDER = os.path.normpath(SAVE_FOLDER)

WORKING_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "fb_post_maker"))

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}


def find_media(user_input):
    """Try IMDB ID first, then fall back to TMDB ID."""
    clean_imdb = user_input if user_input.startswith("tt") else f"tt{user_input}"

    # Attempt 1: IMDB lookup
    url = f"{BASE_URL}/find/{clean_imdb}"
    params = {"external_source": "imdb_id", "language": "en-US", "include_adult": "true"}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("movie_results"):
            return "movie", data["movie_results"][0]["id"]
        elif data.get("tv_results"):
            return "tv", data["tv_results"][0]["id"]
        elif data.get("tv_episode_results"):
            show_id = data["tv_episode_results"][0].get("show_id")
            if show_id:
                return "tv", show_id

    # Attempt 2: Direct TMDB ID
    for m_type in ["movie", "tv"]:
        url = f"{BASE_URL}/{m_type}/{user_input}"
        params = {"language": "en-US", "api_key": API_KEY, "include_adult": "true"}
        resp = requests.get(url, headers=HEADERS, params=params)
        if resp.status_code == 200:
            return m_type, user_input

    return None, None


def get_details(tmdb_id, media_type):
    url = f"{BASE_URL}/{media_type}/{tmdb_id}"
    params = {"language": "en-US", "api_key": API_KEY, "append_to_response": "external_ids", "include_adult": "true"}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def download_image(image_url, filename):
    os.makedirs(SAVE_FOLDER, exist_ok=True)
    filepath = os.path.join(SAVE_FOLDER, filename)
    response = requests.get(image_url, stream=True, timeout=30)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filepath
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_post.py <IMDB_or_TMDB_ID>")
        sys.exit(1)

    user_input = sys.argv[1].strip()
    print(f"Looking up ID: {user_input}")

    media_type, tmdb_id = find_media(user_input)
    if not media_type:
        print("ERROR: No movie or TV show found for this ID.")
        sys.exit(1)

    print(f"Found: {media_type.upper()} (TMDB ID: {tmdb_id})")

    details = get_details(tmdb_id, media_type)
    title = details.get("title") or details.get("name", "Unknown Title")
    date_str = details.get("release_date") or details.get("first_air_date", "")
    year = date_str[:4] if date_str else ""
    overview = details.get("overview", "No description available.")
    backdrop = details.get("backdrop_path")
    poster = details.get("poster_path")
    rating = details.get("vote_average", 0)

    # Download banner
    banner_path = backdrop or poster
    saved_image = None
    if banner_path:
        banner_url = f"{IMAGE_BASE}{banner_path}"
        image_filename = f"{tmdb_id}_{media_type}.jpg"
        saved_image = download_image(banner_url, image_filename)
        if saved_image:
            print(f"Banner saved: {saved_image}")

    # Build post
    watch_link = f"{WATCH_BASE}/{media_type}/{tmdb_id}"
    title_line = f"{title} ({year})" if year else title
    rating_str = f"Rating: {rating:.1f}/10" if rating else ""

    post_lines = ["watch now", title_line]
    if rating_str:
        post_lines.append(rating_str)
    post_lines.append("")
    post_lines.append(overview)
    post_lines.append("")
    post_lines.append(watch_link)

    post_text = "\n".join(post_lines)

    # Write output
    output = {
        "post_text": post_text,
        "image": saved_image,
        "title": title,
        "year": year,
        "rating": str(rating),
        "media_type": media_type,
        "tmdb_id": str(tmdb_id),
    }

    output_path = os.path.join(WORKING_DIR, "output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nOutput written to: {output_path}")
    print(f"Title: {title} ({year})")
    print(f"Rating: {rating}")
    print(f"Banner: {saved_image}")
    print("\n--- POST PREVIEW ---")
    print(post_text)
    print("--- END ---")


if __name__ == "__main__":
    main()
