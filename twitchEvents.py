from twitchAPI.twitch import Twitch, TwitchUser
from twitchAPI.type import AuthScope
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import ChannelSubscribeEvent, ChannelRaidEvent, ChannelFollowEvent
from twitchAPI.helper import first
from typing import Tuple, Optional
import os
from dotenv import load_dotenv
import logging
import colorlog

TARGET_SCOPES = [
                 AuthScope.MODERATOR_READ_FOLLOWERS,
                 AuthScope.USER_READ_CHAT,
                 AuthScope.CHANNEL_BOT, 
                 AuthScope.USER_READ_EMOTES,
                 AuthScope.CHAT_READ, 
                 AuthScope.CHAT_EDIT,
                 AuthScope.CHANNEL_MODERATE,
                 AuthScope.USER_READ_EMAIL,
                 AuthScope.MODERATOR_READ_FOLLOWERS,
                 AuthScope.CHANNEL_MANAGE_POLLS,
                 AuthScope.CHANNEL_READ_GOALS,
                 AuthScope.CHANNEL_READ_ADS,
                 AuthScope.CHANNEL_MODERATE,
                 AuthScope.USER_BOT,
                 AuthScope.BITS_READ,
                 AuthScope.MODERATOR_READ_BLOCKED_TERMS,
                 AuthScope.MODERATOR_READ_CHAT_SETTINGS,
                 AuthScope.MODERATOR_READ_MODERATORS,
                 AuthScope.MODERATOR_READ_VIPS,
                 AuthScope.MODERATOR_MANAGE_UNBAN_REQUESTS,
                 AuthScope.MODERATOR_MANAGE_BANNED_USERS,
                 AuthScope.MODERATOR_MANAGE_CHAT_MESSAGES,
                 AuthScope.MODERATOR_MANAGE_WARNINGS,
                 AuthScope.CHANNEL_MANAGE_VIPS,
                 AuthScope.MODERATION_READ,
                 AuthScope.CHANNEL_MANAGE_POLLS,
                 AuthScope.MODERATOR_MANAGE_BLOCKED_TERMS,
                 AuthScope.CHANNEL_MANAGE_PREDICTIONS,
                 AuthScope.CHANNEL_MANAGE_REDEMPTIONS,
                 AuthScope.MODERATOR_MANAGE_AUTOMOD,
                 AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
                 AuthScope.CHANNEL_READ_HYPE_TRAIN,
                 AuthScope.MODERATOR_MANAGE_SHIELD_MODE,
                 AuthScope.MODERATOR_READ_SUSPICIOUS_USERS,
                 AuthScope.MODERATOR_MANAGE_WARNINGS,
                 AuthScope.MODERATOR_READ_AUTOMOD_SETTINGS,
                 AuthScope.MODERATOR_MANAGE_SHOUTOUTS
                 ]


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
        
        load_dotenv()
        self.use_cli_conn= use_cli_conn
         
        self.setEnv()

            
    async def __aenter__(self):
        if self.use_cli_conn:
            self.eventsub, self.twitch, self.user = await self.climockingConn()
        else:
            self.eventsub, self.twitch, self.user = await self.prodConn()
        self.logger.debug("aenter")
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
        if self.use_cli_conn:
            self.BASE_URL           = os.getenv("BASE_URL")
            self.AUTH_BASE_URL      = os.getenv("AUTH_BASE_URL")
            self.CONNECTION_URL     = os.getenv("CONNECTION_URL")
            self.SUBSCRIPTION_URL   = os.getenv("SUBSCRIPTION_URL")
            self.CLI_S              = os.getenv("CLI_S")
            self.CLI_UID            = os.getenv("CLI_UID")
            self.CLI_ID             = os.getenv("CLI_ID")
        else:
            self.CLIENT_ID          = os.getenv("CLIENT_ID")
            self.CLIENT_S           = os.getenv("CLIENT_S")

    async def prodConn(self) -> Tuple[EventSubWebsocket, Twitch, TwitchUser]:
        """
        creates a connection to Twitch EventSub using websockets
        u need a app registered at twitch -> .env
        """
        twitch = await Twitch(self.CLIENT_ID, self.CLIENT_S,)
        helper = UserAuthenticationStorageHelper(twitch, TARGET_SCOPES)
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
                                 [AuthScope.CHANNEL_READ_SUBSCRIPTIONS], 
                                 auth_base_url=self.AUTH_BASE_URL)
        x = self.CLI_UID

        token = await auth.mock_authenticate(self.CLI_UID)
        await twitch.set_user_authentication(token,
                                             [AuthScope.CHANNEL_READ_SUBSCRIPTIONS])
        user = await first(twitch.get_users())
        eventsub = EventSubWebsocket(twitch,
                                    connection_url=self.CONNECTION_URL,
                                    subscription_url=self.SUBSCRIPTION_URL)
        
        return eventsub, twitch, user
    
    async def onSubscribe(self, x: ChannelSubscribeEvent):
        """
        displays the data received by the channel_subscribe Event
        """
        self.logger.info('received subscribtion')
        self.logger.debug(f'{x.event.to_dict()}')
        
    async def on_channel_raid(self, x: ChannelRaidEvent):
        """
        displays the data received by the channel_subscribe Event
        """
        self.logger.info(f'received channel raid')
        self.logger.debug(f'{x.event.to_dict()}')
        

    async def on_follow(self, x: ChannelFollowEvent):
        """
        displays the data received by the channel_follow_v2 Event
        details: https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/#channel-follow-webhook-notification-example
        relevant parts: x.event.
        https://dev.twitch.tv/docs/eventsub/eventsub-reference/
        """
        self.logger.info(f'received follow event')
        self.logger.debug(f'{x.event.to_dict()}')


    async def subCliEventsTEMPO(self):
        """
        currently tested cli stuff, working and useable 
        also working with your real twitch-app-creds
        """
        self.eventsub.start()
        sub_id = await self.eventsub.listen_channel_subscribe(self.user.id, 
                                                              self.onSubscribe)
        self.logger.info(f'twitch event trigger channel.subscribe -t {self.user.id} -u {sub_id} -T websocket')

        raid_id = await self.eventsub.listen_channel_raid(self.on_channel_raid, 
                                                          None,self.user.id)
        self.logger.info(f'twitch event trigger channel.raid -t {self.user.id} -u {raid_id} -T websocket')

        follow_id =await self.eventsub.listen_channel_follow_v2(self.user.id, 
                                                                self.user.id, 
                                                                self.on_follow)
        self.logger.info(f'twitch event trigger channel.follow -t {self.user.id} -u {follow_id} -T websocket')

   