from twitchAPI.type import AuthScope
from twitchAPI.object.eventsub import ChannelSubscribeEvent, ChannelRaidEvent, ChannelFollowEvent,StreamOnlineEvent,StreamOfflineEvent,ChannelUpdateEvent, GoalEvent
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
CLI_SCOPES = [AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
              AuthScope.CHANNEL_READ_HYPE_TRAIN,
              AuthScope.CHANNEL_MANAGE_POLLS,
              AuthScope.BITS_READ,
              AuthScope.CHANNEL_MANAGE_POLLS,
              AuthScope.CHANNEL_READ_GOALS,
              AuthScope.CHANNEL_MANAGE_POLLS,
              AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
              AuthScope.CHANNEL_READ_HYPE_TRAIN,
              AuthScope.CHANNEL_MANAGE_PREDICTIONS,
              AuthScope.CHANNEL_MANAGE_REDEMPTIONS,
              AuthScope.MODERATOR_MANAGE_SHOUTOUTS
              
                 
                 ]

#AuthScope.CHANNEL_MANAGE_POLLS,
#AuthScope.CHANNEL_READ_ADS