import re
from unicodedata import normalize


def clean_string(some_string):
    # removes escape chars and excess spaces
    normal_str = normalize('NFKD', some_string)
    # remove line breaks
    no_lines = re.sub('\\r\\n|\\n\\n', ' ', normal_str)
    # reduce spaces
    condensed = re.sub(' +', ' ', no_lines)
    return condensed.strip()


def text_values(ResultSet):
    return [clean_string(el.text) for el in ResultSet]


def add_properties(obj, names, values):
    for idx, value in enumerate(values):
        setattr(obj, names[idx], value)

def dict_values(dict):
    return [dict[key] for key in dict.keys()]

def lists2dict(keys, values):
    return {k: v for k, v in map(lambda k, v: (k, v), keys, values)}
