from ml.intentMl import classifyIntentML
from nlp.normalizer import normalize 
from nlp.normalizer import normalizeNumbers 
from nlp.tokenizer import tokenize
from nlp.entities import extractEntities
from nlp.state import initState, updateDialogueState
from logic.actions import routeAction
from response.generator import generateResponse
from core.events import EVENTS
import speech.listener
import speech.speaker
import ledControl
import time
import core


def processEvents(EVENTS: list):
    now = time.time()

    for event in core.events.EVENTS[:]:
        if event["trigger"] <= now:

            if event["type"] == "timer":
                print("टाइमर पूरा हुआ!\n")
                speech.speaker.speak("टाइमर पूरा हुआ!\n")
            elif event["type"] == "alarm":
                print("अलार्म बज रहा है!\n")
                speech.speaker.speak("अलार्म बज रहा है!\n")
            EVENTS.remove(event)


def main():
    print("शुरू करने के लिए असिस्टेंट बोलो\n")
  
    
    assistantActive = False


    speech.listener.startListener()
    speech.speaker.initSpeaker()
    speech.speaker.speak("शुरू करने के लिए असिस्टेंट बोलो\n")
    
    # MAIN LOOP
    while True:

        processEvents(EVENTS)

        
        micText = speech.listener.pollMicText()

        now = time.time()

        if core.flags.IS_SPEAKING.is_set():
            ledControl.ledAssistantSpeaking()
        else:
            ledControl.ledUserSpeaking()
        if not micText:
            continue

        if "असिस्ट" in micText:
            assistantActive = True
            print("Assistant activated")
            print("बाहर निकलने के लिए 'बंद करो' कहें\n")
            speech.speaker.speak("असिस्टेंट शुरू हो गया है, बाहर निकलने के लिए 'बंद करो' कहें\n")

            continue
            
        if not assistantActive:
            continue               
                
        userInput = micText

        normalized = normalizeNumbers(userInput)
        tokens = tokenize(normalize(userInput))
        intent = classifyIntentML(normalized)
        entities = extractEntities(tokens, intent)
        result = {}
        
        
        print("tokens", tokens, '\n')
        print("Entities", entities, '\n')
        print("Intent ", intent ,'\n')

        result = routeAction(intent, entities)
        response = generateResponse(intent, result)

        speech.speaker.speak(response)
        print("असिस्टेंट:", response)


        if intent == "exit":
            assistantActive = False
            ledControl.ledOff()
            speech.speaker.speak("शुरू करने के लिए असिस्टेंट बोलो\n")

        
if __name__ == "__main__":
    main()

