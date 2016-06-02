from . import exception


def get_me(client):
    return get_basic(client)


def get_basic(client, user=None):
    return client.get('user' + ('/%s' % user if user is not None else ''))


def get_follower(client, user):
    return client.get('user/%s/followers' % user)


def get_following(client, user):
    return client.get('user/%s/following' % user)


def get_favourites(client, user):
    return client.get('user/%s/favourites' % user)


def get_animelist(client, user):
    return client.get('user/%s/animelist' % user)


def get_mangalist(client, user):
    return client.get('user/%s/mangalist' % user)


def get_activities(client, user=None, page=0):
    if user is not None:
        return client.get('user/%s/activity' % user, data={'page': page})
    return client.get('user/activity', data={'page': int(page)})


def get_notifications(client):
    client.hasLogin()
    return client.get('user/notifications')


def get_notification_count(client):
    client.hasLogin()
    return client.get('user/notifications/count')


def get_airing(client, limit=None):
    client.hasLogin()
    return client.get('user/airing', data={'limit': limit})


def search(client, query):
    return client.get('user/search/%s' % query)


# write
def write_activity(client, text, reply_id=None, messenger_id=None):
    payload = {'text': text}
    if reply_id is not None:
        payload['reply_id'] = reply_id
    if messenger_id is not None:
        payload['messenger_id'] = messenger_id
    if len(payload) > 2:
        raise exception.AmbigiousCallError('reply_id and messenger_id cannot be used at once')
    return client.post('user/activity', data=payload)


# write
def delete_activity(client, id, isreply=False):
    return client.delete('user/activity/reply' if isreply else 'user/activity', data={'id': id})


# write
"""
Toggles the follow state of an user

:param id: The Username to (un)follow
:return: string "followed"|"unfollowed"
"""


def toggle_follow(client, id):
    return client.post('user/follow', data={'id': id})


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
def create_anime_entry(client, id,
                       list_status="plan to watch",
                       score=0,  # (see comment - List score types)
                       score_raw=0,  # (see comment - Raw score)
                       episodes_watched=0,
                       rewatched=0,
                       notes="",
                       advanced_rating_scores=",,,,",
                       custom_lists=",,,,",
                       hidden_default=0):
    payload = {
        'id': id,
        'list_status': list_status,
        'score': score,
        'score_raw': score_raw,
        'episodes_watched': episodes_watched,
        'rewatched': rewatched,
        'notes': notes,
        'advanced_rating_scores': advanced_rating_scores,
        'custom_lists': custom_lists,
        'hidden_default': hidden_default,
    }
    return client.put('animelist', data=payload)


def create_manga_entry(client, id,
                       list_status="plan to read",
                       score=0,  # (see comment - List score types)
                       score_raw=0,  # (see comment - Raw score)
                       volumes_read=0,
                       chapters_read=0,
                       reread=0,
                       notes="",
                       advanced_rating_scores=",,,,",
                       custom_lists=",,,,",
                       hidden_default=0):
    payload = {
        'id': id,
        'list_status': list_status,
        'score': score,
        'score_raw': score_raw,
        'volumes_read': volumes_read,
        'chapters_read': chapters_read,
        'reread': reread,
        'notes': notes,
        'advanced_rating_scores': advanced_rating_scores,
        'custom_lists': custom_lists,
        'hidden_default': hidden_default,
    }
    return client.put('mangalist', data=payload)


def delete_anime_entry(client, id):
    return client.delete('animelist/%s' % id)


def delete_mang_eEntry(client, id):
    return client.delete('mangalist/%s' % id)


def get_reviews(client, id):
    return client.get("user/%s/reviews" % id)
