
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
        self.loadFavourites()
        self.loadAnilist()
        self.loadMangalist()


    def loadBasic(self):
        self.basic = self.client.get('user/' + self.username)

    def loadActivities(self):
        self.activities = self.client.get('user/%s/activity' % self.username)

    def loadFollower(self):
        self.follower = self.client.get('user/%s/followers' % self.username)
        self.following = self.client.get('user/%s/following' % self.username)

    def loadFavourites(self):
        self.favourites = self.client.get('user/%s/favourites' % self.username)

    def loadAnimelist(self):
        self.anilist = self.client.get('user/%s/animelist' % self.username)

    def loadMangalist(self):
        self.mangalist = self.client.get('user/%s/mangalist' % self.mangalist)
