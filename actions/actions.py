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
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json

ANSWER = 4000

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
        
        
#        if tracker.slots.get("internship") is not None:
#            additional_slots.append("internship2")
#
#        if tracker.slots.get("future") is not None:
#            updated_slots.remove("future")
#            additional_slots.append("future2")
#            additional_slots.append("motiv")
        
        text_of_last_user_message = tracker.latest_message.get("text")
#        if ("course" in text_of_last_user_message or "curriculum" in text_of_last_user_message) and not tracker.slots.get("topic"):
#            additional_slots.append("courses")
            
        if "help" in text_of_last_user_message:
            if tracker.slots.get("math1") is None:
                additional_slots.append("math1")
            elif tracker.slots.get("math2") is None:
                additional_slots.append("math2")
            elif tracker.slots.get("math3") is None:
                additional_slots.append("math3")
            elif tracker.slots.get("math4") is None:
                additional_slots.append("math4")
                
        if "yes" in text_of_last_user_message:
            if tracker.slots.get("math2") is None:
                additional_slots.append("math2")
            elif tracker.slots.get("math3") is None:
                additional_slots.append("math3")
            elif tracker.slots.get("math4") is None:
                additional_slots.append("math4")
                
        if "no" in text_of_last_user_message:
            if tracker.slots.get("math2") is None:
                additional_slots.append("no1")
            elif tracker.slots.get("math3") is None:
                additional_slots.append("no2")
            else:
                additional_slots.append("no3")
            
#    dispatcher.utter_message(text = str(example))

        return additional_slots + updated_slots

#    async def extract_internship(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
#    ) -> Dict[Text, Any]:
#
#        d = {"internship": None}
#        for entity in tracker.latest_message['entities']:
#            if entity["entity"] == "internship":
#                d["internship"] = entity["value"]
#        return d
        
#    async def extract_future(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
#    ) -> Dict[Text, Any]:
#
#        d = {"future": tracker.slots.get("future")}
#        for entity in tracker.latest_message['entities']:
#            if entity["entity"] == "future":
#                d["future"] = entity["value"]
#        return d
                    
#        text_of_last_user_message = tracker.latest_message.get("text")
        
#    async def extract_name(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
#    ) -> Dict[Text, Any]:
#
#        d = {"name": tracker.slots.get("name")}
#        for entity in tracker.latest_message['entities']:
#            if entity["entity"] == "PERSON":
#                d["name"] = entity["value"]
#        return d

#    async def extract_topic(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
#    ) -> Dict[Text, Any]:
#
#        d = {"topic": tracker.slots.get("topic")}
#        for entity in tracker.latest_message['entities']:
#            if entity["entity"] == "topic":
#                d["topic"] = entity["value"]
#        return d
        
    def validate_mathdone1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        """Validate value."""
        if int(slot_value.lower()) == ANSWER:
            dispatcher.utter_message(text="Well done, you found the right answer.")
        else:
            dispatcher.utter_message(text="Unfortunately, your answer is not correct.")
        return {"mathdone1": slot_value}

#
#class ValidateMathForm(FormValidationAction):
#    def name(self) -> Text:
#        return "validate_math_form"
#
#    async def required_slots(
#        self,
#        domain_slots: List[Text],
#        dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#        domain: "DomainDict",
#    ) -> List[Text]:
#        additional_slots = []
#
#        updated_slots = domain_slots.copy()
#
#        text_of_last_user_message = tracker.latest_message.get("text")
#        if "help" in text_of_last_user_message:
#            if tracker.slots.get("math1") is None:
#                additional_slots.append("math1")
#            elif tracker.slots.get("math2") is None:
#                additional_slots.append("math2")
#            elif tracker.slots.get("math3") is None:
#                additional_slots.append("math3")
#
#        if "yes" in text_of_last_user_message:
##            updated_slots.remove("math1")
#            if tracker.slots.get("math2") is None:
#                additional_slots.append("math2")
#            elif tracker.slots.get("math3") is None:
#                additional_slots.append("math3")
#
#        if "no" in text_of_last_user_message:
#            if tracker.slots.get("math2") is None:
#                additional_slots.append("no1")
#            elif tracker.slots.get("math3") is None:
#                additional_slots.append("no2")
#            else:
#                additional_slots.append("no3")
#
#        return additional_slots + updated_slots

#    def extract_help(
#        self,
#        slot_value: Any,
#        dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#        domain: "DomainDict",
#    ) -> Dict[Text, Any]:
#        text_of_last_user_message = tracker.latest_message.get("text")
#        if "no" in text_of_last_user_message:
#            return {"help": None}
#        return {"help": tracker.slots.get("help")}

#    def validate_mathdone1(
#        self,
#        slot_value: Any,
#        dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#        domain: "DomainDict",
#    ) -> Dict[Text, Any]:
#        """Validate value."""
#        if int(slot_value.lower()) == ANSWER:
#            dispatcher.utter_message(text="Well done, you found the right answer.")
#        else:
#            dispatcher.utter_message(text="Unfortunately, your answer is not correct.")
#        return {"mathdone1": slot_value}