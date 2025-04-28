from twitchAPI.object.eventsub import ChannelSubscribeEvent, ChannelRaidEvent, ChannelFollowEvent, StreamOnlineEvent, StreamOfflineEvent, ChannelUpdateEvent, GoalEvent, ChannelPredictionEvent, ChannelPointsCustomRewardRedemptionUpdateEvent, ChannelPointsCustomRewardRedemptionAddEvent, ChannelPointsCustomRewardUpdateEvent, ChannelPointsCustomRewardRemoveEvent, ChannelPointsCustomRewardAddEvent, HypeTrainEvent, HypeTrainEndEvent, ChannelUnbanRequestResolveEvent, ChannelBanEvent, ChannelUnbanEvent, ChannelUnbanRequestCreateEvent, CharityCampaignProgressEvent, CharityCampaignStartEvent, CharityCampaignStopEvent, CharityDonationEvent, ChannelSubscriptionEndEvent, ChannelSubscriptionGiftEvent, ChannelSubscriptionMessageEvent, ChannelShoutoutCreateEvent, ChannelShoutoutReceiveEvent, SubscriptionMessage, ChannelCheerEvent, ChannelPointsAutomaticRewardRedemptionAddEvent
import logging
import colorlog
import subprocess
import asyncio
import os
import sys
import aiofiles
#/home/snafu/src/twitch-irc/obs_websocket/my_obsws.py
script_dir = os.path.abspath("/home/snafu/src/twitch-irc/")  # <-- Hier deinen echten Pfad eintragen!
if script_dir not in sys.path:
    sys.path.append(script_dir)
from scripte.templateMgr import template_manager
myobs_dir = os.path.abspath("/home/snafu/src/twitch-irc/obs_websocket/")
if script_dir not in sys.path:
    sys.path.append(mybobs_dir)
from obs_websocket import my_obsws 

async def setRaid(bools):
    wst = my_obsws.Obs_ws()

    await my_obsws.init_obswebsocket_ws()
    raid_id = await my_obsws.get_scene_item_id("main","raid")
    await my_obsws.set_source_visibility("main",raid_id,bools)

subcnt = 0
followcnt = 62
def add_logger_handler(logger):
    handler = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        '%(asctime)s - %(log_color)s%(levelname)-8s%(reset)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = logging.getLogger(__name__)
logger = add_logger_handler(logger)
logger.setLevel(logging.DEBUG)

async def send_to_websocket(x):
    if isinstance(x, ChannelSubscribeEvent):
        pass 

async def send_to_db(x):
    if isinstance(x, ChannelSubscribeEvent):
        pass

async def send_to_log(x):
    if isinstance(x, ChannelSubscribeEvent):
        pass

async def do_xcow_things(x):
    if isinstance(x, ChannelSubscribeEvent):
        # TODO asyncio.subprocess !!!
        pass

async def onSubscribe(x: ChannelSubscribeEvent, twitch):
    """
    displays the data received by the channel_subscribe Event
    """
    #await twitch.iamatest()
    if x.event.is_gift :
        blub = f'{x.event.user_name} happy U you have gotten a gift-sub'
    else:
        blub = f'{x.event.user_name} bist deppert, danke fuer deinen sub'
        try:
            lock = asyncio.Lock()
            
            async with lock:
                global subcnt
                subcnt += 1
                async with aiofiles.open("/home/snafu/src/scripte_twitch/data_files/subs.txt", "w") as f:
                    await f.write(f"Subs: {subcnt}/1")

        except Exception as e:
            logger.error(f'exceptiopn: {e}')
    #subprocess.run(['xcowsay', '--monitor',  '1', blub, '--image=' '/home/snafu/Downloads/cow.png', '--think' ,'--bubble-at=-230,-6',  ])
    #'xcowsay', '--monitor', '1', blub, '--image=/home/snafu/src/scripte_twitch/img/glitch-minecraft-outlined-b4903b26224ceb4462b1.png', '--think'
    process = await asyncio.create_subprocess_exec(
        
        "xcowsay", blub, "--monitor=0","--font=mono12", '--image=/home/snafu/src/scripte_twitch/img/glitch-minecraft-outlined-b4903b26224ceb4462b1.png', "--time=15",
    )
    
    await process.wait()
    logger.info('received subscription')
    global template_manager
    await template_manager.load_existing_values2()
    template_manager.set_subscriber(x.event.broadcaster_user_name)
    await template_manager.generate_file()
    logger.debug(f'{x.event.to_dict()}')



async def on_channel_raid(x: ChannelRaidEvent, twitch):
    """
    displays the data received by the channel_subscribe Event
    """
    logger.info(f'received channel raid')
    logger.debug(f'{x.event.to_dict()}')
    blub = f'{x.event.from_broadcaster_user_name} just raided with {x.event.viewers} viewer'
    await setRaid(True)
    subprocess.Popen(['xcowsay', '--monitor',  '0', blub, '--image=' '/home/snafu/src/scripte_twitch/img/glitch-minecraft-outlined-b4903b26224ceb4462b1.png', '--think' , '--time=240','--at=1080,0',  ])
    #proc = subprocess.Popen(['mpv', '--no-video', '--volume=50',  '/home/snafu/src/scripte_twitch/vids/kapernfahrt.webm'])
    proc = await asyncio.create_subprocess_exec(
        'mpv', '--no-video', '--volume=50', '--idle=no', '/home/snafu/src/scripte_twitch/vids/kapernfahrt.webm',
        stdin=asyncio.subprocess.DEVNULL,  # wichtig!
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    ret = await proc.wait()
    print( proc.returncode)
    if ret==0: 
        await setRaid(False)


async def on_follow(x: ChannelFollowEvent, twitch):
    """
    displays the data received by the channel_follow_v2 Event
    details: https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/#channel-follow-webhook-notification-example
    relevant parts: x.event.
    https://dev.twitch.tv/docs/eventsub/eventsub-reference/
    """
    blub = f'{x.event.user_name} danke fuers folgen! <3'
    subprocess.run(['xcowsay', '--monitor',  '0', blub, '--image=' '/home/snafu/pics/stream/sna.png', '--think'   ])
    logger.info(f'received follow event')
    try:
        lock = asyncio.Lock()
        
        async with lock:
            global followcnt
            followcnt += 1
            async with aiofiles.open("/home/snafu/src/scripte_twitch/data_files/follower_goal.txt", "w") as f:
                await f.write(f"Follower: {followcnt}/70")

    except Exception as e:
        logger.error(f'exceptiopn: {e}')
    # TODO addtaskmgr
    global template_manager
    await template_manager.load_existing_values2()
    template_manager.set_follower(x.event.user_name)
    await template_manager.generate_file()


    logger.debug(f'{x.event.to_dict()}')

async def on_stream_online(x: StreamOnlineEvent, twitch):
    """
    callback fkt for stream online

    receives the data from stream_online Event
    """
    x.subscription.id
    x.subscription.created_at
    x.subscription.type
    broadcaster_user_id     = x.event.broadcaster_user_id
    event_id                = x.event.id
    started_at              = x.event.started_at
    event_type              = x.event.type
    logger.info(f'Eventdata:\n{x.event.to_dict()}')

async def on_stream_offline(x: StreamOfflineEvent, twitch):
    """
    callback fkt for stream offline

    receives the data from stream_offline Event
    """
    logger.info(f'Eventdata:\n{x.event.to_dict()}')

async def on_channel_update_v2(x: ChannelUpdateEvent, twitch):
    """
    callback fkt for channel_update_v2

    receives the data from stream_online Event
    """
    logger.info(f'Eventdata:\n{x.event.to_dict()}')

async def on_channel_update(x: ChannelUpdateEvent, twitch):
    """
    callback fkt for channel_update

    receives the data from channel_update Event
    """
    logger.info(f'Eventdata:\n{x.event.to_dict()}')

async def on_goal_begin(x: GoalEvent, twitch):
    """
    goal begin
    """
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    x.event.type 
    x.event.target_amount
    x.event.current_amount
    #print(f'{x.event.is_achieved} asdf..............................') # crash? TODO find out why no exception-info...... 
    logger.info(f'started an new goal: {x.event.type}:{x.event.current_amount}/{x.event.target_amount}')

async def on_goal_progress(x: GoalEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_goal_end(x: GoalEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
      

async def on_poll_begin(x: GoalEvent, twitch):
    """
    poll begin
    """
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_poll_progress(x: GoalEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_poll_end(x: GoalEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_prediction_begin(x: ChannelPredictionEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_prediction_end(x: ChannelPredictionEvent, twitch ):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_prediction_progress(x: ChannelPredictionEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_prediction_lock(x: ChannelPredictionEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_reward_add(x: ChannelPointsCustomRewardAddEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_reward_remove(x: ChannelPointsCustomRewardRemoveEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_reward_update(x: ChannelPointsCustomRewardUpdateEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_redemption_add(x: ChannelPointsCustomRewardRedemptionAddEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_redemption_update(x: ChannelPointsCustomRewardRedemptionUpdateEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')

async def on_auto_redemption(x: ChannelPointsAutomaticRewardRedemptionAddEvent, twitch):
    '''
    https://dev.twitch.tv/docs/eventsub/eventsub-reference/#channel-points-automatic-reward-redemption-add-event
    '''
    logger.info(f'Eventdata\n{x.event.to_dict()}')
    
    redeemed_at = x.event.redeemed_at
    user_name = x.event.user_name
    user_msg = x.event.message.text
    reward_information = x.event.reward
    reward_type = x.event.reward.type

    rewardtypes = {"single_message_bypass_sub_mode"     : on_auto_reward_bypass_message, 
                    "send_highlighted_message"          : on_auto_reward_highlight_message, 
                    "random_sub_emote_unlock"           : on_auto_reward_random_sub_emote, 
                    "chosen_sub_emote_unlock"           : on_auto_reward_chosen_sub_emote,
                    "chosen_modified_sub_emote_unlock"  : on_auto_reward_modified_sub_emote,
                    "message_effect"                    : on_auto_reward_message_effect,
                    "gigantify_an_emote,"               : on_auto_reward_gigantify_emote,
                    "celebration"                       : on_auto_reward_celebration}

    if reward_type in rewardtypes:
        handler = rewardtypes[reward_type]

        await handler(x,twitch)



async def on_hype_train_begin(x: HypeTrainEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    
async def on_hype_train_end(x: HypeTrainEndEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    
async def on_hype_train_progress(x: HypeTrainEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    
async def on_ban(x: ChannelBanEvent, twitch ):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    
async def on_unban(x: ChannelUnbanEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    
async def on_unban_request_create(x: ChannelUnbanRequestCreateEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    
async def on_unban_request_resolve(x: ChannelUnbanRequestResolveEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    
async def on_charity_donate(x: CharityDonationEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_charity_progress(x: CharityCampaignProgressEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    
async def on_charity_start(x: CharityCampaignStartEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
            
async def on_charity_stop(x: CharityCampaignStopEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_subscribe(x: ChannelSubscribeEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    
    
async def on_subscription_end(x: ChannelSubscriptionEndEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    

async def on_subscription_gift(x: ChannelSubscriptionGiftEvent, twitch):
    logger.info(f'-------------------------------------------------------')
    logger.info(f'häEventdata:\n{x.event.to_dict()}')
    logger.info(f'-------------------------------------------------------')
    
    username = x.event.user_name
    
    total = x.event.cumulative_total
    cnt = x.event.total
    if x.event.is_anonymous:
        username = "anonymous"
    #if x.event.tier>1:
    #    pass
    msg = f'{username} verschenkt {cnt} sabs, WTF - Danke! '
  
    try:
        lock = asyncio.Lock()
        
        async with lock:
            global subcnt
            subcnt += int(x.event.total)
            async with aiofiles.open("/home/snafu/src/scripte_twitch/data_files/subs.txt", "w") as f:
                await f.write(f"Subs: {subcnt}/1")

    except Exception as e:
        logger.error(f'exceptiopn: {e}')

    logger.info("hmmm")
    
    try:
        proc = await asyncio.create_subprocess_exec(
                                'espeak-ng', '-v', 'mb-de1', msg )
        xy = await proc.wait()
    except Exception as e:
        logger.error(f'exception s..: {e}')

async def on_subscription_message(x: ChannelSubscriptionMessageEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    logger.info(f'XXXX .. {x.event.message.text} \t{type(x.event.message)}')
    msg = f"resub nachricht von {x.event.user_name} {x.event.message.text}"
    proc = await asyncio.create_subprocess_exec(
        'espeak-ng', '-v', 'mb-de1', msg
 
    )
    await proc.wait()
    x.event.user_name
    x.event.tier
    x.event.duration_months
    x.event.cumulative_months

    
    
async def on_shoutout_create(x: ChannelShoutoutCreateEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    
async def on_shoutout_receive(x: ChannelShoutoutReceiveEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    x.event.from_broadcaster_user_name
    x.event.started_at
    x.event.viewer_count

    msg = f'{x.event.from_broadcaster_user_name} hat vor {x.event.viewer_count} zuschauern kostenlose werbung für mich gemacht, danke'

    proc = await asyncio.create_subprocess_exec(
        'espeak-ng', '-v', 'mb-de1', msg
 
    )
    await proc.wait()

async def on_channel_cheer(x: ChannelCheerEvent, twitch):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    user_name = x.event.user_name
    msg = x.event.message
    bits = x.event.bits

    msg = f'{x.event.user_name} schmeisst {x.event.bits} gramm Fischfutter in den Teich mit der Nachricht: {x.event.message}'
    proc = await asyncio.create_subprocess_exec(
        'espeak-ng', '-v', 'mb-de1', msg
 
    )
    await proc.wait()

