
import re
from urllib.parse import parse_qs, urlparse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api import RequestBlocked, IpBlocked

from cache import ClipboardCache
from config import Config
# from copyq import get_lastest_clipboard
from dunstify import notify_cont
from exceptions import ContentNotFoundError, YouTubeExtractionError


def ts_format(ts):
    sec = int(ts['start'])
    hours, remainder = divmod(sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    hhmmss = f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"
    return f"{hhmmss}\n{ts['text']}"


def ts_merge(ts1, ts2 = None):
    sec = int(ts1['start'])
    hours, remainder = divmod(sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    hhmmss = f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"
    if ts2:
        return f"{hhmmss}\n{ts1['text']} {ts2['text']}"
    else:
        return f"{hhmmss}\n{ts1['text']}"


def get_youtube_videoid(url: str) -> str:
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    parsed_url = urlparse(url)
    if "youtube.com" in parsed_url.netloc:
        params = parse_qs(parsed_url.query)
        if "v" in params:
            return params["v"][0]
    raise ValueError(f"지원하지 않는 YouTube URL 형식: {url}")


def download_transcript(
    video_id: str = "",
    language_codes: list[str] = ['en', 'ko'],
):
    notify_cont("youtube summary", f"get youtube transcript: {video_id}")

    # raise RequestBlocked("Test Blocked by youtube")

    # video_id = get_youtube_videoid(video_url)
    ytt_api = YouTubeTranscriptApi()
    try:
        transcript_list = ytt_api.list(video_id)
        try:
            transcript = transcript_list.find_manually_created_transcript(language_codes)
        except Exception as e:
            transcript = transcript_list.find_generated_transcript(language_codes)

        transcript = transcript.fetch(preserve_formatting=False)

        print(f"Selected transcript info:")
        print(f"  - 언어: {transcript.language} ({transcript.language_code})")
        print(f"  - 자동 생성: {transcript.is_generated}")
        if getattr(transcript, "translation_languages", False):
            print(f"  - 번역 가능 언어: {getattr(transcript, 'translation_languages')}")

        raw_data = transcript.to_raw_data()
        merged_segments = [ts_merge(*raw_data[i:i+2]) for i in range(0, len(raw_data), 2)]
        return '\n'.join(merged_segments)
    except (RequestBlocked, IpBlocked) as e:
        raise e
    except Exception as e:
        raise ValueError(f"Transcript download failed for {video_id}: {e}") from e


#
#
#
def get_youtube_content(url:str, transcript:str = "") -> dict:

    assert ('youtube.com/watch' in url or 'youtu.be/' in url)
    video_id = get_youtube_videoid(url)

    timestamps = re.findall(r'\n\d+:\d+\n', transcript)
    if len(timestamps) < 10:
        try:
            transcript = download_transcript(video_id)
        except Exception as e:
            ClipboardCache.save(url, "wait transcript")
            raise YouTubeExtractionError(f"Failed to get transcript for `{video_id}`: {e}")

    return {"video_id": video_id, "transcript": transcript}


if __name__ == '__main__':
    print(download_transcript("k_5NcmxWlVg"))
