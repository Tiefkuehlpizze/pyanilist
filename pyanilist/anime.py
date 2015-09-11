from . import client

SEASONS = ['winter', 'spring', 'summer', 'fall']
TYPES = ['tv', 'movie', 'special', 'ova', 'ona', 'tv short']
STATUS = ['not yet aired', 'currently airing', 'finished airing', 'cancelled']
SORT = ['id', 'score', 'popularity', 'start date', 'end date', 'id-desc', 'score-desc', 'popularity-desc', 'start date-desc', 'end date-desc']

def genre_list(client):
    return client.get('genre_list')

def basic(client, id):
    """ Gets basic data about an anime
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return client.get('anime/%d' % id)

def page(client, id):
    """ Gets all data about an anime to display a page with all related data
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return client.get('anime/%d/page' % id)

def characters(client, id):
    """ Gets data about an anime's characters
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return client.get('anime/%d/characters' % id)

def staff(client, id):
    """ Gets data about an anime's staff
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return cient.get('anime/%d/staff' % id)

def actors(client, id):
    """ Gets data about an anime's actors
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: json string
    :rtype: str
    """
    return client.get('anime/%d/actors' % id)

def airing(client, id):
    """ Gets data about an anime's airing times
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: json string
    :rtype: str
    """
    return client.get('anime/%d/airing' % id)

def browse(client, 
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
    """ Searches animes with the given parameters

    :param client: an instance of a :class:`Client <Client>`
    :param page: (optional) int type
    :param year: (optional) int type 4 digit year
    :param season: (optional) str "spring" || "summer" || "fall" || "winter"
    :param _type: (optional) str "Tv"  || "Movie"  || "Special"  || "OVA"  || "ONA"  || "Tv Short"
    :param status: (optional) str "Not Yet Aired" || "Currently Airing" || "Finished Airing" || "Cancelled"
    :param genres: (optional str comma separated genre string. e.g. "Action,Comedy" Returns anime that have ALL the genres
    :param genres_exclude: (optional) str comma separated genre string. e.g. "Action,Comedy" Excludes returning anime that have ANY of the genres.
    :param sort: (optional) str "id" || "score" || "popularity" || "start date" || "end date" Sorts results, default ascending order. Append "-desc" for descending order e.g. "id-desc"
    :param airing_data: (optional) bool Includes anime airing data in small models
    :param full_page: (optional) Returns all available results. Ignores pages. Only available when status="Currently Airing" or season is included
    :return: json string
    :rtype: str
    """
    nonecheck = {
        'page' : page,
        'year' : year,
        'genres' : genres,
        'genres_exclude' : genres,
        'airing_data' : airing_data,
        'full_page' : full_page,
    }
    params = {}
    for (name, val) in nonecheck.items():
        if val is not None:
            params[name] = val

    if season is not None:
        if season.lower() in SEASONS:
            params['season'] = season
        else:
            raise TypeError('season must be in %s' % str(SEASONS))
    if _type is not None:
        if _type.lower() in TYPES:
            params['type'] = _type
        else:
            raise TypeError('_type must be in %s' % str(TYPES))
    if status is not None:
        if status.lower() in STATUS:
            params['status'] = status
        else:
            raise TypeError('status must be in %s' % str(STATUS))
    if sort is not None:
        if sort.lower() in SORT:
            params['sort'] = sort
        else:
            raise TypeError('sort must be in %s' % str(SORT))
    
    return client.get('browse/anime', data=params)

def favourite(client, id):
    """ Toggles the favourite status of an anime

    :param client: an instance of a :class:`Client <Client>`
    :param id: the id
    :return: "Favourite Added" || "Favourite Removed"
    :rtype: str
    """
    _idisint(id)
    client.hasLogin()
    return client.post('anime/favourite', data={ 'id' : id })

def search(client, query):
    """ Searches an anime by its name
    
    :param client: an instance of a :class:`Client <Client>`
    :param query: string to search for
    :return: json string
    :rtype: str
    """
    return client.get('anime/search/%s' % query)
