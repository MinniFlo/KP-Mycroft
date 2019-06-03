
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.log import LOG


class PrimeNumberSkill(MycroftSkill):

    def __init__(self):
        super(PrimeNumberSkill, self).__init__(name="PrimeNumberSkill")

    @intent_file_handler("tell.number.intent")
    def handle_hello_world_intent(self, message):
        if 'number' in message.data:
            self.speak_dialog("jojo.dat")

            number = int(message.data["number"])
            if number % 2 == 0:
                return self.speak_dialog("not.even.odd", message.data)
            else:
                if self._is_prim(number):
                    return self.speak_dialog("is.a.prime", message.data)
                else:
                    return self.speak_dialog("not.a.prime", message.data)
        else:
            return self.speak_dialog("nene")

    def _is_prim(self, number):
        if number <= 1:
            return False
        else:
            for i in range(2, number):
                if number % i == 0:
                    return False
            return True


def create_skill():
    return PrimeNumberSkill()
