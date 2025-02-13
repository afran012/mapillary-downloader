import time
import asyncio
from loguru import logger

class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute
        self.request_count = 0
        self.last_reset = time.time()

    async def wait_if_needed(self):
        current_time = time.time()
        if current_time - self.last_reset >= 60:
            self.request_count = 0
            self.last_reset = current_time
        
        if self.request_count >= self.requests_per_minute:
            wait_time = 60 - (current_time - self.last_reset)
            logger.info(f"Rate limit reached, waiting {wait_time:.2f} seconds")
            await asyncio.sleep(wait_time)
            self.request_count = 0
            self.last_reset = time.time()
        
        self.request_count += 1