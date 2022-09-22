# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Dict, Text, List, Optional, Any
from rasa_sdk.forms import FormValidationAction
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

class ValidateInterviewtForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_interview_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Text]:
        additional_slots = []
        
        updated_slots = domain_slots.copy()
        
        
        if tracker.slots.get("internship") is not None:
            additional_slots.append("internship")
            
        if tracker.slots.get("future") is not None:
            updated_slots.remove("future")
            additional_slots.append("future2")
            additional_slots.append("motiv")
        
        text_of_last_user_message = tracker.latest_message.get("text")
        if ("course" in text_of_last_user_message or "curriculum" in text_of_last_user_message):# and not tracker.slots.get("motiv"):
            additional_slots.append("courses")
            
#    dispatcher.utter_message(text = str(example))

        return additional_slots + updated_slots

    async def extract_internship(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
    
        d = {"internship": None}
        for entity in tracker.latest_message['entities']:
            if entity["entity"] == "internship":
                d["internship"] = entity["value"]
        
        return d
        
    async def extract_future(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
    
        print(tracker.latest_message['entities'][0])
        d = {"future": tracker.slots.get("future")}
        
        for entity in tracker.latest_message['entities']:
            if entity["entity"] == "future":
                d["future"] = entity["value"]
        print(d)
        
        return d
                    
#        text_of_last_user_message = tracker.latest_message.get("text")
        
    async def extract_name(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        name = tracker.slots.get("name")
        if name is not None:
            return {"name": name}
        try:
            name = next(tracker.get_latest_entity_values(entity_type="PERSON"))
        except:
            return {"name": None}
            
        return {"name": name}
