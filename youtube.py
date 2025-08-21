
from urllib.parse import parse_qs, urlparse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api import RequestBlocked, IpBlocked
import subprocess

def ts_format(ts):
    sec = int(ts['start'])
    hours, remainder = divmod(sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    hhmmss = f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"
    return f"{hhmmss}\n{ts['text']}"


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
    subprocess.run(["notify-send", "running", f"get youtube transcript: {video_id}"], check=False)

    # video_id = get_youtube_videoid(video_url)
    ytt_api = YouTubeTranscriptApi()
    try:
        transcript_list = ytt_api.list(video_id)
        try:
            transcript = transcript_list.find_manually_created_transcript(language_codes)
        except Exception as e:
            transcript = transcript_list.find_generated_transcript(language_codes)

        transcript = transcript.fetch(preserve_formatting=False)

        print(f"선택된 자막 정보:")
        print(f"  - 언어: {transcript.language} ({transcript.language_code})")
        print(f"  - 자동 생성: {transcript.is_generated}")
        if getattr(transcript, "translation_languages", False):
            print(f"  - 번역 가능 언어: {getattr(transcript, 'translation_languages')}")

        return '\n'.join( map(ts_format, transcript.to_raw_data()) )
    except (RequestBlocked, IpBlocked) as e:
        raise e
    except Exception as e:
        raise ValueError(f"자막 다운로드 실패: {video_id}: {e}") from e


if __name__ == '__main__':
    print(download_transcript("https://www.youtube.com/watch?v=k_5NcmxWlVg"))
