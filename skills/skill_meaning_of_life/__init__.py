
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

class MeaningSkill(MycroftSkill):

    def __init__(self):
        super(MeaningSkill, self).__init__(name="MeaningSkill")

    @intent_handler(IntentBuilder("").require("meaning").require("life"))
    def handle_meaning_of_life_intent(self, message):
        self.speak_dialog("meaning")

def create_skill():
    return MeaningSkill()
