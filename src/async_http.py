import asyncio
import json
import aiofiles
from aiohttp import ClientSession, ClientTimeout, ClientError

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
]


def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def fetch_urls(urls: list[str], file_path: str, batch_size: int = 100):
    semaphore = asyncio.Semaphore(20)
    queue = asyncio.Queue()

    async def fetch(url: str, session: ClientSession):
        async with semaphore:
            try:
                async with session.get(url) as response:
                    status_code = response.status
            except (ClientError, asyncio.TimeoutError, Exception):
                status_code = 0
            await queue.put({"url": url, "status_code": status_code})

    async def writer():
        async with aiofiles.open(file_path, "a") as f:
            while True:
                item = await queue.get()
                if item is None:
                    queue.task_done()
                    break
                await f.write(json.dumps(item) + "\n")
                queue.task_done()

    writer_task = asyncio.create_task(writer())

    async with ClientSession(timeout=ClientTimeout(total=10)) as session:
        for batch in chunks(urls, batch_size):
            tasks = [asyncio.create_task(fetch(url, session)) for url in batch]
            await asyncio.gather(*tasks)

    await queue.put(None)
    await queue.join()
    await writer_task


if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))
