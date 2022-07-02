class BaseClass():
    def __init__(self, sched):
        self.sched = sched
        self.sched.add_mailbox(self.mailbox_name, self._mail_handler)


    def _mail_handler(self, mail):
        pass