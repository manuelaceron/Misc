""" 
TODO:
 - process images
 - download images

"""
import requests
import asyncio
import httpx
import time
from PIL import Image
from io import BytesIO
import httpx
import aiofiles # for asynchronous file operations

STORE_PATH = "/home/manuela/Dev/Study/Misc/Tutorials/async_image_processing/images"
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
    
    file_path = f"{STORE_PATH}/img_{number_file}.jpg"
    
    async with aiofiles.open(file_path, "wb") as f:
        
        # stores entire file in memory (one big bytes object)
        # can be problematic with big files and concurrency
        # close is not needed, async with does it automatically
        # await f.write(await response.read())
        
        # downloads small chunks of 8KB, writes chunkc in disk, descard and repeat
        # scales better, memory stays constant
        async for chunk in response.aiter_bytes(chunk_size=8192):
            await f.write(chunk)
        
        return file_path
    

async def download_images(urls: list[str]):
    
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            # tasks created and scheduled on event loop
            tasks = [tg.create_task(download_image(client, url, img_number)) for img_number, url in enumerate(urls)]
            # context manager internally awaits all tasks after creation, no need of calling await or gather
            # event loop runs all tasks... when all done, context manager exits
        img_paths = [task.result() for task in tasks]

    return img_paths

# sequential download
def sync_download(image_urls):
    img_paths = []
    for number_file, url in enumerate(image_urls):
        file_path = f"{STORE_PATH}/img_{number_file}.jpg"
        response = requests.get(url)
        open(file_path, 'wb').write(response.content)
        img_paths.append(file_path)
    return img_paths
        
async def main():
    
    start_time = time.perf_counter()
    img_paths = await download_images(image_urls) #0.21s
    #img_paths = sync_download(image_urls) #1.29 s
    down_time = time.perf_counter()
    print(img_paths)
    print(f"Downloading time: {down_time-start_time}")
    
if __name__ == "__main__":
    asyncio.run(main())
    
