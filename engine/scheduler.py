#!/usr/bin/env python
"""
WaterBoi, By Steven Teglman (Scheduler created by Kristian Stobbe)
"""
import logging
import sys
import time
from threading import Event

def InterruptableEvent():
    e = Event()

    def patched_wait():
        while not e.is_set():
            e._wait(3)

    e._wait = e.wait
    e.wait = patched_wait
    return e

class Mail:
    def __init__(self, recipient, sender, mail_type, msg, delay=0):
        self.recipient = recipient
        self.sender = sender
        self.mail_type = mail_type
        self.msg = msg
        self.time_to_send = int(round(time.time() * 1000) + delay)


class Mailbox:
    def __init__(self, mail_handler):
        self.mail_handler = mail_handler
        self.queue = []
        self.postponed = []

    def push_postpone(self, mail):
        self.postponed.append(mail)

    def pop_postpone(self):
        if len(self.postponed):
            return self.postponed.pop(0)
        else:
            return None


class Scheduler:
    def __init__(self):
        self.mailboxes = {}
        self.timed_mails = []
        self.mail_event = Event()
        self.is_running = True

    def add_mailbox(self, name, mail_handler):
        # Mailbox names must be unique.
        if name not in self.mailboxes:
            self.mailboxes[name] = Mailbox(mail_handler)
            logging.debug("%s mailbox added" % name)
            return self.mailboxes[name]
        else:
            raise ValueError

    def send_mail(self, mail):
        # Mails must be of type mail and to an existing mailbox
        if isinstance(mail, Mail) and mail.recipient in self.mailboxes:
            # Mails with no delays are delivered to mailboxes directly
            if mail.time_to_send <= int(round(time.time() * 1000)):
                self.mailboxes[mail.recipient].queue.append(mail)
                logging.debug("Mail delivered to %s, from %s, type %s", mail.recipient, mail.sender, mail.mail_type)
            else:
                # Delayed mails are stored on a sorted list until they are scheduled for delivery
                self.timed_mails.append(mail)
                self.timed_mails.sort(key=lambda x: x.time_to_send, reverse=False)
                logging.debug("Mail delay %ds to %s, from %s, type %s", ((mail.time_to_send / 1000) - time.time()), mail.recipient, mail.sender, mail.mail_type)

            # Wake up scheduler to ensure handling of mails or reconfiguration of sleep timer
            self.mail_event.set()
        else:
            raise ValueError

    def cancel_mail(self, mail):
        # Mails must be of type mail and to an existing mailbox
        if isinstance(mail, Mail) and mail.recipient in self.mailboxes:
            if mail in self.mailboxes[mail.recipient].queue:
                self.mailboxes[mail.recipient].queue.remove(mail)
                logging.debug("Delivered mail cancelled to %s, from %s, type %s", mail.recipient, mail.sender, mail.mail_type)
            elif mail in self.mailboxes[mail.recipient].postponed:
                self.mailboxes[mail.recipient].postponed.remove(mail)
                logging.debug("Postponed mail cancelled to %s, from %s, type %s", mail.recipient, mail.sender, mail.mail_type)
            elif mail in self.timed_mails:
                self.timed_mails.remove(mail)
                self.timed_mails.sort(key=lambda x: x.time_to_send, reverse=False)
                logging.debug("Delayed mail cancelled to %s, from %s, type %s", mail.recipient, mail.sender, mail.mail_type)
            else:
                logging.debug("No mail to cancel to %s, from %s, type %s", mail.recipient, mail.sender, mail.mail_type)
        else:
            raise ValueError

    def run(self):
        try:
            while self.is_running:
                # Variable n is used to determine when sleep is allowed.
                n = 0

                # First deliver all expired waiting mails
                while len(self.timed_mails) and self.timed_mails[0].time_to_send <= int(round(time.time() * 1000)):
                    mail = self.timed_mails.pop(0)
                    if mail.recipient in self.mailboxes:
                        self.mailboxes[mail.recipient].queue.append(mail)
                        logging.debug("Timed mail delivered to %s, from %s, type %s", mail.recipient, mail.sender,
                                    mail.mail_type)
                    else:
                        logging.error("Mailbox disappeared before mail delivery. Mail discarded.")

                # Then handle mails from all mail boxes - round robin
                for box in self.mailboxes.values():
                    if len(box.queue):
                        n += 1
                        box.mail_handler(box.queue.pop(0))

                # Finally, check is sleep is allowed, i.e. all mailboxes are empty
                if n == 0:
                    self.mail_event.clear()
                    if len(self.timed_mails):
                        if self.timed_mails[0].time_to_send > int(round(time.time() * 1000)):
                            timeout = (self.timed_mails[0].time_to_send / 1000) - time.time()
                            logging.debug("Sleep for %ds" % timeout)
                            self.mail_event.wait(timeout)
                    else:
                        logging.debug("Sleep until event")
                        self.mail_event.wait()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.is_running = False
        self.mail_event.set()
        sys.exit()
