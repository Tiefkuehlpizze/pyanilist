from . import client

TAGS = {1: 'Anime', 2: 'Manga', 3: 'Light Novels',
        4: 'Visual Novels', 5: 'Release Discussion', 6: '(Unused)',
        7: 'General', 8: 'News', 9: 'Music',
        10: 'Gaming', 11: 'Site Feedback', 12: 'Bug Reports',
        13: 'Site Announcements', 14: 'List Customisation', 15: 'Recommendations',
        16: 'Forum Games', 17: 'Misc', 18: 'AniList Apps'
        }


def recent(client, page=1):
    """ Gets recent threads

    :param client: an instance of a :class:`Client <Client>`
    :param page: the page to get (starting at 1)
    :return: json string
    :rtype: str
    """
    return client.get('forum/recent', data={'page': page})


def new(client, page=1):
    """ Gets new threads

    :param client: an instance of a :class:`Client <Client>`
    :param page: the page to get (starting at 1)
    :return: json string
    :rtype: str
    """
    return client.get('forum/new', data={'page': page})


def subscribed(client, page=1):
    """ Gets subscribed threads

    :param client: an instance of a :class:`Client <Client>`
    :param page: the page to get (starting at 1)
    :return: json string
    :rtype: str
    """
    client.hasLogin()
    return client.get('forum/subscribed', data={'page': page})


def thread(client, id):
    """ Gets a thread

    :param client: an instance of a :class:`Client <Client>`
    :param id: thread id
    :return: json string
    :rtype: str
    """
    return client.get('forum/thread/%d' % id)


def bytag(client, tag="", anime="", manga="", page=1):
    """ Gets threads by tags

    :param client: an instance of a :class:`Client <Client>`
    :param tag: comma separated tag ids
    :param anime: comma separated anime ids
    :param manga: comma separated manga ids
    :param page: the page to get (starting at 1)
    :return: json string
    :rtype: str
    """
    return client.get('forum/tag', data={'tag': tag, 'anime': anime, 'manga': manga, 'page': page})


def _create(method, title, body, tags, tags_anime, tags_manga):
    """ Creates a new thread

    :param method: a method of a :class:`Client <Client>` instance
    :param title: str thread title
    :param body: str thread body
    :param tags: comma separated tag ids
    :param tags_anime: comma separated anime ids
    :param tags_manga: comma separated manga ids
    :return: ?
    :rtype: ?
    """
    if len(title) == 0:
        raise ValueError('Title can not be empty')
    if len(body) == 0:
        raise ValueError('Body can not be empty')
    return method('forum/thread',
                  data={'title': title, 'body': body, 'tags': tags, 'tags_anime': tags_anime, 'tags_manga': tags_manga})


def create(client, title, body, tags, tags_anime, tags_manga):
    """ Creates a new thread

    :param client: an instance of a :class:`Client <Client>`
    :param title: str thread title
    :param body: str thread body
    :param tags: comma separated tag ids
    :param tags_anime: comma separated anime ids
    :param tags_manga: comma separated manga ids
    :return: ?
    :rtype: ?
    """
    _create(client.post, title, body, tags, tags_anime, tags_manga)


def edit(client, title, body, tags, tags_anime, tags_manga):
    """ Creates a new thread

    :param client: an instance of a :class:`Client <Client>`
    :param title: str thread title
    :param body: str thread body
    :param tags: comma separated tag ids
    :param tags_anime: comma separated anime ids
    :param tags_manga: comma separated manga ids
    :return: ?
    :rtype: ?
    """
    _create(client.put, title, body, tags, tags_anime, tags_manga)


def delete(client, id):
    """ Deletes a thread

    :param client: an instance of a :class:`Client <Client>`
    :param id: int thread id
    :return: ?
    :rtype: ?
    """
    return client.delete('forum/thread/%d' % id)


def subscribe(client, id):
    """ toggles subscription of thread

    :param client: an instance of a :class:`Client <Client>`
    :param id: int thread id
    :return: "subscribed" || "unsubscribed" (unverified)
    :rtype: str
    """
    return client.post('forum/comment/subscribe', data={'thread_id': id})


def comment(client, id, comment, reply_id=None):
    """ Writes a comment to a thread

    :param client: an instance of a :class:`Client <Client>`
    :param id: int thread id
    :param comment: str comment text
    :param reply_id: comment id (only when replying)
    :return: ?
    :rtype: ?
    """
    if len(comment) == 0:
        raise ValueError("comment can not be empty")
    params = {
        'thread_id': id,
        'comment': comment,
    }
    if reply_id is not None:
        params['reply_id'] = reply_id
    return client.post('forum/comment', data=params)


def edit_comment(client, id, comment):
    """ Edits a comment

    :param client: an instance of a :class:`Client <Client>`
    :param id: int comment id
    :param comment: str comment text
    :return: ?
    :rtype: ?
    """
    if len(comment) == 0:
        raise ValueError("comment can not be empty")
    params = {
        'thread_id': id,
        'comment': comment,
    }
    return client.post('forum/comment', data=params)


def delete_comment(client, id):
    """ Deletes a comment

    :param client: an instance of a :class:`Client <Client>`
    :param id: int comment id
    :return: ?
    :rtype: ?
    """
    return client.delete('forum/comment/%d' % id)


def search(client, query):
    """ Searches the forum

    :param client: an instance of a :class:`Client <Client>`
    :param query: query to search for
    :return: json
    :rtype: str
    """
    return client.get('forum/search/%s' % query)
