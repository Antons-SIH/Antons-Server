from pytz import timezone
from datetime import datetime

def nowTime():
    return(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f'))