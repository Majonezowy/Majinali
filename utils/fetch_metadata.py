from typing import Optional
from bs4 import BeautifulSoup
import aiohttp

async def fetch_metadata(url: str) -> dict[str, Optional[str]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=5) as resp:
            html = await resp.text(errors="ignore")
            soup = BeautifulSoup(html, "html.parser")

            # OpenGraph / fallback
            title = soup.find("meta", property="og:title") or soup.find("title")
            desc = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
            icon = soup.find("link", rel="icon") or soup.find("link", rel="shortcut icon")

            return {
                "title": title.get("content") if title and title.has_attr("content") else title.string if title else None,
                "description": desc.get("content") if desc else None,
                "icon": icon.get("href") if icon else None
            }


