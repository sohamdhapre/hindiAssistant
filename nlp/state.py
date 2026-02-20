
def initState() -> dict:

    #State
    return {
        "lastIntent": None,
        "lastDate": None,
        "entities": {},
        "result": {}

    }


def updateDialogueState(state: dict, intent: str, entities: dict, result: dict) -> tuple:

    finalIntent = intent
    state["entities"].update(entities)
    finalEntities = state["entities"]  
    lastResult = state["result"]

    if finalIntent == "unknown" and state.get("lastIntent"):
        finalIntent = state["lastIntent"]


    if finalIntent:
        state["lastIntent"] = finalIntent


    return finalIntent, finalEntities, state , lastResult
