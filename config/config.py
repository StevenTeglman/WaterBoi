from heapq import merge
import json
from engine import scheduler
from util.base_class import BaseClass
import os
from util.util import remove_empty
import logging


class Config(BaseClass):
    def __init__(self, sched):
        self.mailbox_name = "config"
        super().__init__(sched)


        
    def _mail_handler(self, mail):
        if mail.mail_type == "load_plants_req":
            plant_data = load_plants(mail.msg)
            mail = scheduler.Mail(mail.sender, self.mailbox_name, "load_plants_resp", plant_data)
            self.sched.send_mail(mail)
        
        elif mail.mail_type == "save_plants_req":
            pass
        
        else:
            raise ValueError

def load_plants(pins):
    current_directory = os.getcwd()
    plant_data_file = current_directory + "/config/plant_data.json"

    with open(plant_data_file, "r") as jsonFile:
        data = json.load(jsonFile)
    filtered_data = {}
    if data:
        for k,v in data.items():
            filtered_data[k] = v
    else:
        filtered_data = None
    logging.debug("[Plant Data Loaded]")
    return filtered_data


def save_plants(plant_dict):
    try:
        data_to_save = {}
        for p in plant_dict:
            new_plant = remove_empty(p)
            plant_to_save = {
                "pin": new_plant.get("pin"),
                "last_watered": new_plant.get("last_watered"),
                "moisture_lower_limit": new_plant.get("moisture_lower_limit"),
                "moisture": new_plant.get("moisture"),
                }
            data_to_save[plant_to_save["pin"]] = plant_to_save

        current_directory = os.getcwd()
        plant_data_file = current_directory + "/config/plant_data.json"
        with open(plant_data_file, "r") as jsonFile:
            old_data = json.load(jsonFile)
            updated_data = old_data | data_to_save

        with open(plant_data_file, "w") as jsonFile:
            json.dump(updated_data, jsonFile)

        return True

    except Exception as e:
        logging.error("Unable to save")
        logging.error(e)

