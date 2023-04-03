from abc import ABC, abstractmethod
import aiohttp
import ssl
import certifi

class ScraperBase(ABC):

    @abstractmethod
    async def scrape(self, params):
        pass

          
    async def fetch_url(self, url, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False, headers=headers) as resp:
                html = await resp.text()  
                return html   

             

    