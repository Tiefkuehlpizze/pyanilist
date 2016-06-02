from . import client


def basic(client, id):
    """ Gets basic data about an studio
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return client.get('studio/%d' % id)


def page(client, id):
    """ Gets all data about an studio to display a page with all related data
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return client.get('studio/%d/page' % id)


def favourite(client, id):
    """ Toggles the favourite status of an studio

    :param client: an instance of a :class:`Client <Client>`
    :param id: the id
    :return: "Favourite Added" || "Favourite Removed"
    :rtype: str
    """
    client.hasLogin()
    return client.post('studio/favourite', data={'id': id})


def search(client, query):
    """ Searches an studio by its name
    
    :param client: an instance of a :class:`Client <Client>`
    :param query: string to search for
    :return: json string
    :rtype: str
    """
    return client.get('studio/search/%s' % query)
