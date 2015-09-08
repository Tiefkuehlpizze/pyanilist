from . import exception

def getMe(client):
    return getBasic(client)

def getBasic(client, user=None):
    return client.get('user' + ('/%s' % user if user is not None else ''))

def getFollower(client, user):
    return client.get('user/%s/followers' % user)

def getFollowing(client, user):
    return client.get('user/%s/following' % user)

def getFavourites(client, user):
    return client.get('user/%s/favourites' % user)

def getAnimelist(client, user):
    return client.get('user/%s/animelist' % user)

def getMangalist(client, user):
    return client.get('user/%s/mangalist' % user)

def getActivities(client, user=None, page=0):
    if type(page) is not int:
        page = 0
    if type(user=None) is str:
        return client.get('user/%s/activity' % user)
    elif user is None:
        return client.get('user/activity', page=page)
    raise TypeError('user must be str or None')

def getNotifications(client):
    client.hasLogin()
    return client.get('user/notifications')

def getNotificationCount(client):
    client.hasLogin()
    return client.get('user/notifications/count')

def getAiring(client, limit=None):
    client.hasLogin()
    return client.get('user/airing', limit=limit)

def search(client, query):
    return client.get('user/search/%s' % query)

# write
def writeActivity(client, user, text, reply_id = None, messenger_id = None):
    if type(text) is not str:
        raise TypeError('text must be string')
    payload = { 'text' : text }
    if type(reply_id) is int:
        payload['reply_id'] = reply_id
    if type(messenger_id) is int:
        payload['messenger_id'] = messenger_id
    if len(payload) > 2:
        raise exception.AmbigiousCallError('reply_id and messenger_id cannot be used at once')
    return client.post('user/activity', data=payload)

# write
def deleteActivity(client, user, id, isreply=False):
    if type(id) is not int:
        raise TypeError('id must be int')
    return client.delete('user/activity/reply' if isreply else 'user/activity', data = { 'id' : id })

# write
"""
Toggles the follow state of an user

:param id: The Username to (un)follow
:return: string "followed"|"unfollowed"
"""
def toggleFollow(client, id):
    return client.post('user/follow', data={ 'id' : id })

"""
Adds or edits and entry on the animelist

:param id: The Anime ID
:param list_status: "plan to watch" || "completed" || "on-hold" || "dropped"
:param score: (string|int|float) Score value according to the user's preferences (10 point, 100 point, smiley, etc)
:param score-raw: (int) value from 0-100
:param episodes_watched: (int)
:param rewatched: (int)
:param notes: (string)
:param advanced_rating_scores: (string) comma separated scores, same order as advanced_rating_names (ex: ",,,," for empty or "10,40,0,,")
:param custom_lists: (string)  comma separated 1 or 0, same order as custom_list_anime (ex: ",,,," for empty or "1,1,0,,")
:param hidden_default: (int) 1 or 0
"""
# Note: The documentation states, a POST request should be used
#       to create an entry and a PUT request should modify one.
#       We just use PUT, as anilist.co itclient, user does this, too.
#       Greetings to Josh :)
def createAnimeEntry(client, id,
    list_status="plan to watch", 
    score=0, # (see comment - List score types)
    score_raw=0, # (see comment - Raw score)
    episodes_watched=0,
    rewatched=0,
    notes="",
    advanced_rating_scores=",,,,", 
    custom_lists=",,,,", 
    hidden_default=0):
    payload = {
        'id' : id,
        'list_status' : list_status,
        'score' : score,
        'score_raw' : score_raw,
        'episodes_watched' : episodes_watched,
        'rewatched' : rewatched,
        'notes' : notes,
        'advanced_rating_scores' : advanced_rating_scores,
        'custom_lists' : custom_lists,
        'hidden_default' : hidden_default,
    }
    return client.put('animelist', data=payload)

def createMangaEntry(client, id,
        list_status="plan to read",
        score=0, # (see comment - List score types)
        score_raw=0, # (see comment - Raw score)
        volumes_read=0,
        chapters_read=0,
        reread=0,
        notes="",
        advanced_rating_scores=",,,,",
        custom_lists=",,,,",
        hidden_default=0):
    payload = {
        'id' : id,
        'list_status' : list_status,
        'score' : score,
        'score_raw' : score_raw,
        'volumes_read' : volumes_read,
        'chapters_read' : chapters_read,
        'reread' : reread,
        'notes' : notes,
        'advanced_rating_scores' : advanced_rating_scores,
        'custom_lists' : custom_lists,
        'hidden_default' : hidden_default,
    }
    return client.put('mangalist', data=payload)

def deleteAnimeEntry(client, id):
    if type(id) is not int:
        raise TypeError("id must be positive int")
    return client.delete('animelist/%s' % id)

def deleteMangaEntry(client, id):
    if type(id) is not int:
        raise TypeError("id must be positive int")
    return client.delete('mangalist/%s' % id)
