from . import client

def basic(client, id):
    """ Gets basic data about an character
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return client.get('character/%d' % id)

def page(client, id):
    """ Gets all data about an character to display a page with all related data
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :return: the json answer of the API
    :rtype: str
    """
    return clien.get('character/%d/page' % id)

def favourite(client, id):
    """ Toggles the favourite status of an character

    :param client: an instance of a :class:`Client <Client>`
    :param id: the id
    :return: "Favourite Added" || "Favourite Removed"
    :rtype: str
    """
    client.hasLogin()
    return client.post('character/favourite', data={ 'id' : id })

def search(client, query):
    """ Searches an character by its name
    
    :param client: an instance of a :class:`Client <Client>`
    :param query: string to search for
    :return: json string
    :rtype: str
    """
    return client.get('character/search/%s' % query)
