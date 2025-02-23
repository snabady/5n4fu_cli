import sqlite3
import div_help


class myDB:
    
    def __init__(self):
        self.conn = sqlite3.connect("snafu.db")
        self.cursor = conn.cursor()

    def insertFollower(self, followername):
        
        self.cursor("""
        INSERT INTO followers (name, clientid,firstfollowed,datefollowed,isbanned,datebanned,hasnickname,nickname)
        VALUES (?,?,?,?,?,?,?,?)
        """, (followername,.....))
        
        self.conn.commit()
        
    
    # for coding..... live should be a clean add with client_id
    def insertFollowerDummy(self, followername):
        
        self.cursor.execute("""
        INSERT INTO followers (name,datefollowed,isbanned)
        VALUES (?,?,?)
        """, (followername, div_help.getDatetime(), 0))
        
        self.conn.commit()
        
        
        
    def getClientIdfromFollower(self, followername):
        
        self.cursor.execute("""
        SELECT clientid FROM followers WHERE name = ?
        """, (followername))
        
        return self.cursor.fetchone()
        
        
    # returns last inserted follower 
    def getLatestFollower(self):
        self.cursor.execute("""
        SELECT name FROM followers WHERE id = (SELECT MAX(id) FROM followers) 
        """)
        
        return self.cursor.fetchone()
        
        
    def closeConn(self):
        self.conn.close()
    
    def reConn(self):
        self.conn = sqlite3.connect("snafu.db")
        self.cursor = conn.cursor()