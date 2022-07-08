from asyncore import read
from dataclasses import dataclass
from datetime import datetime
from locale import normalize
import logging
import random
from engine import scheduler
from util.base_class import BaseClass
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
    

class PlantReader(BaseClass):
    def __init__(self, sched):
        self.mailbox_name = "plant_reader"
        
        # create the spi bus
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        self.cs = digitalio.DigitalInOut(board.D5)

        # create the mcp object
        self.mcp = MCP.MCP3008(self.spi, self.cs)
        super().__init__(sched)


        
    def _mail_handler(self, mail):
        if mail.mail_type == "read_plants_req":
            plants = self.read_plants(plants=mail.msg)
            mail = scheduler.Mail(mail.sender, self.mailbox_name, "read_plants_resp", plants)
            self.sched.send_mail(mail)

        else:
            raise ValueError

    def choose_pin(self, p):
        
        if p == 0:
            return AnalogIn(self.mcp, MCP.P0)
        elif p == 1:
            return AnalogIn(self.mcp, MCP.P1)
        elif p == 2:
            return AnalogIn(self.mcp, MCP.P2)
        elif p == 3:
            return AnalogIn(self.mcp, MCP.P3)
        elif p == 4:
            return AnalogIn(self.mcp, MCP.P4)
        elif p == 5:
            return AnalogIn(self.mcp, MCP.P5)
        elif p == 6:
            return AnalogIn(self.mcp, MCP.P6)
        elif p == 7:
            return AnalogIn(self.mcp, MCP.P7)
        elif p == 8:
            return AnalogIn(self.mcp, MCP.P8)
        else:
            raise ValueError

    def read_plants(self, plants):
        new_plants = {}
        print(plants)
        for plant in plants.values():
            pin = plant.pin
            chan = self.choose_pin(pin)
            
            moistness = chan.value
            normalized_moistness = (moistness - plant.min_value) / (plant.max_value - plant.min_value)
            if normalized_moistness > 1 :
                normalized_moistness == 1
            if normalized_moistness < 0 :
                normalized_moistness == 0
            moist_percentage = (1 - normalized_moistness) * 100
            plant.moisture = moist_percentage
            new_plants[pin] = plant
        
        return new_plants
            
            
        
