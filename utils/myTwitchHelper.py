from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.helper import first
from twitchAPI.object.api import GetEmotesResponse
from twitchAPI.object.api import TwitchUser
import logging
import json

import asyncio
import sys
sys.path.append('utils/')
import utils.mydb
twitch = None

#USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT,AuthScope.CHANNEL_MODERATE,AuthScope.USER_READ_EMAIL,AuthScope.MODERATOR_READ_FOLLOWERS,AuthScope.CHANNEL_MANAGE_POLLS]
USER_SCOPE = [AuthScope.MODERATOR_READ_FOLLOWERS,AuthScope.USER_READ_CHAT,AuthScope.CHANNEL_BOT, AuthScope.USER_READ_EMOTES,AuthScope.CHAT_READ, AuthScope.CHAT_EDIT,AuthScope.CHANNEL_MODERATE,AuthScope.USER_READ_EMAIL,AuthScope.MODERATOR_READ_FOLLOWERS,AuthScope.CHANNEL_MANAGE_POLLS]

twitchapp="snafu"

def logger(msg):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("*** myTwitchHelper ")
        logger.info(str(msg))

def createPollData(braodcaster_id,title,choices):
     jchoices= json.dumps({})

     data = {
          "broadcaster_id": braodcaster_id,
          "title": title,
          "choices": jchoices 
     }
     
     
async def getUserId(user_name) -> TwitchUser:
    logger("user: " + str(user_name))
    client_id, client_secret = utils.mydb.getTwitchAppCred("snafu")
   
    twitch = await Twitch(client_id, client_secret)
    helper = UserAuthenticationStorageHelper(twitch,USER_SCOPE)
    await helper.bind()

    twitchUser = await first(twitch.get_users(logins=[str(user_name).strip()]))#
    #logger(str(twitchUser))
    await twitch.close()
    
    return twitchUser

async def getStreams(user_id):
    logger("getStreams")
    client_id, client_secret = utils.mydb.getTwitchAppCred(twitchapp)
    global twitch
    twitch = await Twitch(client_id, client_secret)
    helper = UserAuthenticationStorageHelper(twitch,USER_SCOPE)
    await helper.bind()

    result = await first(twitch.get_streams(None,None,1,None,None,[user_id],None,None,)     )
    #logger(result)

    if result != None:
        return result.user_name
    else:
         return None
    


async def getGlobalEmotes():
    client_id,client_secret = utils.mydb.getTwitchAppCred(twitchapp)
    twitch = await Twitch(client_id,client_secret)
    global_emotes = await twitch.get_global_emotes()
    logger(type(global_emotes))
    emotes = global_emotes.to_dict() #GetEmotesResponse
    
    for x in global_emotes:
        if x == None:
             logger("okay?")
        utils.mydb.insertEmote(x, "global", None)
        logger(x.name)



async def getChannelEmotes(broadcasterId, twitch):
     logger("getChannelEmotes")
     # if not already in DB
     #client_id, client_secret = utils.mydb.getTwitchAppCred(twitchapp)
     #twitch = await Twitch(client_id, client_secret)

     channelEmotes = await twitch.get_channel_emotes(broadcasterId)
     logger("got emotes for : " + str(broadcasterId))
     for x in channelEmotes:
          #logger(str(x))
          
          utils.mydb.insertEmote(x, "channel", broadcasterId)


async def getEmoteSet(emote_set_id):
    logger("helper getEmoteSEt")
    client_id,client_secret = utils.mydb.getTwitchAppCred(twitchapp)
    twitch = await Twitch(client_id,client_secret)
    emoteSet = await twitch.get_emote_sets(emote_set_id)
    logger("###################" + str(emote_set_id))
    #logger(str(type(emoteSet)))
    emoteSet = emoteSet.to_dict()
    
    logger(str(emoteSet))
    for x in emoteSet:
     
        #utils.mydb.insertEmote(x)
        logger("blub ********* **************" )


    logger("----------------->gooood bye emotes set")

async def run():

    client_id, client_secret = utils.mydb.getTwitchAppCred(twitchapp)
    helper = UserAuthenticationStorageHelper(twitch,USER_SCOPE)
    await helper.bind()
    twitch = await Twitch(client_id, client_secret)
    
    
    auth = UserAuthenticator(twitch, USER_SCOPE)

    return twitch
  #  token, refresh_token = await auth.authenticate()
   # await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)



