import asyncio
import aiofiles
from pathlib import Path
from typing import List
from loguru import logger
from ..models.image import ImageMetadata
from ..api.client import MapillaryClient
from config.settings import settings

class ImageDownloader:
    def __init__(self, client: MapillaryClient):
        self.client = client
        self.download_path = settings.DOWNLOAD_PATH
        self.download_path.mkdir(parents=True, exist_ok=True)

    async def download_single_image(self, image: ImageMetadata) -> bool:
        file_path = self.download_path / image.filename
        
        if file_path.exists():
            logger.info(f"Image {image.id} already exists, skipping")
            return True

        for attempt in range(settings.RETRY_ATTEMPTS):
            try:
                async with self.client.session.get(image.thumb_1024_url) as response:
                    if response.status != 200:
                        raise ValueError(f"HTTP {response.status}")

                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(await response.read())
                        
                    logger.success(f"Downloaded image {image.id}")
                    return True

            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed for image {image.id}: {e}")
                if attempt < settings.RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(settings.RETRY_DELAY)
                    
        return False

    async def download_images(self, username: str, bbox: tuple) -> dict:
        images = await self.client.get_images(username, bbox)
        logger.info(f"Found {len(images)} images to download")

        results = {
            'total': len(images),
            'successful': 0,
            'failed': 0
        }

        tasks = []
        for image in images:
            task = asyncio.create_task(self.download_single_image(image))
            tasks.append(task)

        completed = await asyncio.gather(*tasks)
        
        results['successful'] = sum(1 for x in completed if x)
        results['failed'] = sum(1 for x in completed if not x)
        
        return results