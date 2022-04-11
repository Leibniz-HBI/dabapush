def flatten(thing: dict, namespace: str = None, sep: str = ".") -> dict:
    """Flattens a nested dictionary. The flattened keys are joined together with the specified seperator.
    `flatten` only traverses dicts, consequently `list` items are left as is.

    Example
    -------

    To flatten a nested dict:

    >>> not_nice = {'a': {'b': 'yuk'}}
    ... flatten(not_nice)
    {'a.b.': 'yuk'}

    Lists are not unpacked:

    >>> nested_list = {'a': {'b': 'yuk', 'c': [{'d': 'meh'}]}}
    ... flatten(nested_list)
    {'a.b': 'yuk', 'a.c': [{'d': 'meh'}]}

    Parameters
    ----------
    thing : dict
        Nested dict to flatten
    namespace : str
        namespace to preprepend to output key (default value = None)
    sep : str
        Seperator character to use (default value = '.')

    Returns
    -------
    type dict:
        the flattened dict

    """
    res = {}
    for key, item in thing.items():
        if type(item) is dict:
            res = {
                **res,
                **{
                    sep.join([namespace, k] if namespace is not None else [k]): v
                    for (k, v) in flatten(item, key).items()
                },
            }
        else:
            res[sep.join([namespace, key] if namespace is not None else [key])] = item
    return res


def safe_access(thing: dict, path: list[str]):
    """Safely access deep values in a nested dict without risking running into a `KeyException`.
    If the specified key path is not present in the dict `safe_access` returns `None`.

    Parameters
    ----------
    thing : dict
        A (possibly deeply nested) dictionary to retrieve values from.
    path : list[str]
        List of keys
    Returns
    -------
    any or None:
        Returns whichever value is at the leaf of the specified key path or None if no such value exists.
    """

    def safety(thing: dict, attr: str) -> any or None:
        if attr in thing:
            return thing[attr]

    res = thing
    for attr in path:
        res = safety(res, attr)
        if res is None:
            break
    return res


def unpack(id: str, includes: list[any], id_key: str) -> any or None:
    """Looks up an entity in a array of dicts by given key.

    Parameters
    ----------
    id : str
        Value to look for.
    includes : list[any]
        List of dicts to look in.
    id_key : str
        Key of those dicts to look in.

    Returns
    -------

    """
    for included in includes:
        if id == included[id_key]:
            return included
