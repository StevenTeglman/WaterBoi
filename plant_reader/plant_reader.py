from asyncore import read
from dataclasses import dataclass
import logging
import random
from engine import scheduler
from util.base_class import BaseClass


@dataclass
class PlantCollectionInfo:
    plants:dict
    

@dataclass
class PlantInfo:
    moisture:float
    

class PlantReader(BaseClass):
    def __init__(self, sched):
        self.mailbox_name = "plant_reader"
        super().__init__(sched)
        
    def _mail_handler(self, mail):
        if mail.mail_type == "read_plants_req":
            pc = read_plants()
            mail = scheduler.Mail(mail.sender, self.mailbox_name, "read_plants_resp", pc)
            self.sched.send_mail(mail)
            pass

def read_plants():
    # Do stuff
    plant_dict ={}
    plant_data = []
    for i in plant_data:
        m = random.randrange(0, 10)
        pi = PlantInfo(moisture=m)
        plant_dict[i] = pi
    
    pc = PlantCollectionInfo(plants=plant_dict)
        
    return pc