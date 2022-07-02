import argparse
from http import server
from engine import scheduler
from engine.server_engine import ServerEngine
import logging


__author__ = "Steven Jack Teglman"
__version__ = "0.0.1"
__email__ = "steventeglman@gmail.com"

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level='DEBUG')
parser = argparse.ArgumentParser(description='Test tool for long running bare metal modem tests.')
parser.add_argument("-r", "--read_interval", required=True, type=int, help="How often the moister will be read, in seconds.")

args = parser.parse_args()
def main():
    if args.read_interval:
        read_interval = args.read_interval
    else:
        logging.error("Missing argument: -read_interval")
        raise ValueError
    
    sched = scheduler.Scheduler()
    server_engine = ServerEngine(sched, read_interval=read_interval)
    
    sched.send_mail(scheduler.Mail(server_engine.mailbox_name, server_engine.mailbox_name, "start", None))
    
    try:
        sched.run()
    except:
        sched.stop()

if __name__ == "__main__":
    main()