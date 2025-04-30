


async def update_file(filepath, mode, text):
    lock = asyncio.Lock()
        
    async with lock:
        global subcnt
        subcnt += 1
        async with aiofiles.open(filepath, mode) as f:
            await f.write(text)
