import csv

from ._helpers import make_filter

# function for saving a csv files
# file_name: you know this one ...
# columns:  a list of strings for column titles
# data_rows: an iter that provides list of values
def save_csv(file_name, data_iter):
    # assumes the first row is column titles
    columns = next(data_iter)
    column_filter = make_filter(columns)

    # open a file for writing
    with open(file_name, 'w', newline='') as csvfile:
        dlm_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        dlm_writer.writerow(column_filter(columns))
        [dlm_writer.writerow(column_filter(row)) for row in data_iter]
