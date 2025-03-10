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
    print("12: Channel action events")
    print("13: Channel moderate events")
    print("666: Exit")
    print("0: free menu for events happening")

    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None

async def display_action_menu():

    print("1: channel.cheer")
    print("2: channel.follow")
    print("3: channel.raid")
    print("0: exit")

    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None
    
async def display_points_menu():
    print("1: channel.channel_points_custom_reward_redemption.add")
    print("2: channel.channel_points_custom_reward_redemption.update")
    print("3: channel.channel_points_custom_reward_redemption.remove")
    print("4: channel.channel_points_custom_reward_redemption.add")
    print("5: channel.channel_points_custom_reward_redemption.update")
    print("6: channel.channel_points_custom_reward_redemption.remove")
    print("0: exit")

    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None
    
async def run_subprocess(cmd):
    process = await asyncio.create_subprocess_shell(
                            cmd,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )

    tdout, stderr = await process.communicate()
    print(f"stdout: {tdout}")

async def choicechecker(choice, tevents):
        # TODO save -t id in db 
    # TODO save event-sub-id to db -> use data here to print or execute directly an action

    if choice == 666:
        return 
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
            await run_subprocess(cmd)
        except Exception as e:  
            print(e)
    elif choice == 0: 
        return  # sumenu
            #-> print all TEMPO events
        pass
    elif choice == 2:
        return
    elif choice == 3:
        return
    elif choice == 4:
        subchoice = await display_points_menu()
        if subchoice == 1:
            print("channel.channel_points_custom_reward_redemption.add")
            sub_id = tevents.sub_id_map.get("channel.channel_points_custom_reward_redemption.add")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.channel_points_custom_reward_redemption.add -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("channel.channel_points_custom_reward_redemption.update")
            sub_id = tevents.sub_id_map.get("channel.channel_points_custom_reward_redemption.update")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.channel_points_custom_reward_redemption.update -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 3:    
            print("channel.channel_points_custom_reward_redemption.remove")
            sub_id = tevents.sub_id_map.get("channel.channel_points_custom_reward_redemption.remove")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.channel_points_custom_reward_redemption.remove -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 4:
            print("channel.channel_points_custom_reward_redemption.add")    
            sub_id = tevents.sub_id_map.get("channel.channel_points_custom_reward_redemption.add")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.channel_points_custom_reward_redemption.add -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 5:    
            print("channel.channel_points_custom_reward_redemption.update")
            sub_id = tevents.sub_id_map.get("channel.channel_points_custom_reward_redemption.update")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.channel_points_custom_reward_redemption.update -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 6:
            print("channel.channel_points_custom_reward_redemption.remove")
            sub_id = tevents.sub_id_map.get("channel.channel_points_custom_reward_redemption.remove")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.channel_points_custom_reward_redemption.remove -t {user_id} -u {sub_id} -T websocket'      
            await run_subprocess(cmd)
        elif subchoice == 0:
            return
        
        
        
            
    elif choice == 5:
        return
    elif choice == 6:
        return
    elif choice == 7:
        return
    elif choice == 8:
        return
    elif choice == 9:
        return
    elif choice == 10:
        return
    elif choice == 11:
        return
    elif choice == 12:
        # listen channel action events
        subchoice = await display_action_menu()
        if subchoice == 1:
            print("channel.cheer")
            sub_id = tevents.sub_id_map.get("channel.cheer")
            user_id = tevents.user.id   
            cmd = f'twitch event trigger channel.cheer -t {user_id} -u {sub_id} -T websocket'       
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("channel.follow")
            sub_id = tevents.sub_id_map.get("channel.follow")
            user_id = tevents.user.id   
            cmd = f'twitch event trigger channel.follow -t {user_id} -u {sub_id} -T websocket'       
            await run_subprocess(cmd)
        elif subchoice == 3:
            print("channel.raid")
            sub_id = tevents.sub_id_map.get("channel.raid")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.raid -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 0:
            return
    
    elif choice == 13:
        return
    else:
        print("Invalid choice! Please enter a valid number.")
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
            
            #await tevents.subCliEventsTEMPO()
            #await tevents.listen_ban_events()
            #await tevents.listen_channel_goal_events()
            await tevents.listen_channel_points()
            #await tevents.listen_channel_polls()
            #await tevents.listen_channel_predictions()
            #await tevents.listen_hype_train()
            #await tevents.listen_shoutout_events()
            #await tevents.listen_stream_info_events()
            #await tevents.listen_subscribe_events()
            #await tevents.listen_charity_events()
            await tevents.listen_channel_action_events()
            #await tevents.listen_channel_moderate_events()
        except Exception as e:
            print(e)

        try:
            while True:
                choice = await display_menu()
                await choicechecker(choice, tevents)
                await asyncio.sleep(0.1)
         
        except asyncio.CancelledError:
            print("cu later OOO")

asyncio.run(main())

