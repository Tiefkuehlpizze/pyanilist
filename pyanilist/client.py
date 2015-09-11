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
        self.login = False

    def has_login(self, noexcept=False):
        if noexcept or self.login:
            return self.login
        raise exception.NotAuthenticatedError("User not authentificated")

    def get_accesstoken(self):
        if self.session.access_token is not None and not self.session.expired():
            return self.session.access_token
        
        url = self.PREFIX + 'auth/access_token'
        
        payload = {
            'grant_type' : 'client_credentials',
            'client_id' : self.id,
            'client_secret': self.secret,
        }
        if self.session.refresh_token:
            payload['grant_type'] = 'refresh_token'
            payload['refresh_token'] = self.session.refresh_token
        elif self.session.pin:
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
        self.has_login = self.session.refresh_token is not None

        return self.session.access_token

    def get_pin_uri(self):
        return self.PREFIX + 'auth/authorize?grant_type=authorization_pin&client_id=%s&response_type=pin&redirect_uri=%s' % (self.id, self.REDIRECTURI)

    def set_pin(self, pin):
        if isinstance(pin, str):
            raise TypeError("pin is not a string")
        self.session.pin = pin
        self.login = True
        self.session.expire_time = 0

    def check_error(self, response):
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
        if response.content:
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
            'Authorization' : 'Bearer ' + self.get_accesstoken(),
        }
        url = self.PREFIX + path
        params = { } if 'data' not in query else query['data']
        response = self.check_error(method(url, params=params, headers=headers))
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

    def get_me(self):
        self.has_login()
        return self.get('user')

    def set_session(self, obj):
        if not isinstance(obj, session.Session):
            raise TypeError('given parameter has an invalid type, was {!r}'.format(obj.__class__.__name__))
        self.session = obj
        self.login = self.session.refresh_token is not None
    
    def get_session(self):
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
        c.set_session(s)
        c.login = s.refresh_token is not None
        return c

    @staticmethod
    def canWake(filename='state.txt'):
        return os.path.isfile(filename)
        
