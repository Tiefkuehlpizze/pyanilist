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

# create a client object
c = grilllist.anilist.Client(id, secret)
# create a user object
u = grilllist.user.AnilistUser(c, 'some-name')
# load some data
u.loadBasic()
# print the data (ugly)
print(u.basic)
# or load more stuff:
u.loadAnimelist()
u.loadFavourites()
# spam your stdout with data:
print(u.getblob())
```

## Notice
Moar API (readonly) functions are about to come. I'm looking forward to add the functions I want to use first and then add additional calls. I might change my mind and create a full read-write library for Python 3. I'm coding in some languages, but Python is pretty new for me. So please excuse my C'ish style and probably wrong or missing usage of some properties.
You could motivate me, by showing your interest. I really would like to list here some projects using my library.
