import twitchEvents 
import asyncio

async def main():
    """
     u only need to setup your local twitch-cli in advance
     To get started, first install and set up twitch-cli as described here: https://dev.twitch.tv/docs/cli/
     and then use the following commands: 

     generate usercred         twitch mock-api generate
     start the mock server     twitch mock-api start
     start websocketapi        twitch event websocket start
     python test.py 
     when it is running copy paste the output-command and put it into new console *magic*
    """


    async with twitchEvents.TwitchEvents(db=None, use_sna_overlay=False) as tevents:
        try: 
            #await tevents.subCliEventsTEMPO()  
            await tevents.listen_subscribe_events()
            #await tevents.subCliEventsTEMPO()
            await tevents.listen_ban_events()
            await tevents.listen_channel_goal_events()
            await tevents.listen_channel_points()
            await tevents.listen_channel_polls()
            await tevents.listen_channel_predictions()
            await tevents.listen_hype_train()
            await tevents.listen_shoutout_events()
            await tevents.listen_stream_info_events()
            
            #await tevents.listen_charity_events()
            await tevents.listen_channel_action_events()
            #await tevents.listen_channel_moderate_events()
        except Exception as e:
            print(e)
    
        try:
            while True:
                await asyncio.sleep(50)
         
        except asyncio.CancelledError:
            print("cu later OOO")

asyncio.run(main())

