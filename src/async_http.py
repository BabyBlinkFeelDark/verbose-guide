import asyncio
import json
from aiohttp import ClientSession, ClientTimeout, ClientError

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]

async def fetch_urls(urls: list[str], file_path: str):
    semaphore = asyncio.Semaphore(5)
    status_dict = {}

    async def fetch(url: str):
        async with semaphore:
            try:
                async with ClientSession(timeout=ClientTimeout(total=10)) as session:
                    async with session.get(url) as response:
                        status_dict[url] = response.status
            except (ClientError, asyncio.TimeoutError, Exception) as e:
                status_dict[url] = 0

    await asyncio.gather(*(fetch(url) for url in urls))

    with open(file_path, "a") as f:
        for url, status in status_dict.items():
            json.dump({"url": url, "status_code": status}, f)
            f.write("\n")

if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))
