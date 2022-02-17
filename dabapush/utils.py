def flatten(thing: dict, namespace: str = None, sep: str = '.') -> dict:
    res = {}
    for key, item in thing.items():
        if type(item) is dict:
            res = {
                **res,
                **{sep.join([namespace, k] if namespace is not None else [k]):v for (k,v) in flatten(item, key).items()}
            }
        else:
            res[sep.join([namespace, key] if namespace is not None else [key])] = item
    return res 

def safe_access(thing: dict, path: list[str]):
    def safety(thing: dict, attr: str) -> any or None:
        if attr in thing:
            return thing[attr]
    res = thing
    for attr in path:
        res = safety(res, attr)
        if res is None:
            break
    return res

def join(id: str, includes: list[any], id_key: str) -> any or None:
    """
    looks up an entity in a array of dicts by given key.
    """
    for included in includes:
        if id == included[id_key]:
            return included