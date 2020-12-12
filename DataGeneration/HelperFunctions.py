def add_n_to_dict(dic, dict_key, num):
    """
    Adds n to a dict, creates a new entry if no key exists.
    :param dic: The dictionary to be added to.
    :param dict_key: The key in the dictionary to be added to.
    :param num: The amount to be added to the dict.
    """
    if dict_key not in dic.keys():
        dic[dict_key] = num
    else:
        dic[dict_key] += num

def sort_ascending(dic):
    """
    Sorts a dictionary in ascending order
    :param dic: The dictionary to sort
    :return: The sorted dictionary
    """
    return dict(sorted(dic.items(), key=lambda item: item[1]))

def sort_descending(dic):
    """
    Sorts a dictionary in descending order
    :param dic: The dictionary to sort
    :return: The sorted dictionary
    """
    return dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))
