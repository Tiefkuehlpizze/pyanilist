import time

class Session:
    access_token = None
    expire_time = None
    pin = None
    refresh_token = None

    def expired(self):
        if self.expire_time is None:
            return True
        return time.time() > self.expire_time
    
    def dump(self):
        return {
            'access_token' : self.access_token,
            'expire_time' : self.expire_time,
            'pin' : self.pin,
            'refresh_token' : self.refresh_token,
        }

    def restore(self, data):
        self.access_token = data['access_token']
        self.expire_time = data['expire_time']
        self.pin = data['pin'] if 'pin' in data else None
        self.refresh_token = data['refresh_token'] if 'refresh_token' in data else None
