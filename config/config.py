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
    logging.error("We got here1")
    plant_data = current_directory + "/config/plant_data.json"
    logging.error(plant_data)
    
    logging.error("We got here2")
    with open(plant_data, "r") as jsonFile:
        data = json.load(jsonFile)
    filtered_data = {}
    logging.error("We got here3")
    if data:
        for k,v in data.items():
            filtered_data[k] = v
    else:
        filtered_data = None
    logging.error("We got here4")
    return filtered_data

def save_plants(plant_dict):
    data_to_save = {}
    for p in plant_dict:
        new_plant = remove_empty(p)
        new_plant = {
            "pin":new_plant["pin"],
            "last_watered":new_plant["last_watered"],
            "moisture_lower_limit":new_plant["moisture_lower_limit"],
            "moisture":new_plant["moisture"],
            }
        data_to_save[new_plant["pin"]] = new_plant
        
    current_directory = os.getcwd()
    plant_data = current_directory + "/config/plant_data.json"
    updated_data = {}
    with open(plant_data, "r") as jsonFile:
        old_data = json.load(jsonFile)
        updated_data = old_data | data_to_save
    
    with open(plant_data, "w") as jsonFile:
        json.dump(updated_data, jsonFile)

