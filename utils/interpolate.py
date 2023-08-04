def interpolate(minimum, maximum, weight):
    'Returns a value between minimum and maximum, weight is a float from 0-1'
    if minimum < 0: return interpolate(0, maximum + (minimum * -1), weight) + minimum
    else:           return ((maximum - minimum) * weight) + minimum
