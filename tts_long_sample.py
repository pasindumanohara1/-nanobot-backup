"""Generate long TTS samples from both gTTS and edge-tts."""
import asyncio
import os
import time

TEXT = (
    "In the name of Allah, the Most Gracious, the Most Merciful. "
    "All praise is due to Allah, Lord of all the worlds. "
    "The Most Gracious, the Most Merciful. "
    "Master of the Day of Judgment. "
    "You alone we worship, and You alone we ask for help. "
    "Guide us to the straight path. "
    "The path of those upon whom You have bestowed favor, not of those who have earned Your anger, nor of those who are astray. "
    "This is the opening chapter of the Holy Quran, known as Al-Fatiha, the Mother of the Book. "
    "It is recited in every unit of the daily prayers, making it the most frequently recited verses in the world. "
    "The Prophet Muhammad, peace be upon him, said that no prayer is complete without the recitation of Al-Fatiha. "
    "This beautiful chapter encapsulates the essence of our relationship with our Creator — acknowledging His sovereignty, "
    "His mercy, and our complete dependence on His guidance. "
    "May Allah guide us all to the straight path, Ameen."
)

OUT_DIR = r"C:\Users\pasindu\.nanobot\workspace"


def run_gtts():
    from gtts import gTTS
    print("Generating gTTS...")
    t0 = time.time()
    tts = gTTS(text=TEXT, lang="en", tld="co.uk", slow=False)
    path = os.path.join(OUT_DIR, "tts_gtts_long.mp3")
    tts.save(path)
    print(f"gTTS done in {time.time()-t0:.1f}s -> {path}")
    return path


def run_edge():
    import edge_tts

    async def _gen():
        print("Generating edge-tts (Jenny)...")
        t0 = time.time()
        communicate = edge_tts.Communicate(TEXT, "en-US-JennyNeural")
        path = os.path.join(OUT_DIR, "tts_edge_jenny_long.mp3")
        await communicate.save(path)
        print(f"edge-tts Jenny done in {time.time()-t0:.1f}s -> {path}")

        print("Generating edge-tts (Guy)...")
        t0 = time.time()
        communicate2 = edge_tts.Communicate(TEXT, "en-US-GuyNeural")
        path2 = os.path.join(OUT_DIR, "tts_edge_guy_long.mp3")
        await communicate2.save(path2)
        print(f"edge-tts Guy done in {time.time()-t0:.1f}s -> {path2}")

    asyncio.run(_gen())


if __name__ == "__main__":
    run_gtts()
    run_edge()
    print("\nAll done!")
