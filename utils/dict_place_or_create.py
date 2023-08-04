def dict_place_or_create(dictionary, *args):
    '''
    Modifies given dictionary,
    traverses/creates indexes given by arguments
    inserts last argument under the key given next to last
    '''
    d = dictionary
    for i, key in enumerate(args):
        if i == len(args) - 2:
            d[args[-2]] = args[-1]
            break
        else:
            if key not in d.keys():
                d[key] = {}
            d = d[key]
