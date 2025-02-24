from twitchAPI.object.eventsub import ChannelSubscribeEvent, ChannelRaidEvent, ChannelFollowEvent,StreamOnlineEvent,StreamOfflineEvent,ChannelUpdateEvent, GoalEvent, ChannelPredictionEvent, ChannelPointsCustomRewardRedemptionUpdateEvent, ChannelPointsCustomRewardRedemptionAddEvent,ChannelPointsCustomRewardUpdateEvent,ChannelPointsCustomRewardRemoveEvent, ChannelPointsCustomRewardAddEvent, HypeTrainEvent, HypeTrainEndEvent, ChannelUnbanRequestResolveEvent,ChannelBanEvent,ChannelUnbanEvent, ChannelUnbanRequestCreateEvent, CharityCampaignProgressEvent, CharityCampaignStartEvent, CharityCampaignStopEvent, CharityDonationEvent, ChannelSubscriptionEndEvent, ChannelSubscriptionGiftEvent, ChannelSubscriptionMessageEvent, ChannelShoutoutCreateEvent, ChannelShoutoutReceiveEvent
import logging
import colorlog



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

async def onSubscribe( x: ChannelSubscribeEvent):
    """
    displays the data received by the channel_subscribe Event
    """
    logger.info('received subscribtion')
    logger.debug(f'{x.event.to_dict()}')
    
async def on_channel_raid(x: ChannelRaidEvent):
    """
    displays the data received by the channel_subscribe Event
    """
    logger.info(f'received channel raid')
    logger.debug(f'{x.event.to_dict()}')
    

async def on_follow(x: ChannelFollowEvent):
    """
    displays the data received by the channel_follow_v2 Event
    details: https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/#channel-follow-webhook-notification-example
    relevant parts: x.event.
    https://dev.twitch.tv/docs/eventsub/eventsub-reference/
    """
    logger.info(f'received follow event')
    logger.debug(f'{x.event.to_dict()}')

async def on_stream_online(x: StreamOnlineEvent):
    """
    callback fkt for stream online

    receives the data from stream_online Event
    """
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
    pass
async def on_goal_progress(x: GoalEvent):
    pass
async def on_goal_end(x: GoalEvent):
    pass
    
async def on_poll_begin(x: GoalEvent):
    """
    poll begin
    """
    pass
async def on_poll_progress(x: GoalEvent):
    pass
async def on_poll_end(x: GoalEvent):
    pass


async def on_prediction_begin(x: ChannelPredictionEvent):
    pass
async def on_prediction_end(x: ChannelPredictionEvent):
    pass
async def on_prediction_progress(x: ChannelPredictionEvent):
    pass
async def on_prediction_lock(x: ChannelPredictionEvent):
    pass

async def on_reward_add(x: ChannelPointsCustomRewardAddEvent):
    pass

async def on_reward_remove(x: ChannelPointsCustomRewardRemoveEvent):
    pass
async def on_reward_update(x: ChannelPointsCustomRewardUpdateEvent):
    pass
async def on_redemption_add(x: ChannelPointsCustomRewardRedemptionAddEvent):
    pass
async def on_redemption_update(x: ChannelPointsCustomRewardRedemptionUpdateEvent):
    pass

async def on_hype_train_begin(x: HypeTrainEvent):
    pass

async def on_hype_train_end(x: HypeTrainEndEvent):
    pass

async def on_hype_train_progress(x: HypeTrainEvent):
    pass


async def on_ban(x: ChannelBanEvent):
    pass

async def on_unban(x: ChannelUnbanEvent):
    pass

async def on_unban_request_create(x: ChannelUnbanRequestCreateEvent):
    pass

async def on_unban_request_resolve(x: ChannelUnbanRequestResolveEvent):
    pass


async def on_charity_donate(x: CharityDonationEvent):
    pass

async def on_charity_progress(x: CharityCampaignProgressEvent):
    pass

async def on_charity_start(x: CharityCampaignStartEvent):
    pass
        
async def on_charity_stop(x: CharityCampaignStopEvent):
    pass

async def on_subscribe(x: ChannelSubscribeEvent):
    pass

async def on_subscription_end(x: ChannelSubscriptionEndEvent):
    pass

async def on_subscription_gift(x: ChannelSubscriptionGiftEvent):
    pass 

async def on_subscription_message(x: ChannelSubscriptionMessageEvent):
    pass

async def on_shoutout_create(x: ChannelShoutoutCreateEvent):
    pass

async def on_shoutout_receive(x: ChannelShoutoutReceiveEvent):
    pass



logger = logging.getLogger(__name__)
logger = add_logger_handler(logger)
logger.setLevel(logging.DEBUG)