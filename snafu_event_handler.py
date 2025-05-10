
import asyncio,aiofiles

async def update_file(filepath, mode, text):
    lock = asyncio.Lock()
        
    async with lock:
        global subcnt
        subcnt += 1
        async with aiofiles.open(filepath, mode) as f:
            await f.write(text)
lock = asyncio.Lock()
async def blub():        
    async with lock:
        global subcnt
        subcnt += 1
        async with aiofiles.open("/home/snafu/src/scripte_twitch/data_files/subs.txt", "w") as f:
            await f.write(f"Subs: {subcnt}/1")

        async with aiofiles.open("/home/snafu/src/scripte_twitch/data_files/stats/lastsub.txt", "w") as f:
            await f.write(f'last sub, thank you\n{x.event.user_name}')