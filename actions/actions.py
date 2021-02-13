# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
enti_dict = {}


class ActionAskIllness(Action):
    def name(self) -> Text:
        return "action_ask_illness"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        illness = tracker.get_slot('illness')
        illness_duplication = list(set(illness))
        enti_dict['illness'] = illness_duplication
        description = '、'.join(illness_duplication)
        dispatcher.utter_message(text=f"除了{description}外，请问还有不舒服的地方吗？")

        return [SlotSet("illness",illness)]

class ActionQueryFinish(Action):
    def name(self) -> Text:
        return "action_query_finish"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        illness = tracker.get_slot('illness')
        illness_duplication = list(set(illness))
        if len(enti_dict['illness']) < 1:
            enti_dict['illness'] = illness_duplication
        else:
            tmp_illness = enti_dict['illness']
            tmp_illness.extend(illness_duplication)
            enti_dict['illness'] = list(set(tmp_illness))
        duration = tracker.get_slot('duration')
        enti_dict['duration'] = duration
        dispatcher.utter_message(text=f"好的，信息已收集结束。")
        dispatcher.utter_message(text=f"{enti_dict}")
        return [enti_dict]