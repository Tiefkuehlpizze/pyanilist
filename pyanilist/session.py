import time

class Session:
    access_token = None
    expire_time = None
    pin = None
    refresh_token = None

    def expired(self):
        if self.expire_time == None:
            return true
        return time.time() > self.expire_time

