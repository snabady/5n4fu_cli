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

async def display_stream_info_menu():
    print("1: stream.online")
    print("2: stream.offline")
    print("3: channel.update (v2)")
    print("4: channel.update")
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
    
async def display_channel_goal_menu():
    print("1: channel.goal.begin")
    print("2: channel.goal.progress")
    print("3: channel.goal.end")
    print("0: exit")    
    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None 

async def display_channel_polls_menu():
    print("1: channel.poll.begin")
    print("2: channel.poll.progress")
    print("3: channel.poll.end")
    print("0: exit")
    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None
    
async def display_channel_predictions_menu():
    print("1: channel.prediction.begin")
    print("2: channel.prediction.end")
    print("3: channel.prediction.progress")
    print("4: channel.prediction.lock")
    print("0: exit")
    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None 

async def display_hype_train_menu():
    print("1: hype.train.begin")
    print("2: hype.train.progress")
    print("3: hype.train.end")
    print("0: exit")
    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None 
async def display_shoutout_menu():
    print("1: channel.shoutout.create")
    print("2: channel.shoutout.receive")
    print("0: exit")
    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None

async def display_subscribe_menu():
    print("1: channel.subscribe")
    print("2: channel.subscription.gift")
    print("3: channel.subscription.message")
    print("4: channel.subscription.end")
    print("0: exit")
    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None
async def display_ban_menu():
    print("1: channel.ban")
    print("2: channel.unban")
    #print("3: channel.unban.request.create")
    #print("4: channel.unban.request.resolve")
    print("0: exit")
    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None

async def display_charity_menu():
    print("1: charity.donate")
    print("2: charity.progress")
    print("3: charity.start")
    print("4: charity.stop")
    print("0: exit")        
    try:
        # Take the user input as an integer
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None

    
async def run_subprocess(cmd):
    print(f"cmd: {cmd}")
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
        subchoice = await display_ban_menu()
        if subchoice == 1:
            print("channel.ban")
            sub_id = tevents.sub_id_map.get("channel.ban")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.ban -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("channel.unban")
            sub_id = tevents.sub_id_map.get("channel.unban")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.unban -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
            """
            # TODO: implement these events 
            elif subchoice == 3:
                print("channel.unban.request.create")
                sub_id = tevents.sub_id_map.get("channel.unban.request.create")
                user_id = tevents.user.id
                cmd = f'twitch event trigger channel.unban.request.create -t {user_id} -u {sub_id} -T websocket'
                await run_subprocess(cmd)
            elif subchoice == 4:
                print("channel.unban.request.resolve")
                sub_id = tevents.sub_id_map.get("channel.unban.request.resolve")
                user_id = tevents.user.id
                cmd = f'twitch event trigger channel.unban.request.resolve -t {user_id} -u {sub_id} -T websocket'
                await run_subprocess(cmd)
            """
        elif subchoice == 0:
            return
    elif choice == 3:
        subchoice = await display_channel_goal_menu()
        if subchoice == 1:
            print("channel.goal.begin")
            sub_id = tevents.sub_id_map.get("channel.goal.begin")
            user_id = tevents.user.id

            cmd = f'twitch event trigger channel.goal.begin -t {user_id} -u {sub_id} -T websocket'
            
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("channel.goal.progress")
            sub_id = tevents.sub_id_map.get("channel.goal.progress")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.goal.progress -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 3:
            print("channel.goal.end")
            sub_id = tevents.sub_id_map.get("channel.goal.end")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.goal.end -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 0:
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
        subchoice = await display_channel_polls_menu()
        if subchoice == 1:
            print("channel.poll.begin")
            sub_id = tevents.sub_id_map.get("channel.poll.begin")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.poll.begin -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("channel.poll.progress")
            sub_id = tevents.sub_id_map.get("channel.poll.progress")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.poll.progress -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 3:
            print("channel.poll.end")
            sub_id = tevents.sub_id_map.get("channel.poll.end")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.poll.end -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 0:
            return
    elif choice == 6:
        subchoice = await display_channel_predictions_menu()
        if subchoice == 1:
            print("channel.prediction.begin")
            sub_id = tevents.sub_id_map.get("channel.prediction.begin")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.prediction.begin -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("channel.prediction.end")
            sub_id = tevents.sub_id_map.get("channel.prediction.end")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.prediction.end -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 3:
            print("channel.prediction.progress")
            sub_id = tevents.sub_id_map.get("channel.prediction.progress")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.prediction.progress -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 4:
            print("channel.prediction.lock")
            sub_id = tevents.sub_id_map.get("channel.prediction.lock")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.prediction.lock -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 0:
            return
    elif choice == 7:
        subchoice = await display_hype_train_menu()
        if subchoice == 1:
            print("hype.train.begin")
            sub_id = tevents.sub_id_map.get("hype.train.begin")
            user_id = tevents.user.id
            cmd = f'twitch event trigger hype.train.begin -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("hype.train.progress")
            sub_id = tevents.sub_id_map.get("hype.train.progress")
            user_id = tevents.user.id
            cmd = f'twitch event trigger hype.train.progress -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 3:
            print("hype.train.end")
            sub_id = tevents.sub_id_map.get("hype.train.end")
            user_id = tevents.user.id
            cmd = f'twitch event trigger hype.train.end -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 0:
            return
    elif choice == 8:

        subchoice = await display_shoutout_menu()
        if subchoice == 1:
            print("channel.shoutout.create")
            sub_id = tevents.sub_id_map.get("channel.shoutout.create")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.shoutout.create -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("channel.shoutout.receive")
            sub_id = tevents.sub_id_map.get("channel.shoutout.receive")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.shoutout.receive -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 0:
            return
    elif choice == 9:
        
        subchoice = await display_stream_info_menu()
        if subchoice == 1:
            print("stream.online event")
            sub_id = tevents.sub_id_map.get("stream.online")
            user_id = tevents.user.id
            cmd = f'twitch event trigger stream.online -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("stream.offline event")
            sub_id = tevents.sub_id_map.get("stream.offline")
            user_id = tevents.user.id
            cmd = f'twitch event trigger stream.offline -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 3:    
            print("channel.update (v2) event")
            sub_id = tevents.sub_id_map.get("channel.update (v2)")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.update -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 4:
            print("channel.update event")
            sub_id = tevents.sub_id_map.get("channel.update")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.update -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)           
        elif subchoice == 0:
            return





    elif choice == 10:
        subchoice = await display_subscribe_menu()
        if subchoice == 1:
            print("channel.subscribe")
            sub_id = tevents.sub_id_map.get("channel.subscribe")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.subscribe -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("channel.subscription.gift")
            sub_id = tevents.sub_id_map.get("channel.subscription.gift")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.subscription.gift -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 3:
            print("channel.subscription.message")
            sub_id = tevents.sub_id_map.get("channel.subscription.message")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.subscription.message -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 4:
            print("channel.subscription.end")
            sub_id = tevents.sub_id_map.get("channel.subscription.end")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.subscription.end -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 0:
            return
    elif choice == 11:
        subchoice = await display_charity_menu()
        if subchoice == 1:
            print("charity.donate")
            sub_id = tevents.sub_id_map.get("charity.donate")
            user_id = tevents.user.id
            cmd = f'twitch event trigger charity.donate -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 2:
            print("charity.progress")
            sub_id = tevents.sub_id_map.get("charity.progress")
            user_id = tevents.user.id
            cmd = f'twitch event trigger charity.progress -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 3:
            print("charity.start")
            sub_id = tevents.sub_id_map.get("charity.start")
            user_id = tevents.user.id
            cmd = f'twitch event trigger charity.start -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 4:
            print("charity.stop")
            sub_id = tevents.sub_id_map.get("charity.stop")
            user_id = tevents.user.id
            cmd = f'twitch event trigger charity.stop -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 0:
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
        # listen channel moderate events
        subchoice = await display_action_menu()
        if subchoice == 1:
            print("channel.moderate")
            sub_id = tevents.sub_id_map.get("channel.moderate")
            user_id = tevents.user.id
            cmd = f'twitch event trigger channel.moderate -t {user_id} -u {sub_id} -T websocket'
            await run_subprocess(cmd)
        elif subchoice == 0:
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
            
            await tevents.subCliEventsTEMPO()
            await tevents.listen_ban_events()
            await tevents.listen_channel_goal_events()
            await tevents.listen_channel_points()
            await tevents.listen_channel_polls()
            await tevents.listen_channel_predictions()
            await tevents.listen_hype_train()
            await tevents.listen_shoutout_events()
            await tevents.listen_stream_info_events()
            await tevents.listen_subscribe_events()
            await tevents.listen_charity_events()
            await tevents.listen_channel_action_events()
            await tevents.listen_channel_moderate_events()
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

