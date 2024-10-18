def get_shared_keys(left_dict, right_dict):
    yield from set(left_dict.keys()).intersection(set(right_dict.keys()))
