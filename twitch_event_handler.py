from twitchAPI.object.eventsub import ChannelSubscribeEvent, ChannelRaidEvent, ChannelFollowEvent,StreamOnlineEvent,StreamOfflineEvent,ChannelUpdateEvent, GoalEvent, ChannelPredictionEvent, ChannelPointsCustomRewardRedemptionUpdateEvent, ChannelPointsCustomRewardRedemptionAddEvent,ChannelPointsCustomRewardUpdateEvent,ChannelPointsCustomRewardRemoveEvent, ChannelPointsCustomRewardAddEvent, HypeTrainEvent, HypeTrainEndEvent, ChannelUnbanRequestResolveEvent,ChannelBanEvent,ChannelUnbanEvent, ChannelUnbanRequestCreateEvent, CharityCampaignProgressEvent, CharityCampaignStartEvent, CharityCampaignStopEvent, CharityDonationEvent, ChannelSubscriptionEndEvent, ChannelSubscriptionGiftEvent, ChannelSubscriptionMessageEvent, ChannelShoutoutCreateEvent, ChannelShoutoutReceiveEvent
import logging
import colorlog
import subprocess



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

async def eventchecker(x):
    if isinstance(x, ChannelSubscribeEvent):
        pass


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
    

async def onSubscribe( x: ChannelSubscribeEvent):
    """
    displays the data received by the channel_subscribe Event
    """
    await send_to_log(x)
    blub = f'{x.event.user_name} just subscribed'
    subprocess.run(['xcowsay', '--monitor',  '1', blub, '--image=' '/home/snafu/Downloads/cow.png', '--think' ,'--bubble-at=-230,-6',  ])
    
    logger.info('received subscribtion')
    logger.debug(f'{x.event.to_dict()}')
    
async def on_channel_raid(x: ChannelRaidEvent):
    """
    displays the data received by the channel_subscribe Event
    """
    blub = f'{x.event.from_broadcaster_user_name} just raided with {x.event.viewers} viewer'
    subprocess.run(['xcowsay', '--monitor',  '1', blub, '--image=' '/home/snafu/Downloads/cow.png', '--think' ,'--bubble-at=-230,-6',  ])
    logger.info(f'received channel raid')
    logger.debug(f'{x.event.to_dict()}')

async def on_follow(x: ChannelFollowEvent):
    """
    displays the data received by the channel_follow_v2 Event
    details: https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/#channel-follow-webhook-notification-example
    relevant parts: x.event.
    https://dev.twitch.tv/docs/eventsub/eventsub-reference/
    """
    
    blub = f'{x.event.user_name} just followed'
    subprocess.run(['xcowsay', '--monitor',  '1', blub, '--image=' '/home/snafu/Downloads/cow.png', '--think' ,'--bubble-at=-230,-6',  ])
    logger.info(f'received follow event')
    logger.debug(f'{x.event.to_dict()}')

async def on_stream_online(x: StreamOnlineEvent):
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
    
async def on_stream_offline(x: StreamOfflineEvent):
    """
    callback fkt for stream offline

    receives the data from stream_offline Event
    """
    logger.info(f'Eventdata:\n{x.event.to_dict()}')

async def on_channel_update_v2(x: ChannelUpdateEvent):
    """
    callback fkt for channel_update_v2

    receives the data from stream_online Event
    """
    logger.info(f'Eventdata:\n{x.event.to_dict()}')

async def on_channel_update(x: ChannelUpdateEvent):
    """
    callback fkt for channel_update

    receives the data from channel_update Event
    """
    logger.info(f'Eventdata:\n{x.event.to_dict()}')

async def on_goal_begin(x: GoalEvent):
    """
    goal begin
    """
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_goal_progress(x: GoalEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_goal_end(x: GoalEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass  

async def on_poll_begin(x: GoalEvent):
    """
    poll begin
    """
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_poll_progress(x: GoalEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_poll_end(x: GoalEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_prediction_begin(x: ChannelPredictionEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_prediction_end(x: ChannelPredictionEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_prediction_progress(x: ChannelPredictionEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_prediction_lock(x: ChannelPredictionEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_reward_add(x: ChannelPointsCustomRewardAddEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_reward_remove(x: ChannelPointsCustomRewardRemoveEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_reward_update(x: ChannelPointsCustomRewardUpdateEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_redemption_add(x: ChannelPointsCustomRewardRedemptionAddEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_redemption_update(x: ChannelPointsCustomRewardRedemptionUpdateEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_hype_train_begin(x: HypeTrainEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_hype_train_end(x: HypeTrainEndEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_hype_train_progress(x: HypeTrainEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_ban(x: ChannelBanEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_unban(x: ChannelUnbanEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_unban_request_create(x: ChannelUnbanRequestCreateEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_unban_request_resolve(x: ChannelUnbanRequestResolveEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_charity_donate(x: CharityDonationEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_charity_progress(x: CharityCampaignProgressEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_charity_start(x: CharityCampaignStartEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass
        
async def on_charity_stop(x: CharityCampaignStopEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_subscribe(x: ChannelSubscribeEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_subscription_end(x: ChannelSubscriptionEndEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_subscription_gift(x: ChannelSubscriptionGiftEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass 

async def on_subscription_message(x: ChannelSubscriptionMessageEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_shoutout_create(x: ChannelShoutoutCreateEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

async def on_shoutout_receive(x: ChannelShoutoutReceiveEvent):
    logger.info(f'Eventdata:\n{x.event.to_dict()}')
    pass

logger = logging.getLogger(__name__)
logger = add_logger_handler(logger)
logger.setLevel(logging.DEBUG)