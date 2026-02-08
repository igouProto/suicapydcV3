import aiohttp
import logging
from urllib.parse import quote

log = logging.getLogger(__name__)


class OEmbedFetchError(Exception):
    """Raised when oEmbed fetch fails."""
    pass


async def fetch_youtube_oembed(url: str) -> dict:
    """
    Fetch title and author from YouTube's oEmbed API.

    Args:
        url: A YouTube video URL (e.g., https://youtube.com/watch?v=xxx)

    Returns:
        dict with 'title' and 'author' keys

    Raises:
        OEmbedFetchError: If the fetch fails for any reason
    """
    oembed_url = f"https://www.youtube.com/oembed?url={quote(url, safe='')}&format=json"

    log.info(f"[OEmbed] Fetching oEmbed for URL: {url}")
    log.info(f"[OEmbed] Constructed oEmbed URL: {oembed_url}")

    try:
        log.info("[OEmbed] Creating aiohttp session...")
        async with aiohttp.ClientSession() as session:
            log.info("[OEmbed] Sending GET request...")
            async with session.get(oembed_url) as response:
                log.info(f"[OEmbed] Response status: {response.status}")
                log.info(f"[OEmbed] Response headers: {dict(response.headers)}")

                if response.status != 200:
                    body = await response.text()
                    log.error(f"[OEmbed] Non-200 response body: {body[:500]}")
                    raise OEmbedFetchError(f"oEmbed fetch failed with status {response.status}: {body[:200]}")

                raw_body = await response.text()
                log.info(f"[OEmbed] Raw response body: {raw_body[:500]}")

                import json
                data = json.loads(raw_body)
                result = {
                    "title": data.get("title"),
                    "author": data.get("author_name")
                }
                log.info(f"[OEmbed] Parsed result: {result}")
                return result
    except aiohttp.ClientError as e:
        log.exception(f"[OEmbed] aiohttp ClientError: {e}")
        raise OEmbedFetchError(f"Network error: {e}") from e
    except Exception as e:
        log.exception(f"[OEmbed] Unexpected error: {type(e).__name__}: {e}")
        raise OEmbedFetchError(f"Unexpected error: {type(e).__name__}: {e}") from e
