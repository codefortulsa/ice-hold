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



def make_filter(columns):
        # make a list of valid column indexes
        # returns a function to filter out invalid columns
        unique_columns = []

        def is_valid(column_title):
            # check for blanks
            if not column_title:
                return False
            # check for duplicates
            if column_title in unique_columns:
                return False
            unique_columns.append(column_title)
            return True

        # make a list of indices that pass the validity test
        test_indexes = [i for i, v in enumerate(columns) if is_valid(v)]
        # remove any indices that failed
        valid_indexes = list(filter(lambda v: v is not None, test_indexes))

        # make a function to remove invalid items from a list
        def list_filter(raw_list):
            def check_valid_index(enum):
                idx, val = enum
                return True if idx in valid_indexes else False
            valid_enums = filter(check_valid_index, enumerate(raw_list))
            return [e[1].strip() for e in valid_enums]

        return list_filter
