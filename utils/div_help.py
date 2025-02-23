from datetime import datetime

def getTimeNow():
    return datetime.now()

def getDatetime():
    now = datetime.now()
    return now.strftime( "%Y-%m-%d %H:%M:%S" )
    
    
def getDatetime_short():
    
    now = datetime.now()
    return now.strftime( "%H:%M - %d.%m.%y" )