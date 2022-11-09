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

ANSWER = 2000
ANSWER2 = 2

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

        if tracker.slots["requested_slot"] == "sport" and tracker.slots.get("sport") == "yes":
            updated_slots.remove("music")
            updated_slots.remove("music1")
            updated_slots.remove("music2")
            updated_slots.remove("music3")
            updated_slots.remove("extra")
        elif tracker.slots["requested_slot"] == "sport" and tracker.slots.get("sport") == "no":
            updated_slots.remove("sport1")
            
        if tracker.slots["requested_slot"] == "music" and tracker.slots.get("sport") == "no":
            updated_slots.remove("music1")
            updated_slots.remove("music2")
            updated_slots.remove("music3")
        elif tracker.slots["requested_slot"] == "music" and tracker.slots.get("yes") == "yes":
            updated_slots.remove("extra")
                
        if tracker.slots["requested_slot"] == "math1" and tracker.slots.get("math1") == "yes":
            updated_slots.remove("no1")
        if tracker.slots["requested_slot"] == "math2" and tracker.slots.get("math2") == "yes":
            updated_slots.remove("no2")
        if tracker.slots["requested_slot"] == "math3" and tracker.slots.get("math3") == "yes":
            updated_slots.remove("no3")
                
        if (tracker.slots["requested_slot"] == "startmath" or tracker.slots["requested_slot"] == "no1" or tracker.slots["requested_slot"] == "no2" or tracker.slots["requested_slot"] == "math3") and "done" in text_of_last_user_message.lower():
            updated_slots.remove("no1")
            updated_slots.remove("no2")
            updated_slots.remove("math1")
            updated_slots.remove("math2")
            updated_slots.remove("math3")
            updated_slots.remove("help")

        return additional_slots + updated_slots
        
    def validate_sport(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] != "sport":
            return {"sport": tracker.slots.get("sport")}
        slot_value = slot_value[:-1].lower().split(" ")
        print(slot_value)
        if "don't" in slot_value or "not" in slot_value or "never" in slot_value or "no" in slot_value or "haven't" in slot_value:
            return {"sport": "no"}
        else: # "do" in slot_value or "have" in slot_value or "yes" in slot_value:
            return {"sport": "yes"}
        return {"sport": None}
        
    def validate_music(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] != "music":
            return {"music": tracker.slots.get("music")}
        slot_value = slot_value[:-1].lower().split(" ")
        if "don't" in slot_value or "never" in slot_value or "not" in slot_value or "no" in slot_value or "haven't" in slot_value:
            return {"music": "no"}
        else:
            return {"music": "yes"}
        return {"music": None}
        
    def validate_music1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] != "music1":
            return {"music1": tracker.slots.get("music1")}
        if "wave" in slot_value.lower():
            dispatcher.utter_message(text="Exactly! Sound can be represented as a wave.")
        else:
            dispatcher.utter_message(text="That's not correct, sound can be represented as a wave.")
        return {"music1": "done"}
        
    def validate_music2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] != "music2":
            return {"music2": tracker.slots.get("music2")}
        if "frequency" in slot_value.lower() or "period" in slot_value.lower():
            dispatcher.utter_message(text="That's correct! Changing the frequency of a sound will affect it's pitch.")
        else:
            dispatcher.utter_message(text="That's not correct, changing the frequency of a sound will affect it's pitch.")
        return {"music2": slot_value}
        
    def validate_music3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] != "music3":
            return {"music3": tracker.slots.get("music3")}
        if "magnitude" in slot_value.lower() or "amplitude" in slot_value.lower():
            dispatcher.utter_message(text="Well done! Changing the amplitude of a sound will affect it's volume.")
        else: # "do" in slot_value or "have" in slot_value or "yes" in slot_value:
            dispatcher.utter_message(text="That's not correct, changing the amplitude of a sound will affect it's volume.")
        return {"music3": slot_value}
        
    def validate_mathdone1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        answer = None
        try:
            slot_value = slot_value[:-1]
            words = slot_value.split(" ")
            for w in words:
                try:
                    answer = float(w)
                    if "minus" in slot_value:
                        answer = -answer
                except ValueError:
                    continue
            
            if answer == ANSWER or answer == ANSWER2:
                dispatcher.utter_message(text="Well done, you found the right answer.")
            elif answer==ANSWER*2 or answer==ANSWER2*2:
                dispatcher.utter_message(text="You were so close, but this is not the right answer.")
            else:
                dispatcher.utter_message(text="Unfortunately, your answer is not correct. ")
        except ValueError:
            dispatcher.utter_message(text="Sorry, I couldn't process your answer. Please provide the numerical value you found.")
            return {"mathdone1": None}
        return {"mathdone1": str(answer)}
        
    def validate_mathdone2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        dispatcher.utter_message(text="Thanks for walking me through your reasoning. Let me give you the answer, so that you can compare your attempt with the soliution. TO ADD")
        return {"mathdone2": tracker.slots.get("mathdone2")}
                    
                    
    def validate_no1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        """Validate value."""
        if tracker.slots["requested_slot"] != "no1":
            return {"no1": tracker.slots.get("no1")}
        if "done" in slot_value.lower() or "help" in slot_value.lower():
            return {"no1": slot_value}
        return {"no1": None}
        
    def validate_math1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] != "math1":
            return {"math1": tracker.slots.get("math1")}
        slot_value = slot_value[:-1].lower().split(" ")
        if "didn't" in slot_value or "not" in slot_value or "no" in slot_value or "haven't" in slot_value:
            return {"math1": "no"}
        elif "did" in slot_value or "have" in slot_value or "yes" in slot_value:
            return {"math1": "yes"}
        return {"math1": None}
            
    def validate_math2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] != "math2":
            return {"math2": tracker.slots.get("math2")}
        slot_value = slot_value[:-1].lower().split(" ")
        if "didn't" in slot_value or "not" in slot_value or "no" in slot_value or "haven't" in slot_value:
            return {"math2": "no"}
        elif "did" in slot_value or "have" in slot_value or "yes" in slot_value:
            return {"math2": "yes"}
        return {"math2": None}
         
    def validate_math3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] != "math3":
            return {"math3": tracker.slots.get("math3")}
        slot_value = slot_value[:-1].lower().split(" ")
        if "done" in slot_value:
            return {"math3": "done"}
        else:
            return {"math3": None}
        return {"math3": None}
#        if tracker.slots["requested_slot"] != "math3":
#            return {"math3": tracker.slots.get("math3")}
#        slot_value = slot_value.lower().split(" ")
#        if "didn't" in slot_value or "not" in slot_value or "no" in slot_value or "haven't" in slot_value:
#            return {"math3": "no"}
#        elif "did" in slot_value or "have" in slot_value or "yes" in slot_value:
#            return {"math3": "yes"}
#        return {"math3": None}
                
#    def validate_math4(
#        self,
#        slot_value: Any,
#        dispatcher: CollectingDispatcher,
#        tracker: Tracker,
#        domain: "DomainDict",
#    ) -> Dict[Text, Any]:
#        if tracker.slots["requested_slot"] != "math4":
#            return {"math4": tracker.slots.get("math4")}
#        slot_value = slot_value.lower().split(" ")
#        if "done" in slot_value:
#            return {"math4": "done"}
#        else:
#            return {"math4": None}
#        return {"math4": None}
            
    def validate_no2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        """Validate value."""
        if tracker.slots["requested_slot"] != "no2":
            return {"no2": tracker.slots.get("no2")}
        if "done" in slot_value.lower() or "help" in slot_value.lower():
            return {"no2": slot_value}
        return {"no2": None}
        
    def validate_no3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        """Validate value."""
        if tracker.slots["requested_slot"] != "no3":
            return {"no3": tracker.slots.get("no3")}
        if "done" in slot_value.lower() or "help" in slot_value.lower():
            return {"no3": slot_value}
        return {"no3": None}
                
    def validate_startmath(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        """Validate value."""
        if tracker.slots["requested_slot"] != "startmath":
            return {"startmath": tracker.slots.get("startmath")}
        if "done" in slot_value.lower() or "help" in slot_value.lower():
            return {"startmath": slot_value}
        return {"startmath": None}
        
    def validate_help(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        """Validate value."""
        if tracker.slots["requested_slot"] == "mathdone1":
            return {"help": "done"}
        return {"help": tracker.slots.get("help")}
        
    def validate_hs(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        """Validate value."""
        if tracker.slots["requested_slot"] == "hs":
            if not "." in slot_value:
                return {"hs": None}
        return {"hs": tracker.slots.get("hs")}
            
    def validate_passion(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        """Validate value."""
        if tracker.slots["requested_slot"] == "passion":
            if not "." in slot_value:
                return {"passion": None}
        return {"passion": tracker.slots.get("passion")}
            
    def validate_interest(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        """Validate value."""
        if tracker.slots["requested_slot"] == "interest":
            if not "." in slot_value:
                return {"interest": None}
        return {"interest": tracker.slots.get("interest")}
                
            
    def validate_future(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        """Validate value."""
        if tracker.slots["requested_slot"] == "future":
            if not "." in slot_value:
                return {"future": None}
        return {"future": tracker.slots.get("future")}
       
    def extract_music(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "sport1":
            return {"music": "done"}
        return {"music": tracker.slots.get("music")}
       
    def extract_sport1(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "music":
            return {"sport1": "done"}
        return {"sport1": tracker.slots.get("sport1")}
       
    def extract_music1(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "sport1" or tracker.slots["requested_slot"] == "extra":
            return {"music1": "done"}
        return {"music1": tracker.slots.get("music1")}
       
    def extract_music2(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "sport1" or tracker.slots["requested_slot"] == "extra":
            return {"music2": "done"}
        return {"music2": tracker.slots.get("music2")}
       
    def extract_music3(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "sport1" or tracker.slots["requested_slot"] == "extra":
            return {"music3": "done"}
        return {"music3": tracker.slots.get("music3")}
       
    def extract_extra(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "sport1" or tracker.slots["requested_slot"] == "music1":
            return {"extra": "done"}
        return {"extra": tracker.slots.get("extra")}
        
    def extract_help(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "mathdone1":
            return {"help": "done"}
        return {"help": tracker.slots.get("help")}
        
    def extract_math1(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "mathdone1":
            return {"math1": "done"}
        return {"math1": tracker.slots.get("math1")}
        
    def extract_math2(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "mathdone1":
            return {"math2": "done"}
        return {"math2": tracker.slots.get("math2")}
        
    def extract_math3(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "mathdone1":
            return {"math3": "done"}
        return {"math3": tracker.slots.get("math3")}
        
#    def extract_math4(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
#    ) -> Dict[Text, Any]:
#        if tracker.slots["requested_slot"] == "mathdone1":
#            return {"math4": "done"}
#        return {"math4": tracker.slots.get("math4")}
        
    def extract_no1(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "mathdone1":
            return {"no1": "done"}
        return {"no1": tracker.slots.get("no1")}
        
    def extract_no2(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
    ) -> Dict[Text, Any]:
        if tracker.slots["requested_slot"] == "mathdone1":
            return {"no2": "done"}
        return {"no2": tracker.slots.get("no2")}
        
#    def extract_no3(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict"
#    ) -> Dict[Text, Any]:
#        if tracker.slots["requested_slot"] == "mathdone1":
#            return {"no3": "done"}
#        return {"no3": tracker.slots.get("no3")}


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
