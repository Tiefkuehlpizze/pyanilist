# pyanilist

A little Python library to request stuff from the Anilist.co API. Don't forget to get your very own API Developer Client ID and Secret at [http://anilist.co/]


## Installation
### Requirements
* Python 3
* requests

## Usage
```
import grilllist

id = 'some-id'
secret = '00wow00such00secret00'
pin = 'somepin'

# create a client object
c = grilllist.anilist.Client(id, secret)
# give our client object a PIN to authentificate
c.setPin(pin)
# create a user object
u = grilllist.user.AnilistUser(c, 'some-name')
# load some data
basicdata = u.getBasic()
# print the data (ugly)
print(basicdata)
# or load more stuff:
animelist = u.getAnimelist()
favourites = u.loadFavourites()
```
# Limitations
This is still in development. I'm writing a quick Code'n'Fix style, so the library can break everytime.
Also the mechanism to handle user-sessions with a PIN is really buggy and not well thought out. Currently this library is handling the storage of the session data and can save it to a file (sleep and wake functions). This might work, but feels wrong. So I probably move this to a mechanism that moves the responsibility to the application that uses this library.

## Notice
Moar API functions are about to come. I'm looking forward to add the functions I want to use first and then add additional calls. I might change my mind and create a full read-write library for Python 3. I'm coding in some languages, but Python is pretty new for me. So please excuse my C'ish style and probably wrong or missing usage of some properties.
You could motivate me, by showing your interest. I really would like to list here some projects using my library.
