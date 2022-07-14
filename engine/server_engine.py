from dataclasses import dataclass
from datetime import datetime
import logging
import os
from engine import scheduler
from util.base_class import BaseClass


@dataclass
class Plant:
    pin: str
    max_value: int
    min_value: int
    last_watered: datetime = None
    moisture_lower_limit: int = None
    moisture: float = None
    pump_GPIO: int = None
    
    
class ServerEngine(BaseClass):
    def __init__(self, sched, read_interval, pins, calibrations):
        self.mailbox_name = "server_engine"
        self.read_interval = read_interval * 1000
        super().__init__(sched)
        
        # Store calibrations
        self.calibrations = calibrations
        
        # Instantiate plants
        self.plants = {}
        pins = list(pins)
        for p in pins:
            plant = Plant(
                pin=p,
                max_value=self.calibrations[p]["max_value"],
                min_value=self.calibrations[p]["min_value"])
            self.plants[p] = plant

    def _mail_handler(self, mail):
        if mail.mail_type == "startup_sequence":
            mail = scheduler.Mail("config", self.mailbox_name, "load_plants_req", list(self.plants.keys()))
            self.sched.send_mail(mail)
        
        elif mail.mail_type == "load_plants_resp":
            saved_plants = mail.msg
            if saved_plants:
                for k, v in saved_plants.items():
                    self.plants[k].last_watered = v.get("last_watered")
                    self.plants[k].moisture_lower_limit = v.get("moisture_lower_limit")
                    self.plants[k].moisture = v.get("moisture")
            
            mail = scheduler.Mail(self.mailbox_name, self.mailbox_name, "read_moisture", None)
            self.sched.send_mail(mail)
        
        elif mail.mail_type == "read_moisture":
            self_mail = scheduler.Mail(self.mailbox_name, self.mailbox_name, "read_moisture", None, self.read_interval)
            self.sched.send_mail(self_mail)
            
            moist_mail = scheduler.Mail("plant_reader", self.mailbox_name, "read_plants_req", self.plants)
            self.sched.send_mail(moist_mail)
            
        elif mail.mail_type == "read_plants_resp":
            logging.error("We got to read_plants_resp")
            self.plants = mail.msg

            mail = scheduler.Mail("config", self.mailbox_name, "save_plants_req", self.plants)
            self.sched.send_mail(mail)

            self.handle_readings()

        elif mail.mail_type == "water_plants.resp":
            for k, v in mail.msg.items():
                self.plants[k] = v

        else:
            raise ValueError

    def handle_readings(self):
        needs_watering = {}

        # os.system('cls||clear')
        print(" -----------------")
        print("|  PLANT READOUT  |")
        print(" -----------------")
        for plant in self.plants.values():
            print(f"[Plant No.]: {plant.pin} | [Plant Moistness]: {plant.moisture}")
            if plant.moisture < plant.moisture_lower_limit:
                needs_watering[plant.pin] = plant
        print(" -----------------")
        mail = scheduler.Mail("pumps", self.mailbox_name, "water_plants_req", needs_watering)
        self.sched.send_mail(mail)


