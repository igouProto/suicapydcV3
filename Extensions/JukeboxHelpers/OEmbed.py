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

    print(oembed_url)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(oembed_url) as response:
                
                print(response)
                
                if response.status != 200:
                    raise OEmbedFetchError(f"oEmbed fetch failed with status {response.status}")

                data = await response.json()
                return {
                    "title": data.get("title"),
                    "author": data.get("author_name")
                }
    except aiohttp.ClientError as e:
        raise OEmbedFetchError(f"Network error: {e}") from e
