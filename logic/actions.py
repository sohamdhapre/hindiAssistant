import logic.myTime 
from datetime import datetime
import time
import logic.myTime
import adafruit_dht
import board
import logic.myTime
_activeTimers = []

DHT_SENSOR = adafruit_dht.DHT11   
dhtDevice = adafruit_dht.DHT11(board.D4)

DHT_PIN = 4

def handleSensor(entities):

    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity

        if temperature is None:
            return {"error": "sensor_fail"}

        return {
            "status": "temperature",
            "temp": round(temperature, 1),
            "humidity": round(humidity, 1) if humidity else None
        }

    except RuntimeError:
        return {"error": "sensor_fail"}

    except Exception as e:
        return {"error": "sensor_exception"}


def handleMath(intent, entities) -> dict:
    nums = entities.get("numbers", [])
    if "operation" in entities:
        operation = entities["operation"]
    else:
        result = "कृपया संचालन निर्दिष्ट करें"
        return {"custom": result}
    
    if len(nums) <2:
        result = "कृपया एक से अधिक संख्या दर्ज करें"
        return {"custom": result}



    if operation == "add":
        result = sum(nums)

    elif operation == "subtract":
        result = nums[0]
        for n in nums[1:]:
            result -= n

    elif operation == "multiply":
        
        result = 1
        for n in nums:
            result *= n
        
    elif operation == "divide":
        result = nums[0]
        for n in nums[1:]:
            if n == 0:
                return {"error": "divide_by_zero"}
            result /= n

    elif operation == '':
        return {"error": "unknown_intent"}

    return {"result": result}

 
def handleWeather(entities: dict) -> dict:

    city = entities.get("city", "आपके शहर")
    date = entities.get("date", "today")

    return {
        "city": city,
        "date": date,
        "temperature": 22,
        "condition": "साफ"
    }


def handleTime(entities):

    mode = entities.get("TIMEMODE")

    if mode == "current_time":

        now = datetime.now()

        return {
            "status": "showTime",
            "hour": now.hour,
            "minute": now.minute
        }


    if mode == "date":

        now = datetime.now()

        return {
            "status": "date",
            "day": now.strftime("%A"),
            "date": now.day,
            "month": now.strftime("%B"),
            "year": now.year
        }


    if mode == "timer":

        seconds = entities.get("targetSeconds")

        if not seconds:
            return {"error": "missingDuration"}

        logic.myTime.scheduleTimer(seconds)

        return {
            "status": "timerSet",
            "seconds": seconds
        }

    if mode == "alarm":

        logic.myTime.scheduleAlarm(entities["hour"], entities["minute"])

        return {
            "status": "alarmSet"
        }

    return {"error": "unknownTimeMode"}


def handleIdentity() -> dict:

    return {
        "name": "Hindi Assistant",
        "creator": "Soham"
    }


def handleExit() -> dict:

    return {
        "exit": True
    }



def routeAction(intent: str, entities: dict) -> dict:


    if intent == "date":
        return logic.myTime.getCurrentDate()

    if intent == "time":
        return handleTime(entities)

    if intent == "identity":
        return handleIdentity()

    if intent == "exit":
        return handleExit()

    if intent == "math":
        return handleMath(intent, entities)
    
    if intent == "sensor":
        return handleSensor(entities)

    
    if intent == "time":
        return handleTime(entities)
    


	
    return {
        "error": "unknown_intent"
    }

