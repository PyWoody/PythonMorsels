import json


from functools import wraps


def jsonify(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result_dict = func(*args, **kwargs)
        return json.dumps(result_dict)
    return inner
