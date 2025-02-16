import aiohttp
import asyncio
from loguru import logger
from config.settings import settings

async def verify_api_key(api_key: str):
    url = "https://graph.mapillary.com/me"
    headers = {
        'Authorization': f'OAuth {api_key}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                logger.info("API key is valid.")
                return True
            else:
                error_message = await response.text()
                logger.error(f"Invalid API key: {response.status} - {error_message}")
                return False

async def main():
    api_key = settings.API_KEY
    is_valid = await verify_api_key(api_key)
    if is_valid:
        logger.info("Proceed with your application logic.")
    else:
        logger.error("Please check your API key and try again.")

if __name__ == "__main__":
    asyncio.run(main())