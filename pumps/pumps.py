import datetime
import logging

from engine import scheduler
from util.base_class import BaseClass
import RPi.GPIO as GPIO
import time


class Pumps(BaseClass):
    def __init__(self, sched):
        self.mailbox_name = "pumps"
        super().__init__(sched)

    def _mail_handler(self, mail):
        if mail.mail_type == "water_plants_req":
            watered_plants = {}
            for plant in mail.msg.values:
                w_plant = water_plant(plant)
                watered_plants[w_plant.pin] = w_plant

            mail = scheduler.Mail(mail.sender, self.mailbox_name, "water_plants_resp", watered_plants)
            self.sched.send_mail(mail)

        else:
            raise ValueError


def water_plant(plant):
    pump_GPIO = plant.pump_GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pump_GPIO, GPIO.OUT)

    GPIO.output(pump_GPIO, True)
    logging.debug(f"[Watering Plant: {plant.pin} | Pump GPIO: {pump_GPIO}")
    logging.debug(f"[RELAY ON]")
    time.sleep(5)
    GPIO.output(pump_GPIO, False)
    logging.debug(f"[RELAY OFF]")

    plant.last_watered = datetime.datetime.now()
    return plant




