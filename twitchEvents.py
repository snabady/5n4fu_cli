from twitchAPI.twitch import Twitch, TwitchUser
from twitchAPI.type import AuthScope
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import ChannelSubscribeEvent, ChannelRaidEvent, ChannelFollowEvent,StreamOnlineEvent,StreamOfflineEvent,ChannelUpdateEvent, GoalEvent
from twitchAPI.helper import first
from typing import Tuple, Optional
import os
from dotenv import load_dotenv
import logging
import colorlog
import twitch_event_handler as teh
import authscopes as auth_scope


class TwitchEvents:
    """
    Connects to Twitch-Event-Sub via websockets
    use .env for credentials and other settings

    (c) ChaosQueen 5n4fu
    """
    
    twitch: Optional[Twitch]                = None
    eventsub: Optional[EventSubWebsocket]   = None
    user: Optional[TwitchUser]              = None

    def __init__(self, 
                 use_cli_conn=False):
        """
        use_cli_conn    bool    default False
                                if True -> mock-cli is used instead of production
        send2Overlay    bool    default False
                                enables websocket to Overlay and sends JSON-Strings from events
        """
        self.logger = logging.getLogger(__name__)
        self.add_logger_handler()
        self.logger.setLevel(logging.DEBUG)
        
        load_dotenv(override=True)
        self.use_cli_conn= use_cli_conn
         
        self.setEnv()

            
    async def __aenter__(self):
        if self.use_cli_conn:
            self.eventsub, self.twitch, self.user = await self.climockingConn()
        else:
            self.eventsub, self.twitch, self.user = await self.prodConn()
        
        self.eventsub.start()
        self.logger.info("eventsub started successfully")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # ??? deconstructor
        await self.eventsub.stop()
        await self.twitch.close()
        self.logger.debug("aexit")
        return self
    
    def add_logger_handler(self):
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
        self.logger.addHandler(handler)
        

    def setEnv(self):
        """
        loads the .env variables
        adjust variables in .env File 
        """
        if self.use_cli_conn:
            self.BASE_URL           = os.getenv("BASE_URL") 
            self.AUTH_BASE_URL      = os.getenv("AUTH_BASE_URL")
            self.CONNECTION_URL     = os.getenv("CONNECTION_URL")
            self.SUBSCRIPTION_URL   = os.getenv("SUBSCRIPTION_URL")
            self.CLI_S              = os.getenv("CLI_S")
            self.CLI_UID            = os.getenv("CLI_UID")
            self.CLI_ID             = os.getenv("CLI_ID")

            self.logger.debug(f'BASE_URL: {self.BASE_URL or "NOT SET"}')
            self.logger.debug(f'AUTH_BASE_URL: {self.AUTH_BASE_URL or "NOT SET"}')
            self.logger.debug(f'CONNECTION_URL: {self.CONNECTION_URL or "NOT SET"}')
            self.logger.debug(f'SUBSCRIPTION_URL: {self.SUBSCRIPTION_URL or "NOT SET"}')
            self.logger.debug(f'CLI_S: {self.CLI_S or "NOT SET"}')
            self.logger.debug(f'CLI_UID: {self.CLI_UID or "NOT SET"}')
            self.logger.debug(f'CLI_ID: {self.CLI_ID or "NOT SET"}')

        else:
            self.CLIENT_ID          = os.getenv("CLIENT_ID")
            self.CLIENT_S           = os.getenv("CLIENT_S")

    async def prodConn(self) -> Tuple[EventSubWebsocket, Twitch, TwitchUser]:
        """
        creates a connection to Twitch EventSub using websockets
        u need a app registered at twitch -> .env
        """
        twitch = await Twitch(self.CLIENT_ID, self.CLIENT_S,)
        helper = UserAuthenticationStorageHelper(twitch, auth_scope.TARGET_SCOPES)
        await helper.bind()
        user = await first(twitch.get_users())

        eventsub = EventSubWebsocket(twitch)
        
        return eventsub, twitch, user

    async def climockingConn(self) -> Tuple[EventSubWebsocket, Twitch, TwitchUser]:
        """
        connect to mock-cli WS -> trigger commands per twitch cmdl
        connect to eventsocked
        and get the TwitchUser using this connection
        https://dev.twitch.tv/docs/cli/event-command/ event commands for twitch-cli
        credentials and server settings in .env

        TODO AuthScopes compare || check if normal working
        """
        self.logger.critical("a worm inserted your console")
        twitch = await Twitch(self.CLI_ID,
                            self.CLI_S,
                            base_url        = self.BASE_URL, 
                            auth_base_url   = self.AUTH_BASE_URL)
        twitch.auto_refresh_auth = False # cli needs no refreshing
        auth = UserAuthenticator(twitch, 
                                 auth_scope.CLI_SCOPES, 
                                 auth_base_url=self.AUTH_BASE_URL)
        x = self.CLI_UID

        token = await auth.mock_authenticate(self.CLI_UID)
        await twitch.set_user_authentication(token,
                                             auth_scope.CLI_SCOPES)
        user = await first(twitch.get_users())
        eventsub = EventSubWebsocket(twitch,
                                    connection_url=self.CONNECTION_URL,
                                    subscription_url=self.SUBSCRIPTION_URL)
        
        return eventsub, twitch, user
    
    

    async def subCliEventsTEMPO(self):
        """
        currently tested cli stuff, working and useable 
        also working with your real twitch-app-creds
        """
        try:
            self.eventsub.start()
            
            self.logger.info(f'copy&paste the following command to trigger an event')
            sub_id = await self.eventsub.listen_channel_subscribe(self.user.id, 
                                                                teh.onSubscribe)
            self.logger.info(f'twitch event trigger channel.subscribe -t {self.user.id} -u {sub_id} -T websocket')

            raid_id = await self.eventsub.listen_channel_raid(teh.on_channel_raid, 
                                                            None,self.user.id)
            self.logger.info(f'twitch event trigger channel.raid -t {self.user.id} -u {raid_id} -T websocket')

            follow_id = await self.eventsub.listen_channel_follow_v2(self.user.id, 
                                                                    self.user.id, 
                                                                    teh.on_follow)
            self.logger.info(f'twitch event trigger channel.follow -t {self.user.id} -u {follow_id} -T websocket')
        except Exception as e:
            self.logger.error(e)
         
    async def listen_stream_info_events(self):
        """
        EVENT_LISTENER

        subscribes to stream Info related Events - exactly to: 

            listen_stream_online
            listen_stream_offline
            listen_channel_update_v2
            listen_channel_update

        For more information see here: 
        https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types#streamonline
        https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types#streamoffline
        https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types#channelupdate
        https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types#streamoffline

        """
        streamonline_id     = await self.eventsub.listen_stream_online(self.user.id,
                                                                       teh.on_stream_online)  
        self.logger.debug(f'twitch event trigger stream.online -t {self.user.id} -u {streamonline_id} -T websocket') 

        streamoffline_id    = await self.eventsub.listen_stream_offline(self.user.id,
                                                                        teh.on_stream_offline)   
        self.logger.debug(f'twitch event trigger stream.offline -t {self.user.id} -u {streamoffline_id} -T websocket') 

        channelupdatev2_id  = await self.eventsub.listen_channel_update_v2(self.user.id,
                                                                           teh.on_channel_update_v2)
        self.logger.debug(f'twitch event trigger channel.update -t {self.user.id} -u {channelupdatev2_id} -T websocket') 

        channelupdate_id    = await self.eventsub.listen_channel_update(self.user.id,
                                                                        teh.on_channel_update)
        self.logger.debug(f'twitch event trigger channel.update -t {self.user.id} -u {channelupdate_id} -T websocket') 
        self.logger.info("successfully subscribed to stream_info_events")
    
    async def listen_channel_goal_events(self):
        """
        channel.goal.begin
        channel.goal.end 
        channel.goal.progress
        """

        goal_begin_id       = await self.eventsub.listen_goal_begin(self.user.id, teh.on_goal_begin)
        goal_end_id         = await self.eventsub.listen_goal_end(self.user.id, teh.on_goal_end)
        goal_progress_id    = await self.eventsub.listen_goal_progress(self.user.id, teh.on_goal_progress)

        self.logger.info("successfully subscribed to channel_goal_events")

        self.logger.debug(f'twitch event trigger channel.goal.begin -t {self.user.id} -u {goal_begin_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.goal.end -t {self.user.id} -u {goal_end_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.goal.progress -t {self.user.id} -u {goal_progress_id} -T websocket') 

    async def listen_channel_polls(self):
        """
        channel.poll.begin 
        channel.poll.end
        channel.poll.progress   
        """
        poll_begin_id       = await self.eventsub.listen_channel_poll_begin(self.user.id, teh.on_poll_begin) 
        poll_end_id         = await self.eventsub.listen_channel_poll_end(self.user.id, teh.on_poll_end)
        poll_progress_id    = await self.eventsub.listen_channel_poll_progress(self.user.id, teh.on_poll_progress)

        self.logger.info("successfully subscribed to channel_poll_events")

        self.logger.debug(f'twitch event trigger channel.poll.begin -t {self.user.id} -u {poll_begin_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.poll.end -t {self.user.id} -u {poll_end_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.poll.progress -t {self.user.id} -u {poll_progress_id} -T websocket') 

    async def listen_channel_predictions(self):
        """
        channel.prediction.begin
        channel.prediction.end
        channel.prediction.lock
        channel.prediction.progress
        """

        prediction_begin_id         = await self.eventsub.listen_channel_prediction_begin(self.user.id, teh.on_prediction_begin)
        prediction_end_id           = await self.eventsub.listen_channel_prediction_end(self.user.id, teh.on_prediction_end)
        prediction_lock_id          = await self.eventsub.listen_channel_prediction_lock(self.user.id, teh.on_prediction_lock)
        prediction_progress_id      = await self.eventsub.listen_channel_prediction_progress(self.user.id, teh.on_prediction_progress)

        self.logger.info("successfully subscribed to channel_prediction_events")

        self.logger.debug(f'twitch event trigger channel.prediction.begin -t {self.user.id} -u {prediction_begin_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.prediction.end -t {self.user.id} -u {prediction_end_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.prediction.lock -t {self.user.id} -u {prediction_lock_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.prediction.progress -t {self.user.id} -u {prediction_progress_id} -T websocket') 


    async def listen_channel_points(self):
        """
        channel.channel_points_custom_reward.add 
        channel.channel_points_custom_reward.remove 
        channel.channel_points_custom_reward.update 
        channel.channel_points_custom_reward_redemption.add
        channel.channel_points_custom_reward_redemption.update
        """
        reward_add_id        = await self.eventsub.listen_channel_points_custom_reward_add(self.user.id, teh.on_reward_add)
        reward_remove_id     = await self.eventsub.listen_channel_points_custom_reward_remove(self.user.id, teh.on_reward_remove)
        reward_update_id     = await self.eventsub.listen_channel_points_custom_reward_update(self.user.id, teh.on_reward_update)
        redemption_add_id    = await self.eventsub.listen_channel_points_custom_reward_redemption_add(self.user.id, teh.on_redemption_add)
        redemption_update_id = await self.eventsub.listen_channel_points_custom_reward_redemption_update(self.user.id, teh.on_redemption_update)

        self.logger.info("successfully subscribed to channel_point_events")

        self.logger.debug(f'twitch event trigger channel.channel_points_custom_reward.add -t {self.user.id} -u {reward_add_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.channel_points_custom_reward.remove -t {self.user.id} -u {reward_remove_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.channel_points_custom_reward.update -t {self.user.id} -u {reward_update_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.channel_points_custom_reward_redemption.add -t {self.user.id} -u {redemption_add_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.channel_points_custom_reward_redemption.update -t {self.user.id} -u {redemption_update_id} -T websocket') 


    async def listen_hype_train(self):
        """
        channel.hype_train.begin 
        channel.hype_train.end 
        channel.hype_train.progress
        """

        hype_train_begin_id    = await self.eventsub.listen_hype_train_begin(self.user.id, teh.on_hype_train_begin)
        hype_train_end_id      = await self.eventsub.listen_hype_train_end(self.user.id, teh.on_hype_train_end)
        hype_train_progress_id = await self.eventsub.listen_hype_train_progress(self.user.id, teh.on_hype_train_progress)

        self.logger.info("successfully subscribed to hype_train_events")

        self.logger.debug(f'twitch event trigger channel.hype_train.begin -t {self.user.id} -u {hype_train_begin_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.hype_train.end -t {self.user.id} -u {hype_train_end_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.hype_train.progress -t {self.user.id} -u {hype_train_progress_id} -T websocket') 


    async def listen_ban_events(self):
        """
        ATTENTION: PROBABLY NOT WORKING WITHIN CLI!


        channel.ban 
        channel.unban
        channel.unban_request.create
        channel.unban_request.resolve
        TODO: mod? ->


        """
        ban_id                = await self.eventsub.listen_channel_ban(self.user.id, teh.on_ban)
        unban_id              = await self.eventsub.listen_channel_unban(self.user.id, teh.on_unban)
        unban_request_id      = await self.eventsub.listen_channel_unban_request_create(self.user.id, self.user.id, teh.on_unban_request_create)
        unban_request_resolve = await self.eventsub.listen_channel_unban_request_resolve(self.user.id, self.user.id, teh.on_unban_request_resolve)

        self.logger.info("successfully subscribed to ban_events")

        self.logger.debug(f'twitch event trigger channel.ban -t {self.user.id} -u {ban_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.unban -t {self.user.id} -u {unban_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.unban_request.create -t {self.user.id} -u {unban_request_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.unban_request.resolve -t {self.user.id} -u {unban_request_resolve} -T websocket') 
        pass



    async def listen_charity_events(self):
        """
        channel.charity_campaign.donate 
        channel.charity_campaign.progress
        channel.charity_campaign.start 
        channel.charity_campaign.stop
        """
        charity_donate_id   = await self.eventsub.listen_channel_charity_campaign_donate(self.user.id, teh.on_charity_donate)
        charity_progress_id = await self.eventsub.listen_channel_charity_campaign_progress(self.user.id, teh.on_charity_progress)
        charity_start_id    = await self.eventsub.listen_channel_charity_campaign_start(self.user.id, teh.on_charity_start)
        charity_stop_id     = await self.eventsub.listen_channel_charity_campaign_stop(self.user.id, teh.on_charity_stop)

        self.logger.info("successfully subscribed to charity_events")

        self.logger.debug(f'twitch event trigger channel.charity_campaign.donate -t {self.user.id} -u {charity_donate_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.charity_campaign.progress -t {self.user.id} -u {charity_progress_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.charity_campaign.start -t {self.user.id} -u {charity_start_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.charity_campaign.stop -t {self.user.id} -u {charity_stop_id} -T websocket') 
        pass

    async def listen_shoutout_events(self):
        """
        channel.shoutout.create
        channel.shoutout.receive
        """
        shoutout_create_id  = await self.eventsub.listen_channel_shoutout_create(self.user.id, self.user.id, teh.on_shoutout_create)
        shoutout_receive_id = await self.eventsub.listen_channel_shoutout_receive(self.user.id, self.user.id,  teh.on_shoutout_receive)

        self.logger.info("successfully subscribed to shoutout_events")

        self.logger.debug(f'twitch event trigger channel.shoutout.create -t {self.user.id} -u {shoutout_create_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.shoutout.receive -t {self.user.id} -u {shoutout_receive_id} -T websocket') 
        pass

    async def listen_subscribe_events(self):
        """
        channel.subscribe
        channel.subscription.end
        channel.subscription.gift
        channel.subscription.message
        """
        subscribe_id          = await self.eventsub.listen_channel_subscribe(self.user.id, teh.on_subscribe)
        sub_end_id            = await self.eventsub.listen_channel_subscription_end(self.user.id, teh.on_subscription_end)
        sub_gift_id           = await self.eventsub.listen_channel_subscription_gift(self.user.id, teh.on_subscription_gift)
        sub_message_id        = await self.eventsub.listen_channel_subscription_message(self.user.id, teh.on_subscription_message)

        self.logger.info("successfully subscribed to subscribe_events")

        self.logger.debug(f'twitch event trigger channel.subscribe -t {self.user.id} -u {subscribe_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.subscription.end -t {self.user.id} -u {sub_end_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.subscription.gift -t {self.user.id} -u {sub_gift_id} -T websocket') 
        self.logger.debug(f'twitch event trigger channel.subscription.message -t {self.user.id} -u {sub_message_id} -T websocket') 

    async def listen_moderate_events(self):
        """
        channel.moderator.add 
        channel.moderator.remove
        channel.ad_break.begin 
        """

    async def listen_channel_action_events(self):
        """
        channel.cheer 
        channel.follow 
        channel.raid 
        """

    async def collection_of_events_not_supported_with_cli(self):
        """
        ATTENTION: you cant use this fct. when self.use_cli = True! only in production or simulation
        """
        #await eventsub.listen_channel_suspicious_user_message(user.id, user.id,  onSuspiciosUserMessage)
        #await eventsub.listen_channel_suspicious_user_update(user.id, user.id, onSuspiciousUserUpdate)
        #await eventsub.listen_channel_warning_send(user.id, user.id, onWarningSend)
        #await eventsub.listen_channel_warning_acknowledge(user.id,user.id, onWarningAcknowledge)

        #await eventsub.listen_automod_message_hold(user.id, user.id, onAutomodMessageHold)
        #await eventsub.listen_automod_message_update(user.id, user.id, onAutomodMessageUpdate)
        #await eventsub.listen_automod_terms_update(user.id, user.id, onAutomodTermsUpdate)
        #await eventsub.listen_automod_settings_update(user.id, user.id , onAutomodSettingsUpdate)

        #await eventsub.listen_channel_points_automatic_reward_redemption_add(user.id, onPointsAutoRewardRedemptionAdd)
        #await eventsub.listen_channel_chat_clear(user.id,user.id, onChatClear)
        #await eventsub.listen_channel_chat_clear_user_messages(user.id, user.id, onChatClearUserMessages)

        #await eventsub.listen_channel_chat_notification(user.id, user.id, onChatNotification)


        #await eventsub.listen_channel_chat_notification(user.id, user.id, onChatNotification)
        #await eventsub.listen_channel_cheer(user.id, onChannelCheer)

        #await eventsub.listen_channel_moderate(user.id,user.id, onChannelModerate)
        #await eventsub.listen_channel_moderator_add(user.id,   onChannelModeratorAdd)
        #await eventsub.listen_channel_moderator_remove(user.id,  onModeratorRemove)
        #await eventsub.listen_channel_vip_add(user.id,onVipAdd)
        #await eventsub.listen_channel_vip_remove(user.id,onVipRemove)
        #await eventsub.listen_channel_chat_message(user.id , user.id, onChatMessage)