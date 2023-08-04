def dict_insert_at_index(dict, item_key, item_value, index):
    if index < len(dict):
        result = {}
        left   = list(dict)[:index]
        right  = list(dict)[index:]

        for key in left: result[key] = dict[key]
        result[item_key] = item_value
        for key in right: result[key] = dict[key]

        dict.clear(); dict.update(result)

    else:
        dict[item_key] = item_value
