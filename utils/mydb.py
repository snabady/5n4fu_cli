import datetime
import sqlite3
import sys
sys.path.append('utils/')
import utils.div_help
import logging
from twitchAPI.chat import ChatMessage
import utils.myTwitchHelper
from twitchAPI.object.api import TwitchUser
import json
from twitchAPI.twitch import Twitch
import asyncio

#dotenv?
dbpath = "c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db"

def getTwitchAppCred(client_name):
    
    conn,cursor = getConn()
    cursor.execute("""
                select client_id, client_secret
                from credentials
                where client_name = ?
           """, (client_name,))
    gnarf=  cursor.fetchone()
    client_id = gnarf[0]
    client_secret = gnarf[1]
    
    return client_id, client_secret


def logger(msg):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("*** dbInfo")
        logger.info(str(msg))
        

def getConn():
    conn = sqlite3.connect(dbpath,check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = conn.cursor()
    return conn, cursor

def logError(msg):
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger("dbError")
    logger.error("*** myDB ***: " + str(msg))


def checkTwitchUserExists(user_name):
    conn,curr = getConn()
    logger("adding x to db: "+ user_name)
    """"""
    curr.execute("""
                 select * from chat where username = ? and userId not Null""", 
                 (user_name.strip(),))
    res = curr.fetchmany()
    #logger(str(res))
    if res != None:
        return False
    return True


# TODO db for raid_received
def insertChannelRaidReceived(from_broadcaster_user_id, 
                              from_broadcaster_user_name, 
                              viewers,
                              eventtype ):
    query = """
            insert into Events (eventtype,
                                timetriggered, 
                                from_broadcaster, 
                                from_broadcaster_id, 
                                viewer)
            values (?,?,?,?,?)
            """
    con, cur = getConn()
    cur.execute(query,(eventtype, datetime.datetime.now(), from_broadcaster_user_name, from_broadcaster_user_id, viewers))    
    con.commit()
    con.close()
    

def insertEmote(emotedata, type, ownerId):

    logger("insert emote db")
    #logger(type == "setid")
    
    emotedata.name
    emotedata.images
    emotedata.format
    emotedata.scale
    emotedata.theme_mode
    conn, curr = getConn()

    if type == "channel":
        
        logger("EMOTEDATA: " + str(emotedata))
        curr.execute("""insert into twitchEmotes (id,name,images,format,scale,theme_mode,userId)
            values (?,?,?,?,?,?,?) on conflict(id) do nothing
                    """, (str(emotedata.id), str(emotedata.name), str(emotedata.images), str(emotedata.format), str(emotedata.scale), str(emotedata.theme_mode), str(ownerId)))
        
    
    if type == "global":
        curr.execute("""insert into twitchEmotes (id,name,images,format,scale,theme_mode)
            values (?,?,?,?,?,?)on conflict(id) do nothing
                    """, (str(emotedata.id), str(emotedata.name), str(emotedata.images), str(emotedata.format), str(emotedata.scale), str(emotedata.theme_mode)))
    conn.commit()
    conn.close()

    
def twitchUser2(usr , isFollower):
    #print("ja moin aus twitchUser / db")
     #logger(str(usr))
     #logger(type(usr))
     #print(dir(usr))
     
     usr.created_at
     usr.description
     usr.id
     usr.login
     usr.offline_image_url
     usr.profile_image_url
     usr.view_count
     usr.type
     usr.login
     usr.display_name
     usr.broadcaster_type

     conn, curr = getConn()
     curr.execute("""insert into twitchUserDetails( 
                    userid,
                    broadcaster_type,
                    description,
                    login,
                    offline_image_url,
                    profile_image_url, 
                    view_count,
                    type,
                    display_name,
                    isfollower )
                  Values (?,?,?,?,?,?,?,?,?,?) on conflict(userid) do nothing""", (usr.id,usr.broadcaster_type,usr.description,usr.login,usr.offline_image_url,usr.profile_image_url,usr.view_count,usr.type,usr.display_name,"1" ))
     conn.commit()
     conn.close()
     return True

def twitchUser(usr ):
    #print("ja moin aus twitchUser / db")
     logger(str(usr))
     logger(type(usr))
     print(dir(usr))
     
     usr.created_at
     usr.description
     usr.id
     usr.login
     usr.offline_image_url
     usr.profile_image_url
     usr.view_count
     usr.type
     usr.login
     usr.display_name
     usr.broadcaster_type

     conn, curr = getConn()
     curr.execute("""insert into twitchUserDetails( 
                    userid,
                    broadcaster_type,
                    description,
                    login,
                    offline_image_url,
                    profile_image_url, 
                    view_count,
                    type,
                    display_name )
                  Values (?,?,?,?,?,?,?,?,?) on conflict(userid) do nothing""", (usr.id,usr.broadcaster_type,usr.description,usr.login,usr.offline_image_url,usr.profile_image_url,usr.view_count,usr.type,usr.display_name))
     conn.commit()
     conn.close()
     return True

def getFollowerImages():
    query = """
            select x.profile_image_url from (select distinct(userid), profile_image_url  from twitchUserDetails where isfollower="1")as x
            """
    cur,con = getConn()
    res = con.execute(query)
    ret = res.fetchall()
    cur.commit()
    cur.close()
    return ret

def insertChatJoins(u,t, jt):
    query = """
            insert into chatjoins ( username,
                                    timereceived,
                                    jointype)
            values (?,?,?)
            """
    conn,cur = getConn()
    cur.execute(query, (u,t,jt))
    conn.commit()
    conn.close()
    return True

def inserthtmlChad(htmlPrintable, msg_id, msgdatecreate, usr_color,chatter_user_id,    chatter_user_name ,displayed ):
    #logger("inserthtmlchad: " + msg_id)
    query = """INSERT INTO htmlchad (id, htmlfull, datecreated,dateinserted, userid, username, displayed) VALUES (?, ?, ?, ?, ?,?, ?) on conflict(id) do nothing"""
    conn, cur = getConn()
    res = cur.execute(query,(msg_id,
                             str(htmlPrintable),
                             msgdatecreate,
                             datetime.datetime.now().timestamp() ,
                             chatter_user_id,
                             chatter_user_name,
                             displayed))
    conn.commit()
    conn.close()
    return True


def emoteExists(emoteOwnerId, emoteId):
    query = """
            select * from twitchEmotes where userid=? or id=?
            """
    con, cur = getConn()
    res = cur.execute(query, (emoteOwnerId,emoteId))
    x = res.fetchone()
    #logger(str(type(x)))
    #logger(str(x))
    
    if isinstance(x , type(None)):
        logger("MOFOO ISI NONONNONONONO")
        return False
    else:
        return True
    


def getEmoteURL(isize,eid):
    # select images from twitchEmotes where id = 425618
    #logger("hello from getEmoteURL")
    conn,cur = getConn()
    res = cur.execute("""select images from twitchEmotes where id = ?""", (str(eid),))
    yolo = json.dumps(res.fetchone())
    isizestart = yolo.rfind(isize)
    #logger(f"0: {yolo}")
    #logger(f"startpt: {str(isizestart)}")
    yolo = yolo[int(isizestart):-1]
    #logger(f"1: {yolo}")
    yolo = yolo[6:-1]
    #logger(f".:{yolo}")
    startpt = yolo.find("\'")
    #logger(f"start: {str(startpt)} + endpt: {str(len(yolo))}")
    yolo = yolo[0:int(startpt) +1]
    #logger(f"2: {yolo}")
    endpoint = yolo.find("\'")
    #logger(f"endpiont: {str(endpoint)}")
    yolo = yolo[0 :int(endpoint)]
    logger(f"final_url: {yolo}")
    
    conn.commit()
    conn.close()
    return yolo


# - chat related data
def addNewTwitchUser(msg: ChatMessage):
    usr = msg.user
    usr_id = usr.id
    usr_type = usr.user_type
    isVip = usr.vip
    display_name = usr.display_name
    color = usr.color
    isMod = usr.mod
    isSub = usr.subscriber
    conn, cursor = getConn()
    cursor.execute ("""INSERT INTO twitchUser (userId, userType, isVip, displayName, color, isMod, isSub) 
                       VALUES (?, ?, ?, ?, ?, ? ,?) on conflict(userid) do nothing
                    """, (usr_id,usr_type,isVip,display_name,color,isMod, isSub))
    conn.commit()
    conn.close()

def getChat(limit):# sql preparen für: usr-img, emote-images, emote coord, msg
    conn, curr = getConn()
    #query = """select * from htmlchad order by dateinserted desc limit ?"""
    query = """
            select x.*,t.profile_image_url from htmlchad x 
            join twitchUserDetails t on x.userid = t.userid
            where displayed ="0"
            order by x.dateinserted desc 
            limit ?
            """
    res = curr.execute(query,(str(limit)))
    ret=[]
    for x in res:
        ret.append(x)
    conn.commit()
    conn.close()

    return ret


def userExists(chatter_user_id):
    query = """ select * from twitchUserDetails 
                where userid=?
            """
    conn, curr = getConn()
    res = curr.execute(query, (str(chatter_user_id),))
    #logger( res.fetchone() is None)
    if res.fetchone() is None:
        return False
    else:
        return True


def setChatDisplayed(msgid):
    conn, cur = getConn()
    query = """ update htmlchad
                set displayed="1"
                where id = ?
            """
    cur.execute(query,(str(msgid),))
    conn.commit()
    conn.close()
    
def getGlobalEmoteUrls(emoteId):
    conn, cur = getConn()
    query = """
                select images from twitchEmotes where name = ?
            """
    
    res = cur.execute(query, (emoteId,))
    x = res.fetchone()

    conn.commit()
    conn.close()
    return x



        
async def chatLog(msg: ChatMessage):
    
    #logger(msg.fragments)
    sent_timestamp = msg.sent_timestamp
    isFirstMsg = msg.first
    emotes = msg.emotes # next chapter
    #logger(str(type(emotes)))
    #logger(emotes)
    
    text = msg.text
    username = msg.user.name 
    user = await utils.myTwitchHelper.getUserId(username)
    user_id = user.id
    hasUserId = checkTwitchUserExists(username)
    
    logger("isFirstMsg: " + str(isFirstMsg) + " " + str(type(isFirstMsg)))
    logger("hasUserId: " + str(hasUserId) + " " + str(type(hasUserId)))
    #logger(isFirstMsg or not hasUserId)
    if isFirstMsg or not hasUserId:
        addNewTwitchUser(msg)
    conn, cursor = getConn()
    cursor.execute(
    """INSERT INTO "chat" ("username", "msg", "_datetime", "isFirstMsg", "emotes", "userId") 
    VALUES (?,?,?,?,?,?)
    """, (username, text, sent_timestamp, isFirstMsg==True ,str(emotes),int(user_id)))
    


    #utils.myTwitchHelper.getEmoteSet()
    conn.commit()
    conn.close()


def insertTwitchUser():
    pass


def insertFollower( followername):
    #logger("in insertFollowerDummy")
    conn = sqlite3.connect("snafu.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO follower (name, clientid,firstfollowed,datefollowed,isbanned,datebanned,hasnickname,nickname)
    VALUES (?,?,?,?,?,?,?,?)
    """, (followername,))
    conn.set_trace_callback(trace_callback)

    conn.commit()
    conn.close()
    

# for coding..... live should be a clean add with client_id
def insertFollowerDummy(followername):
    #logger("in insertFollowerDummy")
    conn, cursor = getConn()
    try:
        cursor.execute("""
        INSERT INTO follower (name,datefollowed,hasShoutout)
        VALUES (?,?,?)
        """, (followername, utils.div_help.getDatetime(), 0))
    except sqlite3.Error as e:
        #logError(e)
        logger(followername + " already followed, not adding to followers.")
        # refollow in DB loggen (firstfollow, latestfollow, followcount :D)
    conn.commit()
    conn.close()
    
def getLastFollowerSent():   
    pass
    
def getClientIdfromFollower(followername):
    #logger("in getClientIdfromFollower")
    conn = sqlite3.connect("c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db",check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = getCursor(conn)
    
    cursor.execute("""
    SELECT clientid FROM follower WHERE name = ?
    """, (followername,))
    
    client_id = cursor.fetchone()
    
    conn.close()
    return client_id
    
def getIdfromFollower(followername):
    #logger("in getIdfromFollower")
    conn = sqlite3.connect("c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db",check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = getCursor(conn)
    
    cursor.execute("""
    SELECT id FROM follower WHERE name = ?
    """, (followername,))
    
    client_id = cursor.fetchone()
    
    conn.close()
    return client_id
    
def trace_callback(sql):
    logger("Executing SQL:", sql)
    
def setlatestFollowerShoutout(followername):
    #logger("in setlatestFollowerShoutout")
    conn = sqlite3.connect("c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db",check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = getCursor(conn)
    #logger(followername)
    try:
        cursor.execute("""
            UPDATE status
            SET status = ?
            WHERE name = 'lastFollowerSent'
            """, ( followername,))
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e: 
        logError (e)
        
    
def getLatestFollowerShoutout():
    #logger("in getLatestFollowerShoutout")
    conn = sqlite3.connect("c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db",check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = conn.cursor()
    #print
    cursor.execute("""
        SELECT status FROM status 
        WHERE name = ?
        """,('lastFollowerSent',))
    latest_shoutout = cursor.fetchone()
    #
    # logger("DBDBDB: latest_shoutout" + str(latest_shoutout))
    
    conn.commit()
    conn.close()
    
    return latest_shoutout
    
def setShoutoutFlag(follower_name):
    #logger("in setlatestFollowerShoutout")
    conn = sqlite3.connect("c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db",check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = getCursor(conn)
    try:
        cursor.execute("""
            UPDATE follower
            SET hasShoutout = 1
            WHERE name = ?
            """, ( follower_name,))
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e: 
        logger (e)
 
# returns last inserted follower 
def get_notShoutoutedFollowers():
    #logger("in get_notShoutoutedFollowers")
    conn = sqlite3.connect("c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db",check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT name FROM follower WHERE hasShoutout = 0 
    """)
    latest_follower = cursor.fetchall()
    #logger("latest_follower: " + str(latest_follower))
    conn.close()
    return latest_follower
    

def getLatestFollower():
    #logger("in getLatestFollower")
    conn = sqlite3.connect("c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db",check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT name FROM follower WHERE id = (SELECT MAX(id) FROM follower) 
    """)
    latest_follower = cursor.fetchone()
    #logger("latest_follower from DBDBDB;: " + str(latest_follower))
    conn.close()


def getAllFollowerIds():
    query = """
            select distinct userid from twitchFollower
            """
    con, cur = getConn()
    res = cur.execute(query)
    result = res.fetchall()
    con.close()
    return result 


def insertStreamSession(eventid,  eventtime, isonline):
    query = """
            insert into stream_sessions (event_id,event_start, is_online) 
            values (?,?,?)
            """
    con,cur = getConn()
    cur.execute(query, (eventid,eventtime, isonline))
    con.commit()
    con.close()
    
def insertTwitchFollower(username, userid, followdate):
    query = """
            insert into twitchFollower (userid, username, followdate,insertdate)
            values (?,?,?,?)
            """
    con, cur = getConn()
    cur.execute(query, (userid, username, followdate,datetime.datetime.now().timestamp()))
    con.commit()
    con.close()


def getLatestFollowerOverlay():
    #logger("in getLatestFollowerOverlay")
    conn = sqlite3.connect("c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db",check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT name,hasShoutout FROM follower WHERE id = (SELECT MAX(id) FROM follower) 
    """)
    res = cursor.fetchone()
    latest_follower = res[0]
    hasShoutout = res[1]
    conn.close()
    return hasShoutout, latest_follower
    
    
def deleteFollower():
    conn = sqlite3.connect("c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db",check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = conn.cursor()
    
    cursor.execute("""
    DELETE from follower 
    """)
    conn.commit()
    conn.close()
    
def getTodos():
    #logger("in getTodos")
    conn = sqlite3.connect("c:\\users\\snafu\\desktop\\hyperb\\db\\snafu.db",check_same_thread=False)
    conn.set_trace_callback(trace_callback)
    cursor = conn.cursor()
    cursor.execute("""
        select kurztext from todos where isDone is 0 
    """)
    
    todos_time = utils.div_help.getTimeNow()
    todos = cursor.fetchall()
    #logger(todos)
    #logger(type(todos))
    conn.close()
    
    return todos




    


def insertChannelUpdate():
    getConn();
    
def closeConn(conn):
    conn.close()

def getDBconn():
    return 

def getCursor(conn):
    return conn.cursor()