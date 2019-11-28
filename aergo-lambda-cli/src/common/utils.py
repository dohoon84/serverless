import time
import datetime

# YYYY-MM-DD HH:MM:SS 같이 날짜+시간을 문자열로 리턴
def getCurrentStrTime() :
    return time.strftime("%Y-%m-%d %H:%M:%S")