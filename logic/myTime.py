from datetime import datetime
from core.events import EVENTS
import time 
def getCurrentTime():
    now = datetime.now()
    return now.strftime("%H:%M")

def getCurrentDate():
    now = datetime.now()
    return {
        "day": now.strftime("%A"),
        "date": now.strftime("%d"),
        "month": now.strftime("%B"),
        "year": now.strftime("%Y")
    }


def scheduleTimer(seconds):
    EVENTS.append({
        "type": "timer",
        "trigger": time.time() + seconds
    })


def scheduleAlarm(hour, minute):
    from datetime import datetime, timedelta

    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if target.timestamp() <= time.time():
        target += timedelta(days=1)

    EVENTS.append({
        "type": "alarm",
        "trigger": target.timestamp()
    })
