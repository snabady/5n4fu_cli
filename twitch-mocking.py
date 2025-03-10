import twitchEvents 
import asyncio
import db.mydb
import subprocess


async def display_menu():
    # Display a simple menu to the user
    print("Event Categories:")
    print("1: Subscribe TEMPO events")
    print("2: Ban events")
    print("3: Channel goal events")
    print("4: Channel points events")
    print("5: Channel polls events")
    print("6: Channel predictions events")
    print("7: Hype train events")
    print("8: Shoutout events")
    print("9: Stream info events")
    print("10: Subscribe events")
    print("11: Charity events")
    print("0: free menu for events happening")

    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None
    


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

    #this for mocking with cli
    #mydb = mydb.MyDB()
    async with twitchEvents.TwitchEvents(use_cli_conn=True) as tevents:
        try:
            
            await tevents.subCliEventsTEMPO()
            #await tevents.listen_ban_events()
            #await tevents.listen_channel_goal_events()
            #await tevents.listen_channel_points()
            #await tevents.listen_channel_polls()
            #await tevents.listen_channel_predictions()
            #await tevents.listen_hype_train()
            #await tevents.listen_shoutout_events()
            #await tevents.listen_stream_info_events()
            #await tevents.listen_subscribe_events()
            #await tevents.listen_charity_events()
        except Exception as e:
            print(e)

        try:
            while True:
                # TODO save -t id in db 
                # TODO save event-sub-id to db -> use data here to print or execute directly an action
                choice = await display_menu()
                if choice == 666:
                    break
                elif choice == 1:
                    try: 
                        print("yeah")
                        try: 
                            print("foo")
                            user_id = tevents.user.id 
                            print("baz")
                            sub_id = tevents.sub_id_map.get("channel.subscribe")
                            print("bar")
                            
                            print("bari")
                            print(f'user_id: {user_id} sub_id: {sub_id}')
                            print(str(tevents.sub_id_map))
                        except Exception as e:
                            print(e)
                        #subprocess.run(['twitch' , 'event trigger channel.subscribe', '-t ', f'{user_id} ', '-u ' , f'{sub_id} '])
                        cmd = f'twitch event trigger channel.subscribe -t {user_id} -u {sub_id} -T websocket'
                        process = await asyncio.create_subprocess_shell(
                                                    cmd,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE
                                                )

                        tdout, stderr = await process.communicate()
                        print(f"stdout: {tdout}")
                    except Exception as e:  
                        print(e)
                elif choice == 0: 
                    break  # sumenu
                        #-> print all TEMPO events
                    pass
          
                
                await asyncio.sleep(0.1)
         
        except asyncio.CancelledError:
            print("cu later OOO")

asyncio.run(main())

