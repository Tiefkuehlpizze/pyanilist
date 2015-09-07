from . import exception, userlist

class AnilistUser:

    def __init__(self, client, username):
        self.username = username
        self.client = client
    
    def getUserlist(self):
        return userlist.Userlist(self.client)

    def getBasic(self):
        reutrn self.client.get('user/' + self.username)

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
