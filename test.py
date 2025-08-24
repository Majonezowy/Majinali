from youtubesearchpython import VideosSearch
from typing import Optional

def fetch_video_url(query: str) -> Optional[str]:
    video_search = VideosSearch(query, limit=1)
    results = video_search.result()['result']
    if results:
        return results[0]['link']
    return None

# Example usage
url = fetch_video_url("Python tutorial")
print(url)
