from . import session, anime as _anime, character as _char, client as _client, forum as _forum, manga as _manga, staff as _staff, studio as _studio, review as _review, user as _user

class Anilist:
    
    ANIME_TYPES = _anime.TYPES
    ANIME_STATUS = _anime.STATUS
    AOM = _review.AOM
    FORUM_TAGS = _forum.TAGS
    MANGA_TYPES = _manga.TYPES
    MANGA_STATUS = _manga.STATUS
    SEASONS = _anime.SEASONS
    SORT = _anime.SORT

    def __init__(self, id, secret):
        self._con = _client.Client(id, secret)
        self.anime = Anilist.Anime(self._con)
        self.character = Anilist.Character(self._con)
        self.forum = Anilist.Forum(self._con)
        self.manga = Anilist.Manga(self._con)
        self.staff = Anilist.Staff(self._con)
        self.studio = Anilist.Studio(self._con)
        self.review = Anilist.Review(self._con)
        self.user = Anilist.User(self._con)
    
    def get_pin_uri(self):
        return self._con.get_pin_uri()

    def set_pin(self, pin):
        self._con.set_pin(pin)
    
    def set_session(self, obj):
        self._con.set_session(obj)

    def get_session(self):
        return self._con.get_session()

    def restore_session(self, access_token, expire_time, pin=None, refresh_token=None):
        self._con.restore_session(access_token, expire_time, pin, refresh_token)

    class API:
        def __init__(self, con):
            self._con = con
    
    class Anime(API):
        def genre_list(self):
            return _anime.genre_list(self._con)
        def basic(self, id):
            return _anime.basic(self._con, id)
        def page(self, id):
            return _anime.page(self._con, id)
        def characters(self, id):
            return _anime.characters(self._con, id)
        def staff(self, id):
            return _anime.staff(self._con, id)
        def actors(self, id):
            return _anime.actors(self._con, id)
        def airing(self, id):
            return _anime.airing(self._con, id)
        def browse(self, 
                page=None,
                year=None,
                season=None,
                _type=None,
                status=None,
                genres=None,
                genres_exclude=None,
                sort=None,
                airing_data=None,
                full_page=None):
            return _anime.browse(self._con, page, year, season, _type, status, genres, genres_exclude, sort, airing_data, full_page)
        def favourite(self, id):
            return _anime.favourite(self._con, id)
        def search(self, query):
            return _anime.search(self._con, query)

    class Character(API):
        def basic(self, id):
            return _char.basic(self._con, id)
        def page(self, id):
            return _char.page(self._con, id)
        def favourite(self, id):
            return _char.favourite(self._con, id)
        def search(self, query):
            return _char.search(self._con, query)

    class Forum(API):
        def recent(self, page=1):
            return _forum.recent(self._con, page)
        def new(self, page=1):
            return _forum.recent(self._con, page)
        def subscribed(self, page=1):
            return _forum.subscribed(self._con, page)
        def thread(self, id):
            return _forum.thread(self._con, id)
        def bytag(self, tag="", anime="", manga="", page=1):
            return _forum.bytag(self._con, tag, anime, manga, page=1)
        def create(self, title, body, tags, tags_anime, tags_manga):
            return _forum.create(self._con, title, body, tags, tags_anime, tags_manga)
        def edit(self, title, body, tags, tags_anime, tags_manga):
            return _forum.edit(self._con, title, body, tags, tags_anime, tags_manga)
        def delete(self, id):
            return _forum.delete(self._con, id)
        def subscribe(self, id):
            return _forum.subscribe(self._con, id)
        def comment(self, id, comment, reply_id=None):
            return _forum.comment(self._con, id, comment, reply_id)
        def edit_comment(self, id, comment):
            return _forum.edit_comment(self._con, id, comment)
        def delete_comment(self, id):
            return _forum.delete_comment(self._con, id)
        def search(self, query):
            return _forum.search(self._con, query)

    class Manga(API):
        def genre_list(self):
            return _manga.genre_list(self._con)
        def basic(self, id):
            return _manga.basic(self._con, id)
        def page(self, id):
            return _manga.page(self._con, id)
        def characters(self, id):
            return _manga.characters(self._con, id)
        def staff(self, id):
            return _manga.staff(self._con, id)
        def browse(self,
                page=None,
                year=None,
                _type=None,
                status=None,
                genres=None,
                genres_exclude=None,
                sort=None
                ):
            return _manga.browse(self._con, page, year, _type, status, genres, genres_exclude, sort)
        def favourite(self, id):
            return _manga.favourite(self._con, id)
        def search(self, query):
            return _manga.search(self._con, query)

    class Review(API):
        def get(self, id, aom="anime"):
            return _review.get(self._con, id, aom)
        def get_for(self, id, aom="anime"):
            return _review.get_for(self._con, id, aom)
        def rate(self, id, rating=0, aom="anime"):
            return _review.rate(self._con, id, rating, aom)
        def create(self,
                anime_id=None,
                manga_id=None,
                text=None,
                summary=None,
                private=None,
                score=None):
            return _review.create(self._con, anime_id, manga_id, text, summary, private, score)
        def delete(self, id, aom="anime"):
            return _review.delete(self._con, id, aom)

    class Staff(API):
        def basic(self, id):
            return _staff.basic(self._con, id)
        def page(self, id):
            return _staff.page(self._con, id)
        def favourite(self, id):
            return _staff.favourite(self, id)
        def search(self, query):
            return _staff.search(self, id)

    class Studio(API):
        def basic(self, id):
            return _studio.basic(self._con, id)
        def page(self, id):
            return _studio.page(self._con, id)
        def favourite(self, id):
            return _studio.favourite(self, id)
        def search(self, query):
            return _studio.search(self, id)

    class User(API):
        def get_basic(self, user=None):
            return _user.get_basic(self._con, user)
        def get_follower(self, user):
            return _user.get_follower(self._con, user)
        def get_following(self, user):
            return _user.get_following(self._con, user)
        def get_favourites(self, user):
            return _user.get_following(self._con, user)     
        def get_animelist(self, user):
            return _user.get_animelist(self._con, user)
        def get_mangalist(self, user):
            return _user.get_mangalist(self._con, user)
        def get_activities(self, user=None, page=0):
            return _user.get_activities(self._con, user, page)
        def get_notifications(self):
            return _user.get_notifications(self._con)
        def get_notifications_count(self):
            return _user.get_notifications_count(self._con)
        def get_airing(self, limit=None):
            return _user.get_airing(self._con, limit)
        def get_search(self, query):
            return _user.search(self._con, query)
        def write_activity(self, user, text, reply_id=None, messenger_id=None):
            return _user.write_activity(self._con, user, text, reply_id, messenger_id)
        def delete_activity(self, id, isreply=False):
            return _user.delete_activity(self._con, id, isreply)
        def toggle_follow(self, id):
            return _user.toggle_follow(self._con, id)
        def create_anime_entry(self, id, 
            list_status = "plan to watch",
            score=0,
            score_raw=0,
            episodes_watched=0,
            rewatched=0,
            notes="",
            advanced_rating_scores=",,,,",
            custom_lists=",,,,",
             hidden_default=0):
            return _user.create_anime_entry(self._con, id, list_status, score, score_raw, episodes_watched, rewatched, notes, advanced_rating_scores, custom_lists, hidden_default)
        def create_manga_entry(self, id,
            list_status="plan to read",
            score=0,
            score_raw=0,
            volumes_read=0,
            chapters_read=0,
            reread=0,
            notes="",
            advanced_rating_scores=",,,,",
            custom_lists=",,,,",
            hidden_default=0):
            return _user.create_manga_entry(self._con, id, list_status, score, score_raw, volumes_read, chapters_read, reread, notes, advanced_rating_scores, custom_lists, hidden_default)
        def delete_anime_entry(self, id):
            return _user.delete_anime_entry(self._con, id)
        def delete_manga_entry(self, id):
            return _user.delete_manga_entry(self._con, id)
        def get_reviews(self, id):
            return _user.get_reviews(self._con, id)

