class ImageDownloader:
    def __init__(self, client: MapillaryClient):
        self.client = client
        self.download_path = Path('data/downloads')
        self.download_path.mkdir(parents=True, exist_ok=True)

    async def download_images(self, username: str, bbox: tuple):
        images = await self.client.get_images(username, bbox)
        tasks = []
        for image in images:
            task = asyncio.create_task(
                self.download_single_image(image)
            )
            tasks.append(task)
        await asyncio.gather(*tasks)