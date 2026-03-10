""" 
TODO:
 - Get  I want to track
 - download images
 - process images
 - download images

"""

import asyncio
import httpx
from PIL import Image
from io import BytesIO
import httpx
import aiofiles # for asynchronous file operations

image_urls = [
    
    "https://images.unsplash.com/photo-1529778873920-4da4926a72c2?q=80&w=736&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D0",
    "https://images.unsplash.com/photo-1591824438708-ce405f36ba3d?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?q=80&w=1228&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1574870111867-089730e5a72b?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1535083783855-76ae62b2914e?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?q=80&w=764&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
]

async def download_image(client: httpx.AsyncClient, url: str, number_file: str):
    
    response = await client.get(url, timeout=10, follow_redirects=True)
    response.raise_for_status()
    
    file_name = f"img_{number_file}.jpg"
    async with aiofiles.open("file_name", "w") as f:
        await f.write(await response.read())
        await f.close()
    

async def download_images(urls: list[str]):
    
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(download_image(client, url, img_number)) for img_number, url in enumerate(urls)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    
    
    return None
    
async def main():
    
    for url in image_urls:
        download_images(url)
    return None
    
if __name__ == "__main__":
    asyncio.run(main())
    
