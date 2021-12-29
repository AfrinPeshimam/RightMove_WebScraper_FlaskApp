def get_type(x):
    if 'apartment' in x:
        return 'apartment'
    if 'house' or 'House' in x:
        return 'house'
    if 'Property' or 'property' in x:
        return 'property'
    if 'flat' in x:
        return 'flat'

