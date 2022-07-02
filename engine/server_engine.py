import logging
from engine import scheduler
from util.base_class import BaseClass


class ServerEngine(BaseClass):
    def __init__(self, sched, read_interval):
        self.mailbox_name = "server_engine"
        self.read_interval = read_interval * 1000
        super().__init__(sched)
        
    def _mail_handler(self, mail):
        if mail.mail_type == "start":
            mail = scheduler.Mail(self.mailbox_name, self.mailbox_name, "read_moisture", None)
            self.sched.send_mail(mail)
            
            pass
        
        elif mail.mail_type == "read_moisture":
            mail = scheduler.Mail(self.mailbox_name, self.mailbox_name, "read_moisture", None, self.read_interval)
            self.sched.send_mail(mail)
            logging.debug("sending read_moister request")
            
        
        else:
            raise ValueError

