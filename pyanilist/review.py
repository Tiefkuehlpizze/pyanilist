from . import client

AOM = ["anime", "manga"]


def _aomvalid(aom):
    if aom not in AOM:
        raise TypeError("aom must be in %s" % str(AOM))


def _get(client, path, id, aom):
    _aomvalid(aom)
    return client.get(path % (aom, id))


def get(client, id, aom="anime"):
    """ Gets a review
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :param aom: str "anime" || "manga"
    :return: the json answer of the API
    :rtype: str
    """
    return _get(client, '%s/%d', id, aom)


def get_for(client, id, aom="anime"):
    """ Gets multiple reviews for an anime|manga
    
    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to get
    :param aom: str "anime" || "manga"
    :return: the json answer of the API
    :rtype: str
    """
    return _get(client, '%s/%d/reviews', id, aom)


def rate(client, id, rating=0, aom='anime'):
    """ Rates a review

    :param client: an instance of a :class:`Client <Client>`
    :param id: the id to rate
    :param rating: int 0 (no rating), 1 (positive rating), 2 (negative rating)
    :param aom: str "anime" || "manga"
    :return: ?
    :rtype: ?
    """
    _aomvalid(aom)
    if not 2 <= rating <= 0:
        raise ValueError('rating must be 0-2, not {!r}'.format(rating))
    client.post('%s/review/rate' % aom, data={'id': id, 'rating': rating})


def create(client,
           anime_id=None,
           manga_id=None,
           text=None,
           summary=None,
           private=None,
           score=None):
    """ Creates a review 

    :param client: an instance of a :class:`Client <Client>`
    :param anime_id: (int)
    :param manga_id: (int) (required if anime_id is not set)
    :param text: (str) at least 2000 chars
    :param summary: (str) 20-120 chars
    :param private: (int) 0 or 1
    :param score: (int) 0-100 review score
    :return: ?
    :rtype: ?
    """
    payload = {}
    aom = None
    if anime_id is not None and manga_id is not None:
        raise TypeError('Cannot set anime_id and manga_id at the same time')
    if anime_id is not None:
        payload['anime_id'] = anime_id
        aom = AOM[0]
    if manga_id is not None:
        payload['manga_id'] = manga_id
        aom = AOM[1]
    if len(text) < 2000:
        raise ValueError('text must have at least 2000 chars, not {!r}'.format(len(text)))
    payload['text'] = text
    if not 20 <= len(summary) <= 120:
        raise ValueError('summary must have at least 20 and maximal 120 chars, not {!r}'.format(len(summary)))
    payload['summary'] = summary
    payload['private'] = private
    if score is not None:
        payload['score'] = score

    client.put("%s/review" % aom, data=payload)


def delete(client, id, aom="anime"):
    """ Deletes a review

    :param client: an instance of a :class:`Client <Client>`
    :param id: the id
    :param aom: str "anime" || "manga"
    :return: ?
    :rtype: ?
    """
    _aomvalid(aom)
    return client.delete('%s/review' % aom, data={'id': id})
