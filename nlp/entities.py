import nlp.dictionaries as dicts

def extractEntities(tokens: list, intent: str) -> dict:
    entities = {}

    # --- MATH INTENT ---
    if intent == "math":
        entities["numbers"] = []
        for op, words in dicts.OPERATIONS.items():
            if any(w in tokens for w in words):
                entities["operation"] = op

        for token in tokens:
            # Check for word-numbers (ek, do, teen)
            if token in dicts.WORD_NUMS:
                entities["numbers"].append(dicts.WORD_NUMS[token])
            # Check for digit-strings ("10", "5")
            elif token.isnumeric():
                entities["numbers"].append(int(token))

    # --- DATE INTENT ---
    if intent == "date":
        for token in tokens:
            if token in dicts.DATE_KEYWORDS:
                entities["date_keyword"] = token
                break

    # --- TIME / ALARM / TIMER INTENT ---
    if intent == "time":
        
        # 1. Detect Mode (alarm, timer, current_time)
        entities["TIMEMODE"] = "current_time" # Default
        for mode, words in dicts.TIME_SCHEMA["mode"].items():
            if any(w in tokens for w in words):
                entities["TIMEMODE"] = mode
                break

    
        if entities["TIMEMODE"] == "timer":
            entities["target"] = {}
            target_seconds = 0
            
            # Simple parser: Look for number followed by unit
            for i, token in enumerate(tokens):
                value = None
                if token in dicts.WORD_NUMS:
                    value = dicts.WORD_NUMS[token]
                elif token.isnumeric():
                    value = int(token)
                
                if value is not None and i + 1 < len(tokens):
                    next_token = tokens[i+1]
                    # Check units (ghante, minute, second)
                    for unit, keywords in dicts.TIME_SCHEMA["units"].items():
                        if next_token in keywords:
                            entities["target"][unit] = value
            
            # Calculate total seconds
            target_seconds += entities["target"].get("hour", 0) * 3600
            target_seconds += entities["target"].get("minute", 0) * 60
            target_seconds += entities["target"].get("second", 0)
            
            entities["targetSeconds"] = target_seconds

        # 3. Handle ALARM ("Subah 6 baje ka alarm")
        elif entities["TIMEMODE"] == "alarm":
            entities["alarm_time"] = {"hour": 0, "minute": 0}
            
            # Detect AM/PM keywords
            is_pm = False
            is_am = False
            if any(w in tokens for w in ["shyaam", "shaam", "raat", "dopahar", "pm"]):
                is_pm = True
            if any(w in tokens for w in ["subah", "savere", "am"]):
                is_am = True

            # Extract numbers
            nums = []
            for token in tokens:
                if token in dicts.WORD_NUMS:
                    nums.append(dicts.WORD_NUMS[token])
                elif token.isnumeric():
                    nums.append(int(token))
            
            if nums:
                raw_hour = nums[0]
                raw_minute = nums[1] if len(nums) > 1 else 0
                
                # Logic to convert 12-hour to 24-hour format
                final_hour = raw_hour
                
                if is_pm and raw_hour < 12:
                    final_hour += 12
                elif is_am and raw_hour == 12:
                    final_hour = 0
                
                entities["alarm_time"]["hour"] = final_hour
                entities["alarm_time"]["minute"] = raw_minute

    # --- SENSOR INTENT ---
    if intent == "sensor":
        # Default to temperature/humidity since that's all we have
        entities["sensor_type"] = "all" 

    return entities