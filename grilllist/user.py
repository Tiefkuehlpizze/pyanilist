from . import exception, animelist

class AnilistUser:

    def __init__(self, client, username):
        self.username = username
        self.client = client
    
    def __str__(self):
        ret = self.username + " | "
        ret += "Basic: %s | " %        str(hasattr(self, 'basic'))
        ret += "Activity: %s | " %     str(hasattr(self, 'activities'))
        ret += "Followers: %s | " %    str(hasattr(self, 'followers'))
        ret += "Favourites: %s | " %   str(hasattr(self, 'favourites'))
        ret += "Anilist: %s | " %      str(hasattr(self, 'anilist'))
        ret += "Mangalist: %s" %    str(hasattr(self, 'mangalist'))
        return ret

    def getAnimelist(self):
        return animelist.Animelist(self.client)

    def getblob(self):
        attributes = [ 'activities', 'followers', 'following', 'favourites',
                'anilist', 'mangalist', ]
        blob = { }
        if hasattr(self, 'basic'):
            blob['profile'] = self.basic
        for attr in attributes:
            if hasattr(self, attr):
                blob[attr] = getattr(self, attr)
        return blob
    
    def loadAll(self):
        self.loadBasic()
        self.loadActivities()
        self.loadFollower()
        self.loadFollowing()
        self.loadFavourites()
        self.loadAnilist()
        self.loadMangalist()


    def loadBasic(self):
        self.basic = self.client.get('user/' + self.username)
        return self.basic

    def loadFollower(self):
        self.follower = self.client.get('user/%s/followers' % self.username)
        return self.follower

    def loadFollowing(self):
        self.following = self.client.get('user/%s/following' % self.username)
        return self.following

    def loadFavourites(self):
        self.favourites = self.client.get('user/%s/favourites' % self.username)
        return self.favourites

    def loadAnimelist(self):
        self.anilist = self.client.get('user/%s/animelist' % self.username)
        return self.anilist

    def loadMangalist(self):
        self.mangalist = self.client.get('user/%s/mangalist' % self.username)
        return self.mangalist

    def getActivities(self, user=None, page=0):
        if type(page) is not int:
            page = 0
        if type(user) is str:
            return self.client.get('user/%s/activity' % user)
        elif user is None:
            self.activities = self.client.get('user/activity', page=page)
            return self.activities
        raise TypeError('user must be str or None')

    def loadNotifications(self):
        self.client.hasLogin()
        self.notifications = self.client.get('user/notifications')
        return self.notifications

    def getNotificationCount(self):
        self.client.hasLogin()
        self.notificationcount = self.client.get('user/notifications/count')
        return self.notificationcount

    def loadAiring(self, limit=None):
        self.client.hasLogin()
        self.airing = self.client.get('user/airing', limit=limit)
        return self.airing

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
