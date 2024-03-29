import argparse
from http import server
from config.config import Config
from engine import scheduler
from engine.server_engine import ServerEngine
import logging
import json

from plant_reader.plant_reader import PlantReader


__author__ = "Steven Jack Teglman"
__version__ = "0.0.1"
__email__ = "steventeglman@gmail.com"

from pumps.pumps import Pumps

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level='DEBUG')
parser = argparse.ArgumentParser(description='Test tool for long running bare metal modem tests.')
parser.add_argument("-r", "--read_interval", required=True, type=int, help="How often the moister will be read, in seconds.")
parser.add_argument("-p", "--pins", required=True, type=str, help="The pins that will be read, all one string. '123'")
parser.add_argument("-c", "--calibrations", required=False, type=str, default="moisture_calibration.json", help="Moisture Sensor Calibration file")

args = parser.parse_args()
def main():
    if args.read_interval:
        read_interval = args.read_interval
    else:
        logging.error("Missing argument: --read_interval")
        raise ValueError
    
    if args.pins:
        pins = args.pins
    else:
        logging.error("Missing argument: --pins")
        raise ValueError
    
    try:
        with open(args.calibrations, 'r') as fp:
            calibrations = json.load(fp)    
    except:
        logging.error("Something is fucked with the calibration file")
        raise ValueError
    
    sched = scheduler.Scheduler()
    PlantReader(sched)
    Config(sched)
    Pumps(sched)
    server_engine = ServerEngine(sched, read_interval=read_interval, pins=pins, calibrations=calibrations)
    sched.send_mail(scheduler.Mail(server_engine.mailbox_name, "main.py", "startup_sequence", None))
    

    
    try:
        sched.run()
    except:
        sched.stop()

if __name__ == "__main__":
    main()
