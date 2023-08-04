def copy_dict(obj):
    result = {}
    for name, value in obj.items():
        if isinstance(value, dict):
            value = copy_dict(value)
        result[name] = value
    return result
