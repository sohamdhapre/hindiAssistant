import nlp.dictionaries as dict

def generateTimeResponse(result):

    status = result.get("status")


    if status == "showTime":
        return f"अभी समय {result['hour']} बजकर {result['minute']} मिनट है।"


    if status == "date":
        return (
            f"आज {result['day']} है, "
            f"तारीख {result['date']} "
            f"{result['month']} {result['year']}।"
        )


    if status == "timerSet":
        return "टाइमर सेट कर दिया गया है।"


    if status == "alarmSet":
        return "अलार्म सेट कर दिया गया है।"

    if result.get("error") == "missingDuration":
        return "कितने समय का टाइमर लगाना है?"

    return "मैं समय से संबंधित यह आदेश समझ नहीं पाया।"

def generateCustomError(result: dict) -> str:
    return result["custom"]

def generateDateResponse(result: dict) -> str:
    return (
        f"आज {dict.DAYS[result['day']]} है, "
        f"तारीख {result['date']} "
        f"{dict.MONTHS[result['month']]} {result['year']}।"
    )

def generateMath(result: dict) -> str: 
    if "result" in result:
        return f"जवाब है: {result['result']} ।"
    else:
        return generateErrorResponse()

def generateIdentityResponse(result: dict) -> str:
    return "मैं एक हिंदी वॉयस असिस्टेंट हूँ।"

def generateExitResponse() -> str:
    return "ठीक है, अलविदा।"

def generateErrorResponse() -> str:
    return "माफ़ कीजिए, मैं यह समझ नहीं पाया।"

def generateResponse(intent: str, result: dict) -> str:
    
    if "custom" in  result:
        return generateCustomError(result)

    if intent == "date":
        return generateDateResponse(result)

    if intent == "time":
        return generateTimeResponse(result)

    if intent == "identity":
        return generateIdentityResponse(result)

    if intent == "math":
        return generateMath(result)
   
    if intent == "sensor":
        return generateSensorResponse(result)

    if intent == "exit":
        return generateExitResponse()

    return generateErrorResponse()

def generateSensorResponse(result):

    status = result.get("status")

    if status == "temperature":

        temp = result["temp"]

        if result.get("humidity") is not None:
            hum = result["humidity"]
            return f"कमरे का तापमान {temp} डिग्री और आर्द्रता {hum} प्रतिशत है।"

        return f"कमरे का तापमान {temp} डिग्री सेल्सियस है।"

    if result.get("error") == "sensor_fail":
        return "सेंसर से डेटा नहीं मिला।"

    return "सेंसर समझ नहीं आया।"
