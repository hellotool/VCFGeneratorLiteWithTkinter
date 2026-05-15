import gc


def replace_object[T](obj: T, new_obj: T):
    """Replace an object with another object in dict-type referrers.

    Note: This only handles dict referrers (e.g., module __dict__).
    References in lists, tuples, sets, or other containers are not replaced.
    """
    for referrer in gc.get_referrers(obj):
        if isinstance(referrer, dict):
            for key, value in referrer.items():
                if value is obj:
                    referrer[key] = new_obj
