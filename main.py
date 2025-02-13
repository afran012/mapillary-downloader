import asyncio
import argparse
from loguru import logger
from src.api.client import MapillaryClient
from src.services.downloader import ImageDownloader
from src.utils.logger import setup_logger
from src.utils.validators import validate_bbox, validate_username
from config.settings import settings

async def main(username: str, bbox: tuple):
    if not validate_username(username):
        logger.error("Invalid username")
        return
    
    if not validate_bbox(bbox):
        logger.error("Invalid bounding box")
        return

    setup_logger()
    logger.info(f"Starting download for user {username} in area {bbox}")

    async with MapillaryClient(settings.API_KEY) as client:
        downloader = ImageDownloader(client)
        results = await downloader.download_images(username, bbox)
        
        logger.info(
            f"Download completed:\n"
            f"Total images: {results['total']}\n"
            f"Successfully downloaded: {results['successful']}\n"
            f"Failed downloads: {results['failed']}"
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Mapillary images for a specific user and area")
    parser.add_argument("username", help="Mapillary username")
    parser.add_argument("--bbox", nargs=4, type=float, required=True,
                      help="Bounding box coordinates: min_lon min_lat max_lon max_lat")
    
    args = parser.parse_args()
    bbox = tuple(args.bbox)
    
    asyncio.run(main(args.username, bbox))