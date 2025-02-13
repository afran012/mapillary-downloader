class RateLimiter:
    def __init__(self):
        self.requests_per_minute = 10000  # Límite de búsqueda
        self.request_count = 0
        self.last_reset = time.time()

    async def wait_if_needed(self):
        current_time = time.time()
        if current_time - self.last_reset >= 60:
            self.request_count = 0
            self.last_reset = current_time
        
        if self.request_count >= self.requests_per_minute:
            wait_time = 60 - (current_time - self.last_reset)
            await asyncio.sleep(wait_time)