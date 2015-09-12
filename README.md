# pyanilist

A little Python library to request stuff from the Anilist.co API. Don't forget to get your very own API Developer Client ID and Secret at [http://anilist.co/]


## Installation
### Requirements
* Python 3
* requests

## Usage
```
import pyanilist

id = 'some-id'
secret = '00wow00such00secret00'
pin = 'somepin'

# create a client object
c = pyanilist.client.Client(id, secret)
# give our client object a PIN to authentificate
c.set_pin(pin)
# get some data about the authentificated user (no parameter means the authentifcated user)
basicdata = pyanilist.get_basic(c)
# get some data about the user "foo"
someusersdata = pyanilist.user.get_basic(c, "foo")
# print the data (ugly)
print(basicdata)
# or get more stuff:
animelist = pyanilist.user.get_animelist(c)
favourites = pyanilist.user.get_favourites(c)
# get foo's animelist
fooslist = pyanilist.user.get_animelist(c, "foo")
# search for an anime
result = pyanilist.anime.browse(c, year=2014, _type="Tv", genres="Action,Comedy")
```
To go the object oriented way, you can do the same by using this code
```
ani = pyanilist.anilist.Anilist(id, secret)
ani.set_pin(pin)
# get basic data about the authentificated user
basicdata = ani.user.get_basic()
# get basic data about user "foo"
someusersdata = ani.user.get_basic("foo")
# get animelist and favourites of the authentifcated user
animelist = ani.user.get_animelist()
favourites = ani.user.get_favourites()
# get foo's animelist
fooslist = ani.user.get_animelist("foo")
# search for an anime
result  = ani.anime.browse(year=2014, _type="tv", genres="Action,Comedy")
```

When you are finished, you have to save the token to avoid asking the user to pass another pin to your app!
```
# store a dictionary in mysessiondata to store it persistently somewhere
mysessiondata = c.get_session().dump()

# To restore a session you can use multiple ways (assuming the used vars containing the right data)
c = pyanlist.client.Client(id, secret)
c.restore_session(access_token, expire_time, pin, refresh_token)
# or 
s = pyanilist.session.Session()
s.restore(mysessiondata)
c.set_ession(s)
```
Just remember to save this data everytime, if you have an authentificated user session!


# Limitations
This might be still in development. I'm writing a quick Code'n'Fix style, so the library can break everytime.
I'm not sure, if I could tell this is stable. I just implemented the API by it's documententation. If you are using this library and something does not work, please tell me. I'm sure I can fix it in a short time, if you provide enough infos.

## Notice
I was writing C-ish languages for a long time. I got some feedback to do things more pythonic but I think there are still things that could be implemented or named better. Just tell me, if you notice something.
I think, this thing is finished for now. As long as there are no bug reports or something, I'm gonna work on other projects.
I would be happy if you show your interest and I really would like to list here some projects using this library.
