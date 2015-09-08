from . import client

def _idisint(id):
    if not isinstance(id, int):
        raise TypeError('the id must be int, not {!r}'.format(id.__class__.__name__))

def _get(client, path, id):
    _idisint(id)
    return client.get(path % id)

def basic(client, id):
    """ Gets basic data about an studio
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return _get(client, 'studio/%d', id)

def page(client, id):
    """ Gets all data about an studio to display a page with all related data
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return _get(client, 'studio/%d/page', id)

def favourite(client, id):
    """ Toggles the favourite status of an studio

    :param client: an instance of a :class:`Client <Client>`
    :param id: the id
    :return: "Favourite Added" || "Favourite Removed"
    :rtype: str
    """
    _idisint(id)
    client.hasLogin()
    return client.post('studio/favourite', data={ 'id' : id })

def search(client, query):
    """ Searches an studio by its name
    
    :param client: an instance of a :class:`Client <Client>`
    :param query: string to search for
    :return: json string
    :rtype: str
    """
    return client.get('studio/search/%s' % query)
