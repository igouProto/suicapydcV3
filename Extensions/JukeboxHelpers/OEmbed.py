import asyncio
import aiohttp
import logging
import socket
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

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        connector = aiohttp.TCPConnector(family=socket.AF_INET)  # Force IPv4
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            async with session.get(oembed_url) as response:
                if response.status != 200:
                    body = await response.text()
                    log.error(f"[OEmbed] Failed with status {response.status}: {body[:200]}")
                    raise OEmbedFetchError(f"oEmbed fetch failed with status {response.status}")

                data = await response.json()
                return {
                    "title": data.get("title"),
                    "author": data.get("author_name")
                }
    except asyncio.TimeoutError as e:
        log.error("[OEmbed] Request timed out")
        raise OEmbedFetchError("Request timed out") from e
    except aiohttp.ClientError as e:
        log.error(f"[OEmbed] Network error: {e}")
        raise OEmbedFetchError(f"Network error: {e}") from e
    except OEmbedFetchError:
        raise
    except Exception as e:
        log.error(f"[OEmbed] Unexpected error: {type(e).__name__}: {e}")
        raise OEmbedFetchError(f"Unexpected error: {e}") from e
