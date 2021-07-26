import aiohttp
import asyncio
import ssl
import json
from config import URLS


async def fetch(session, url):
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        return await response.text()


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True)
        return results


def get_data_from_api():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    urls = URLS
    htmls = loop.run_until_complete(fetch_all(urls, loop))
    result = []
    for res in htmls:
        json_result = json.loads(res)
        for product in json_result:
            result.append(f"{product.get('name')} {product.get('price')}")
    return result
