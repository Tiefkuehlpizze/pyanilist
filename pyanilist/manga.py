from . import client

TYPES = ['manga', 'novel', 'manhua', 'manhwa', 'one', 'doujin']
STATUS = ['not yet published', 'currently publishing', 'finished', 'cancelled']
SORT = ['id', 'score', 'popularity', 'start date', 'end date', 'id-desc', 'score-desc', 'popularity-desc',
        'start date-desc', 'end date-desc']


def genre_list(client):
    return client.get('genre_list')


def basic(client, id):
    """ Gets basic data about an manga
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return client.get('manga/%d' % id)


def page(client, id):
    """ Gets all data about an manga to display a page with all related data
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return client.get('manga/%d/page' % id)


def characters(client, id):
    """ Gets data about an manga's characters
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return client.get('manga/%d/characters' % id)


def staff(client, id):
    """ Gets data about an manga's staff
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return client.get('manga/%d/staff' % id)


def browse(client,
           page=None,
           year=None,
           _type=None,
           status=None,
           genres=None,
           genres_exclude=None,
           sort=None
           ):
    """ Searches mangas with the given parameters

    :param client: an instance of a :class:`Client <Client>`
    :param page: (optional) int type
    :param year: (optional) int type 4 digit year
    :param _type: (optional) str "Manga" ||  "Novel" ||  "Manhua" ||  "Manhwa" ||  "One" ||  "Doujin"
    :param status: (optional) str "Not Yet Published" || "Currently Publishing" || "Finished" || "Cancelled"
    :param genres: (optional str comma separated genre string. e.g. "Action,Comedy" Returns manga that have ALL the genres
    :param genres_exclude: (optional) str comma separated genre string. e.g. "Action,Comedy" Excludes returning manga that have ANY of the genres.
    :param sort: (optional) str "id" || "score" || "popularity" || "start date" || "end date" Sorts results, default ascending order. Append "-desc" for descending order e.g. "id-desc"
    :return: json string
    :rtype: str
    """
    params = {}
    if page is not None:
        params['page'] = page

    if year is not None:
        params['year'] = year

    if _type is not None:
        if _type.lower() in map(str.lower, TYPES):
            params['type'] = _type
        else:
            raise ValueError('_type must be in %s' % str(TYPES))
    if status is not None:
        if status.lower() in map(str.lower, STATUS):
            params['status'] = status
        else:
            raise ValueError('status must be in %s' % str(STATUS))
    if genres is not None:
        params['genres'] = genres
    if genres_exclude is not None:
        params['genres_exclude'] = genres_exclude
    if sort is not None:
        if sort.lower() in SORT:
            params['sort'] = sort
        else:
            raise TypeError('sort must be in %s' % str(SORT))

    return client.get('browse/manga', data=params)


def favourite(client, id):
    """ Toggles the favourite status of an manga

    :param client: an instance of a :class:`Client <Client>`
    :param id: the id
    :return: "Favourite Added" || "Favourite Removed"
    :rtype: str
    """
    client.hasLogin()
    return client.post('manga/favourite', data={'id': id})


def search(client, query):
    """ Searches an manga by its name
    
    :param client: an instance of a :class:`Client <Client>`
    :param query: string to search for
    :return: json string
    :rtype: str
    """
    return client.get('manga/search/%s' % query)
