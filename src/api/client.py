class MapillaryClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.rate_limiter = RateLimiter()
        self.session = aiohttp.ClientSession()

    async def get_images(self, username: str, bbox: tuple):
        await self.rate_limiter.wait_if_needed()
        params = {
            'access_token': self.api_key,
            'fields': 'id,geometry,thumb_1024_url',
            'creator_username': username,
            'bbox': f'{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}',
            'limit': 2000
        }
        # Implementar paginación y manejo de errores