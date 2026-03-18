import requests
import asyncio
import httpx
import time
from PIL import Image
import aiofiles  # for asynchronous file operations
import cv2
import numpy as np
from concurrent.futures import ProcessPoolExecutor

STORE_PATH = "/home/manuela/Dev/Study/Misc/Tutorials/async_image_processing/images"
DOWNLOAD_LIMIT = 4
image_urls = [
    "https://images.unsplash.com/photo-1529778873920-4da4926a72c2?q=80&w=736&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D0",
    "https://images.unsplash.com/photo-1591824438708-ce405f36ba3d?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?q=80&w=1228&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1574870111867-089730e5a72b?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1535083783855-76ae62b2914e?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?q=80&w=764&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1516117172878-fd2c41f4a759?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1532009324734-20a7a5813719?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1524429656589-6633a470097c?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1530224264768-7ff8c1789d79?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1564135624576-c5c88640f235?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1541698444083-023c97d3f4b6?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1522364723953-452d3431c267?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1516972810927-80185027ca84?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1550439062-609e1531270e?w=1920&h=1080&fit=crop",
    "https://images.unsplash.com/photo-1549692520-acc6669e2f0c?w=1920&h=1080&fit=crop",
]


async def download_image(
    client: httpx.AsyncClient, url: str, number_file: str, semaphore: asyncio.Semaphore
):

    async with semaphore:
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
    dl_semaphore = asyncio.Semaphore(DOWNLOAD_LIMIT)
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:  # Task group works with coroutines
            # tasks created and scheduled on event loop
            tasks = [
                tg.create_task(download_image(client, url, img_number, dl_semaphore))
                for img_number, url in enumerate(urls)
            ]
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
        open(file_path, "wb").write(response.content)
        img_paths.append(file_path)
    return img_paths


def sync_process_images(img: str):
    # for img in img_paths:
    image = cv2.imread(img)
    width, height = image.shape[1], image.shape[0]
    center = (width // 2, height // 2)
    angles = [10, 30, -30, 40, -40, 50, -50]
    scales = [1, 2, 3]
    for num_a, angle in enumerate(angles):
        for num_s, scale in enumerate(scales):
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
            rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
            cv2.imwrite(f"{img.split(".")[0]}_a{num_a}_s{num_s}.jpg", rotated_image)

    txs = [np.random.randint(-500, 500) for t in np.arange(4)]
    tys = [np.random.randint(-500, 500) for t in np.arange(4)]

    for tx, ty in zip(txs, tys):
        translation_matrix = np.array([[1, 0, tx], [0, 1, ty]], dtype=np.float32)
        translated_image = cv2.warpAffine(image, translation_matrix, (width, height))
        cv2.imwrite(f"{img.split(".")[0]}_t{tx}_{ty}.jpg", translated_image)

    blurred = cv2.GaussianBlur(image, (9, 9), 0)
    cv2.imwrite(f"{img.split(".")[0]}_b.jpg", blurred)


async def process_images(img_paths: list[str]):

    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor(max_workers=6) as executor:  # Executor works with futures
        # list of futures
        tasks = [
            loop.run_in_executor(executor, sync_process_images, img)
            for img in img_paths
        ]
        results = await asyncio.gather(*tasks)


async def main():

    start_time = time.perf_counter()
    img_paths = await download_images(image_urls)  # 0.21s
    # img_paths = sync_download(image_urls) #1.29 s
    down_time = time.perf_counter()
    print(img_paths)
    print(f"Downloading time: {down_time-start_time}")

    start_time = time.perf_counter()
    # sync_process_images(img_paths) #6s
    await process_images(img_paths)  # 4s
    process_time = time.perf_counter()
    print(f"Processing time: {process_time-start_time}")


if __name__ == "__main__":
    asyncio.run(main())
