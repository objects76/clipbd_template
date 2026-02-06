import re
import webbrowser
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import IpBlocked, RequestBlocked, YouTubeTranscriptApi

from cache import ClipboardCache

# from copyq import get_lastest_clipboard
from exceptions import YouTubeExtractionError
from ui import dunst


def ts_format(ts):
    sec = int(ts["start"])
    hours, remainder = divmod(sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    hhmmss = (
        f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"
    )
    return f"{hhmmss}\n{ts['text']}"


def ts_merge(ts1, ts2=None):
    sec = int(ts1["start"])
    hours, remainder = divmod(sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    hhmmss = (
        f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"
    )
    if ts2:
        return f"{hhmmss}\n{ts1['text']} {ts2['text']}"
    return f"{hhmmss}\n{ts1['text']}"


def get_youtube_videoid(url: str) -> str:
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    parsed_url = urlparse(url)
    if "youtube.com" in parsed_url.netloc:
        params = parse_qs(parsed_url.query)
        if "v" in params:
            return params["v"][0]
    raise YouTubeExtractionError(f"Unsupported YouTube URL format: {url}")


def download_transcript(
    video_id: str = "",
    language_codes: list[str] | None = None,
):
    language_codes = language_codes or ["en", "ko"]
    dunst("youtube summary", "information", f"get youtube transcript: {video_id}", msgid=1)
    # raise RequestBlocked("Test Blocked by youtube")

    # video_id = get_youtube_videoid(video_url)
    ytt_api = YouTubeTranscriptApi()
    try:
        transcript_list = ytt_api.list(video_id)

        # Get available languages
        available_languages = []
        for transcript in transcript_list:
            available_languages.append(transcript.language_code)

        # Try to find a matching language (including variants like en-US for en)
        matched_codes = []
        for pref_code in language_codes:
            for avail_code in available_languages:
                if avail_code == pref_code or avail_code.startswith(pref_code + "-"):
                    matched_codes.append(avail_code)
                    break

        # If no match found, use any available language
        if not matched_codes:
            matched_codes = available_languages[:1]  # Use first available

        try:
            transcript = transcript_list.find_manually_created_transcript(matched_codes)
        except Exception:
            transcript = transcript_list.find_generated_transcript(matched_codes)

        transcript = transcript.fetch(preserve_formatting=False)

        print("Selected transcript info:")
        print(f"  - 언어: {transcript.language} ({transcript.language_code})")
        print(f"  - 자동 생성: {transcript.is_generated}")
        if getattr(transcript, "translation_languages", False):
            print(f"  - 번역 가능 언어: {transcript.translation_languages}")

        raw_data = transcript.to_raw_data()
        merged_segments = [
            ts_merge(*raw_data[i : i + 2]) for i in range(0, len(raw_data), 2)
        ]
        return "\n".join(merged_segments)
    except (RequestBlocked, IpBlocked) as e:
        raise e
    except Exception as e:
        raise YouTubeExtractionError(
            f"Transcript download failed for {video_id}: {e}"
        ) from e


def get_youtube_content(url: str, transcript: str = "") -> dict:
    assert "youtube.com/watch" in url or "youtu.be/" in url
    video_id = get_youtube_videoid(url)

    timestamps = re.findall(r"\n\d+:\d+\n", transcript)
    if len(timestamps) < 10:
        try:
            transcript = download_transcript(video_id)
        except Exception as e:
            ClipboardCache.save(url, "wait transcript")
            dunst("Error", "error", str(e), 5)
            transcript = ""
            # raise YouTubeExtractionError(f"Failed to get transcript for `{video_id}`: {e}")

    return {"video_id": video_id, "transcript": transcript}


def play_youtube_video(video_id: str):
    # set edge://flags, autoplay: enable
    url = f"https://www.youtube.com/embed/{video_id}?start=10&end=30&autoplay=1"
    webbrowser.open(url, new=2)  # new=2 for new tab


if __name__ == "__main__":
    # print(download_transcript("9ctOnQKoxv8"))
    # https://www.youtube.com/embed/9ctOnQKoxv8?start=10&end=30&autoplay=1
    print("\nTesting play_youtube_video function:")
    play_youtube_video("9ctOnQKoxv8")
