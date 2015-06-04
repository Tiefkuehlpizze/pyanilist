import json
import requests
import time
from . import user

class Client:
    PREFIX = 'http://anilist.co/api/'
    UA = 'py/grilllist'

    def __init__(self, id, secret):
        self.id = id
        self.secret = secret
        self.access_token = None
        self.expire_time = None

    def expired(self):
        if self.expire_time == None:
            return true
        return time.time() > self.expire_time

    def getaccesstoken(self):
        if self.access_token != None and not self.expired():
            return self.access_token

        url = self.PREFIX + 'auth/access_token'
        payload = {
            'grant_type' : 'client_credentials',
            'client_id' : self.id,
            'client_secret': self.secret,
        }
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'User-Agent' : self.UA,
        }

        start = time.time()
        response = requests.post(url, data=payload, headers=headers)
        res = response.json()
        
        self.access_token = res['access_token']
        self.expire_time = start + res['expires_in']

        return self.access_token

    def get(self, path, **query):
        headers = {
            'access_token' : self.getaccesstoken(),
            'User-Agent' : self.UA,
        }

        query['access_token'] = self.getaccesstoken()
        url = self.PREFIX + path
        
        response = requests.get(url, params=query, headers=headers)
        return response.json()

    def sleep(self, filename='state.txt'):
        data = {
            'id' : self.id,
            'secret' : self.secret,
            'access_token' : self.access_token,
            'expire_time' : self.expire_time,
        }
        with open(filename, 'w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def wake(filename='state.txt'):
        with open(filename, 'r') as f:
            data = json.loads(f.read())
        c = Client(data['id'], data['secret'])
        c.access_token = data['access_token']
        c.expire_time = data['expire_time']
        return c

