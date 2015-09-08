from . import client

SEASONS = ['winter', 'spring', 'summer', 'fall']
TYPES = ['Tv', 'Movie', 'Special', 'OVA', 'ONA', 'Tv Short']
STATUS = ['Not Yet Aired', 'Currently Airing', 'Finished Airing', 'Cancelled']
SORT = ['id', 'score', 'popularity', 'start date', 'end date', 'id-desc', 'score-desc', 'popularity-desc', 'start date-desc', 'end date-desc']

def _idisint(id):
    if not isinstance(id, int):
        raise TypeError('the id must be int, not {!r}'.format(id.__class__.__name__))

def _get(client, path, id):
    _idisint(id)
    return client.get(path % id)

def basic(client, id):
    """ Gets basic data about an anime
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return _get(client, '/anime/%d', id)

def page(client, id):
    """ Gets all data about an anime to display a page with all related data
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return _get(client, '/anime/%d/page', id)

def characters(client, id):
    """ Gets data about an anime's characters
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return _get(client, '/anime/%d/characters', id)

def staff(client, id):
    """ Gets data about an anime's staff
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return _get(client, '/anime/%d/staff', id)

def actors(client, id):
    """ Gets data about an anime's actors
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: json string
    :rtype: str
    """
    return _get(client, '/anime/%d/actors', id)

def airing(client, id):
    """ Gets data about an anime's airing times
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: json string
    :rtype: str
    """
    return _get(client, '/anime/%d/airing', id)

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
    params = {}
    if page is not None:
        if isinstance(page, int):
            params['page'] = page
        else:
            raise TypeError('page must be int, not {!r}'.format(page.__class__.__name__))

    if year is not None:
        if isinstance(year, int) and (1900 <= year <= 9999):
            params['year'] = year
        else:
            raise TypeError('year must be int between 1900 and 9999'.format(year.__class__.__name__))

    if season is not None:
        if isinstance(season, str):
            if season.lower() in SEASONS:
                params['season'] = season
            else:
                raise TypeError('season must be in %s' % str(SEASONS))
        else:
            raise TypeError('season must be string, not {!r}'.format(season.__class__.__name__))

    if _type is not None:
        if isinstance(_type, str) and _type.lower() in map(str.lower, TYPES):
            params['type'] = _type
        else:
            raise TypeError('_type must be string and in %s' % str(TYPES))
    if status is not None:
        if isinstance(status, str) and status.lower() in map(str.lower, STATUS):
            params['status'] = status
        else:
            raise TypeError('status must be string and in %s' % str(STATUS))
    if genres is not None:
        if isinstance(genres, str):
            params['genres'] = genres
        else:
            raise TypeError('genres must be string, not {!r}'.format(genres.__class__.__name__))
    if genres_exclude is not None:
        if isinstance(genres_exclude, str):
            params['genres_exclude'] = genres_exclude
        else:
            raise TypeError('genres_exclude must be string, not {!r}'.format(genres_exclude.__class__.__name__))
    if sort is not None:
        if isinstance(sort, str):
            if sort.lower() in SORT:
                params['sort'] = sort
            else:
                raise TypeError('sort must be in %s' % str(SORT))
        else:
            raise TypeError('sort must be string, not {!r}'.format(sort.__class__.__name__))
    if airing_data is not None:
        if isinstance(airing_data, bool):
            params['airing_data'] = airing_data
        else:
            raise TypeError('airing must be bool, not {!r}'.format(airing_data.__class__.__name__))
    if full_page is not None:
        if isinstance(full_page, bool):
            params['full_page'] = full_page
        else:
            raise TypeError('full_page must be bool, not {!r}'.format(full_page.__class__.__name__))
    
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
