import json
import os
import requests
import time
from . import exception, session

class Client:
    PREFIX = 'https://anilist.co/api/'
    UA = 'py/grilllist'
    REDIRECTURI = 'https://github.com/Tiefkuehlpizze/grilllist' # Placeholder or something /o\

    def __init__(self, id, secret, pin=None):
        self.id = id
        self.secret = secret
        self.session = session.Session()
        self.haslogin = False

    def hasLogin(self, noexcept=False):
        if noexcept or self.haslogin:
            return self.haslogin
        raise exception.NotAuthenticatedError("User not authentificated")

    def getaccesstoken(self):
        if self.session.access_token != None and not self.session.expired():
            return self.session.access_token
        
        url = self.PREFIX + 'auth/access_token'
        
        payload = {
            'grant_type' : 'client_credentials',
            'client_id' : self.id,
            'client_secret': self.secret,
        }
        if type(self.session.refresh_token) is str:
            payload['grant_type'] = 'refresh_token'
            payload['refresh_token'] = self.session.refresh_token
        elif type(self.session.pin) is str:
            payload['grant_type'] = 'authorization_pin'
            payload['code'] = self.session.pin

        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'User-Agent' : self.UA,
        }
        start = time.time()
        response = requests.post(url, data=payload, headers=headers)
        res = response.json()
        if 'error' in res:
            raise exception.ApiError(res['error'], res['error_description'])
        self.session.access_token = res['access_token']
        self.session.expire_time = start + res['expires_in']
        self.session.refresh_token = res['refresh_token'] if 'refresh_token' in res else None
        self.haslogin = self.session.refresh_token is not None

        return self.session.access_token

    def getPinUri(self):
        return self.PREFIX + 'auth/authorize?grant_type=authorization_pin&client_id=%s&response_type=pin&redirect_uri=%s' % (self.id, self.REDIRECTURI)

    def setPin(self, pin):
        if type(pin) is not str:
            raise TypeError("pin is not a string")
        self.session.pin = pin
        self.haslogin = True
        self.session.expire_time = 0

    def checkerror(self, response):
        if response.status_code >= 400:
            error = ""
            try:
                json = response.json()
                if response.status_code == 401:
                    raise exception.NotAuthenticatedError(json['error'])
                error = json['error'] if isinstance(json['error'], str) else json['error']['message']
            except ValueError:
                pass
            raise exception.ApiError("API returned non positive statuscode: " + error, response.status_code)
        if len(response.content) > 0:
            try:
                int(response.content)
                return response
            except ValueError:
                pass
            try:
                cont = response.json()
                if 'error' in cont:
                    raise self.exceptions[cont['error']](cont['error'], cont['error_description'])
            except ValueError:
                # Anilist can reply with just "followed" *duh*
                pass
        return response
                

    def send_request(self, method, path, **query):
        if method is not requests.get and self.pin is None:
            raise NotAuthenticatedError("Action cannot be done until authentificated")
        headers = {
            'User-Agent' : self.UA,
            'Authorization' : 'Bearer ' + self.getaccesstoken(),
        }
        url = self.PREFIX + path
        params = { } if 'data' not in query else query['data']
        response = self.checkerror(method(url, params=params, headers=headers))
        try:
            return response.json()
        except ValueError:
            return None

    def get(self, path, **query):
        return self.send_request(requests.get, path, **query)
    
    def put(self, path, **query):
        return self.send_request(requests.put, path, **query)

    def post(self, path, **query):
        return self.send_request(requests.post, path, **query)

    def delete(self, path, **query):
        return self.send_request(requests.delete, path, **query)

    def getme(self):
        self.hasLogin()
        return self.get('user')

    def setSession(self, obj):
        if not isinstance(obj, session.Session):
            raise TypeError('given parameter has an invalid type, was {!r}'.format(obj.__class__.__name__))
        self.session = obj
        self.haslogin = self.session.refresh_token is not None
    
    def getSession(self):
        return self.session

    def sleep(self, filename='state.txt'):
        data = {
            'id' : self.id,
            'secret' : self.secret,
            'access_token' : self.session.access_token,
            'expire_time' : self.session.expire_time,
            'refresh_token' : self.session.refresh_token,
            'pin' : self.session.pin,
        }
        with open(filename, 'w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def wake(filename='state.txt'):
        with open(filename, 'r') as f:
            data = json.loads(f.read())
        c = Client(data['id'], data['secret'])
        s = session.Session()
        s.access_token = data['access_token']
        s.expire_time = data['expire_time']
        s.refresh_token = data['refresh_token']
        s.pin = data['pin']
        c.setSession(s)
        c.haslogin = s.refresh_token is not None
        return c

    @staticmethod
    def canWake(filename='state.txt'):
        return os.path.isfile(filename)
        
