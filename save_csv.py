import csv


# function for saving a csv files
# file_name: you know this one ...
# columns:  a list of strings for column titles
# data_rows: an iter that provides list of values
def save_csv(file_name, data_iter):
    # make a list of valid column indexes
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

    # assumes the first row is column titles
    columns = next(data_iter)
    # make a list of indices that pass the validity test
    test_indexes = [i for i,v in enumerate(columns) if is_valid(v)]
    # remove any indices that failed
    valid_indexes = list(filter(lambda v: v is not None, test_indexes))

    # make a function to remove invalid items from a list
    def valid_list(raw_list):
        def check_valid_index(enum):
            idx, val = enum
            return True if idx in valid_indexes else False
        valid_enums = filter(check_valid_index, enumerate(raw_list))
        return [e[1] for e in valid_enums]

    # open a file for writing
    import ipdb; ipdb.set_trace()
    with open(file_name, 'w', newline='') as csvfile:
        dlm_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        dlm_writer.writerow(valid_list(columns))
        [dlm_writer.writerow(valid_list(row)) for row in data_iter]
