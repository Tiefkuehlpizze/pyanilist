from . import exception, userlist

class AnilistUser:

    def __init__(self, client, username):
        self.username = username
        self.client = client
    
    def getUserlist(self):
        return userlist.Userlist(self.client)

    def getBasic(self):
        return self.client.get('user/' + self.username)

    def getFollower(self):
        return self.client.get('user/%s/followers' % self.username)

    def getFollowing(self):
        return self.client.get('user/%s/following' % self.username)

    def getFavourites(self):
        return self.client.get('user/%s/favourites' % self.username)

    def getAnimelist(self):
        return self.client.get('user/%s/animelist' % self.username)

    def getMangalist(self):
        return self.client.get('user/%s/mangalist' % self.username)

    def getActivities(self, user=None, page=0):
        if type(page) is not int:
            page = 0
        if type(user) is str:
            return self.client.get('user/%s/activity' % user)
        elif user is None:
            return self.client.get('user/activity', page=page)
        raise TypeError('user must be str or None')

    def getNotifications(self):
        self.client.hasLogin()
        return self.client.get('user/notifications')

    def getNotificationCount(self):
        self.client.hasLogin()
        return self.client.get('user/notifications/count')

    def getAiring(self, limit=None):
        self.client.hasLogin()
        return self.client.get('user/airing', limit=limit)

    def search(self, query):
        return self.client.get('user/search/%s' % query)

    # write
    def writeActivity(self, text, reply_id = None, messenger_id = None):
        if type(text) is not str:
            raise TypeError('text must be string')
        payload = { 'text' : text }
        if type(reply_id) is int:
            payload['reply_id'] = reply_id
        if type(messenger_id) is int:
            payload['messenger_id'] = messenger_id
        if len(payload) > 2:
            raise exception.AmbigiousCallError('reply_id and messenger_id cannot be used at once')
        return self.client.post('user/activity', data=payload)

    # write
    def deleteActivity(self, id, isreply=False):
        if type(id) is not int:
            raise TypeError('id must be int')
        return self.delete('user/activity/reply' if isreply else 'user/activity', data = { 'id' : id })
   
    # write
    """
    Toggles the follow state of an user

    :param id: The Username to (un)follow
    :return: string "followed"|"unfollowed"
    """
    def toggleFollow(self, id):
        return self.client.post('user/follow', data={ 'id' : id })

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
    #       We just use PUT, as anilist.co itself does this, too.
    #       Greetings to Josh :)
    def createAnimeEntry(self, id,
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
        return self.client.put('animelist', data=payload)
    
    def createMangaEntry(self, id,
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
        return self.client.put('mangalist', data=payload)

    def deleteAnimeEntry(self, id):
        if type(id) is not int:
            raise TypeError("id must be positive int")
        return self.client.delete('animelist/%s' % id)

    def deleteMangaEntry(self, id):
        if type(id) is not int:
            raise TypeError("id must be positive int")
        return self.client.delete('mangalist/%s' % id)
