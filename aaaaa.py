#asyncio.run(twitch_setup())
subprocess.run(['twitch', 'event', 'trigger', 'channel.subscribe', '-t', 8465457, '-u' , 86545]])