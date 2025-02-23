import sqlite3
import div_help

def getDBconn():
    return sqlite3.connect("snafu.db")

def getCursor(conn):
    return conn.cursor()

def insertFollower( followername):
    conn = sqlite3.connect("snafu.db")
    cursor = conn.cursor()
    cursor("""
    INSERT INTO followers (name, clientid,firstfollowed,datefollowed,isbanned,datebanned,hasnickname,nickname)
    VALUES (?,?,?,?,?,?,?,?)
    """, (followername,.....))
    
    conn.commit()
    conn.close()
    

# for coding..... live should be a clean add with client_id
def insertFollowerDummy(followername):
    conn = getDBConn()
    cursor = getCursor(conn)
    
    cursor.execute("""
    INSERT INTO followers (name,datefollowed,isbanned)
    VALUES (?,?,?)
    """, (followername, div_help.getDatetime(), 0))
    
    conn.commit()
    conn.close()
    
    
    
def getClientIdfromFollower(followername):
    
    conn = getDBConn()
    cursor = getCursor(conn)
    
    cursor.execute("""
    SELECT clientid FROM followers WHERE name = ?
    """, (followername))
    
    client_id = cursor.fetchone()
    
    conn.close()
    return client_id
    
    
# returns last inserted follower 
def getLatestFollower():
    conn = getDBConn()
    cursor = getCursor(conn)
    
    cursor.execute("""
    SELECT name FROM followers WHERE id = (SELECT MAX(id) FROM followers) 
    """)
    latest_follower = cursor.fetchone()
    conn.close()
    return latest_follower
    
    
def closeConn(conn):
    conn.close()
