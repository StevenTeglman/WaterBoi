from dataclasses import dataclass
from datetime import datetime
import logging
import os
from engine import scheduler
from util.base_class import BaseClass
from datetime import datetime

@dataclass
class Plant:
    pin:int
    max_value:int
    min_value:int
    last_watered:datetime = None
    moisture:float = None
    
    
class ServerEngine(BaseClass):
    def __init__(self, sched, read_interval, pins, calibrations):
        self.mailbox_name = "server_engine"
        self.read_interval = read_interval * 1000
        
        # Store calibrations
        self.calibrations = calibrations
        
        # Instantiate plants
        self.plants = {}
        pins = list(pins)
        for p in pins:
            plant = Plant(
                pin=int(p),
                max_value=self.calibrations[p]["max_value"],
                min_value=self.calibrations[p]["min_value"])
            self.plants[p] = plant
        
        super().__init__(sched)


    def _mail_handler(self, mail):
        if mail.mail_type == "start":
            mail = scheduler.Mail(self.mailbox_name, self.mailbox_name, "read_moisture", None)
            self.sched.send_mail(mail)
        
        elif mail.mail_type == "read_moisture":
            self_mail = scheduler.Mail(self.mailbox_name, self.mailbox_name, "read_moisture", None, self.read_interval)
            self.sched.send_mail(self_mail)
            
            moist_mail = scheduler.Mail("plant_reader", self.mailbox_name, "read_plants_req", self.plants)
            self.sched.send_mail(moist_mail)
            
        elif mail.mail_type == "read_plants_resp":
            self.plants = mail.msg
            os.system('cls||clear')
            print(f"[Last Read]: {datetime.today().strftime('%d-%m-%Y--%H.%M.%S')}")
            print(" -----------------")
            print("|  PLANT READOUT  |")
            print(" -----------------")
            for plant in self.plants.values():
                print(f"[Plant No.]: {plant.pin} | [Plant Moistness]: {plant.moisture}")
            print(" -----------------")
            
        
        else:
            raise ValueError

