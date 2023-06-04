from django.core.cache import cache


def get_data_from_cache(key: str):
    '''responsible for retrieving the data stored in cache'''
    cache_data = cache.get(key)

    if not cache_data:
        return None
    return {'successful': True,  'response': cache_data}


def set_data_to_cache(key: str, value, timeout):
    """Responsible for adding data to the cache"""
    data_already_cached = get_data_from_cache(key)

    if not timeout:
        timeout = 300  # by default, data will be cached for a maximum of 5 minutes

    if data_already_cached:
        return {'successful': False, 'response': 'Data already cached'}

    try:
        cache.set(key, value, timeout=timeout)
    except Exception as cache_exception:
        return {'successful': False, 'response': cache_exception}

    return {'successful': True, 'response': 'Item added to cache'}


def remove_data_from_cache(key: str):
    """Responsible for removing data from the cache"""
    data_already_cached = get_data_from_cache(key)

    if not data_already_cached:
        return {'successful': False, 'response': 'Could not find element in cache'}

    try:
        cache.delete(key)
    except Exception as cache_exception:
        return {'successful': False, 'response': cache_exception}

    return {'successful': True, 'response': 'deleted'}
