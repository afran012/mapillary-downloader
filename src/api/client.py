import aiohttp
import asyncio
from typing import Dict, Optional, List
from loguru import logger
from ..models.image import ImageMetadata
from .rate_limiter import RateLimiter
from config.settings import settings

class MapillaryClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.rate_limiter = RateLimiter(settings.REQUESTS_PER_MINUTE)
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_images(self, username: str, bbox: tuple) -> List[ImageMetadata]:
        if not self.session:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        
        await self.rate_limiter.wait_if_needed()
        
        headers = {
            'Authorization': f'OAuth {self.api_key}'
        }
        
        params = {
            'fields': 'id,geometry,thumb_1024_url,captured_at',
            'creator_username': username,
            'bbox': f'{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}',
            'limit': settings.BATCH_SIZE
        }

        images = []
        next_page = f"{settings.BASE_URL}/images"

        while next_page:
            try:
                async with self.session.get(next_page, params=params, headers=headers) as response:
                    if response.status != 200:
                        error_message = await response.text()
                        logger.error(f"Error fetching images: {response.status} - {error_message}")
                        if response.status == 400:
                            logger.error("Bad request. Please check the parameters and try again.")
                        elif response.status == 401:
                            logger.error("Unauthorized. Please check your API key.")
                        elif response.status == 403:
                            logger.error("Forbidden. You do not have permission to access this resource.")
                        elif response.status == 404:
                            logger.error("Not found. The requested resource could not be found.")
                        elif response.status == 500:
                            logger.error("Internal server error. Please try again later.")
                        break

                    data = await response.json()
                    for image_data in data.get('data', []):
                        images.append(ImageMetadata(**image_data))

                    next_page = data.get('paging', {}).get('next')
                    params = {}  # Clear params as they're included in next_page URL

            except Exception as e:
                logger.error(f"Error during API request: {e}")
                break

        return images