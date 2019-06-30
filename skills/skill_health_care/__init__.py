from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_file_handler
from mycroft.util.log import LOG
import json
import os


class HealthCareSkill(MycroftSkill):

    def __init__(self):
        super(HealthCareSkill, self).__init__(name="HealthCareSkill")
        self.path = "skills/skill_health_care/data.txt"
        self.first_name = ""
        self.last_name = ""

    @intent_file_handler("add.patient.intent")
    def add_patient_intent(self, message):
        data = message.data
        if "name" in data:
            if self._convert_name(data["name"]):
                if self._add_patient(self.first_name, self.last_name, []):
                    return self.speak_dialog("patient.added", data)
                else:
                    return self.speak_dialog("patient.allready.exists")
            else:
                return self.speak_dialog("invalid.name")
        else:
            return self.speak_dialog("debug")
    
    @intent_file_handler("remove.patient.intent")
    def remove_patient_intent(self, message):
        data = message.data
        if "name" in data:
            if self._convert_name(data["name"]):
                if self._remove_patient(self.first_name, self.last_name):
                    return self.speak_dialog("patient.removed", data)
                else:
                    return self.speak_dialog("patient.not.found", data)
            else:
                return self.speak_dialog("invalid.name")
        else:
            return self.speak_dialog("debug")

    @intent_file_handler("add.heartrate.intent")
    def add_heartrate_intent(self, message):
        data = message.data
        if "name" in data and "heartrate" in data:
            if self._convert_name(data["name"]):
                if self._add_heartrate(self.first_name, self.last_name, data["heartrate"]):
                    return self.speak_dialog("heartrate.added", data)
                else:
                    return self.speak_dialog("patient.not.found", data)
            else:
                return self.speak_dialog("invalid.name")
        else:
            return self.speak_dialog("debug")
    
    @intent_file_handler("average.heartrate.intent")
    def average_heartrate_intent(self, message):
        data = message.data
        if "name" in data:
            if self._convert_name(data["name"]):
                calc_heartrate = self._average_heartrate(self.first_name, self.last_name)
                if calc_heartrate > 0:
                    data["average"] = str(calc_heartrate)
                    return self.speak_dialog("heartrate.average", data)
                elif calc_heartrate == 0:
                    return self.speak_dialog("no.heartrates.available")
                else:
                    return self.speak_dialog("patient.not.found", data)
            else:
                return self.speak_dialog("invalid.name")
        else:
            return self.speak_dialog("debug")

    def _add_patient(self, name, lastname, heartrate):
        if not os.path.exists(self.path):
            with open(self.path, 'w') as fp:
                data = {"patients": {}}
                json.dump(data, fp, indent=4)

        with open(self.path, 'r') as fp:
            data = json.load(fp)
            for patient in data["patients"].keys():
                cur_patient = data["patients"][patient]
                if cur_patient["name"] == name and cur_patient["lastname"] == lastname:
                    return False

        with open(self.path, 'w') as fp:
            key_str = "{}{}".format(name, lastname)
            new_patient = {
                "name": name,
                "lastname": lastname,
                "heartrate": heartrate}
            data["patients"][key_str] = new_patient
            json.dump(data, fp, indent=4)
            return True

    def _remove_patient(self, name, lastname):
        patient = self._find_patient(name, lastname)
        if patient is None:
            # patient not found
            return False

        with open(self.path, 'r') as fp:
            data = json.load(fp)

        with open(self.path, 'w') as fp:
            key_str = "{}{}".format(name, lastname)
            data["patients"].pop(key_str)
            json.dump(data, fp, indent=4)
            return True

    def _find_patient(self, name, lastname):
        if not os.path.exists(self.path):
            with open(self.path, 'w') as fp:
                data = {"patients": {}}
                json.dump(data, fp, indent=4)
                return None # data file does not exist
    
        with open(self.path, 'r') as fp:
            data = json.load(fp)
            if len(data) == 0:
                return None # json data is empty
            search_key = "{}{}".format(name, lastname)
            
            if search_key in data["patients"]:
                return data["patients"][search_key]
            return None # patient is not in data


    def _average_heartrate(self, name, lastname):
        patient = self._find_patient(name, lastname)
        if patient is None:
            return -1 # patient not found
    
        heartrate_list = patient["heartrate"]
    
        if len(heartrate_list) == 0:
            return 0 # no values are present
    
        avr_heartrate = 0
        for val in heartrate_list:
            avr_heartrate += val
    
        return avr_heartrate / len(heartrate_list)
    
    
    def _add_heartrate(self, name, lastname, heartrate):
        patient = self._find_patient(name, lastname)
        if patient is None:
            return False # patient not found
        heartrate = int(heartrate)
        patient["heartrate"].append(heartrate)
        key_str = "{}{}".format(name, lastname)
    
        with open(self.path, 'r') as fp:
            data = json.load(fp)
    
        with open(self.path, 'w') as fp:
            data["patients"][key_str] = patient
            json.dump(data, fp, indent=4)
            return True 

    def _convert_name(self, name):
        name.lower()
        names = name.split(' ', 1)
        if len(names) <= 1:
            return False
        self.first_name = names[0]
        self.last_name = names[1]
        return True

def create_skill():
    return HealthCareSkill()
