import requests
import csv

from bs4 import BeautifulSoup

from settings import BOOKINGS_URL
from _helpers import text_values


def param_generator():
    pages = range(1, 200)
    for p in pages:
        yield {'grid-page': p}

def get_values(params):
    response = requests.get(BOOKINGS_URL, params)
    soup = BeautifulSoup(response.text, 'html.parser')
    inmate_table = soup.find('table', 'table table-striped grid-table')
    thead = inmate_table.find('thead').find_all('th')
    rows = inmate_table.find('tbody').find_all('tr')
    # return a list of column headers and a list of table rows
    # each row is a list of the values in the row
    return (text_values(thead), [text_values(row.find_all('td')) for row in rows])

# open a file for writing

with open('data/dlm_inmates.csv', 'w', newline='') as csvfile:
    dlm_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # get started with the first page
    request_params = param_generator()
    (header, inmates) = get_values(next(request_params))
    dlm_writer.writerow(header)
    print(header)

    while True:
        [print (inmate) for inmate in inmates]
        [dlm_writer.writerow(inmate) for inmate in inmates]
        last_inmates = inmates
        (header, inmates) = get_values(next(request_params))
        if inmates == last_inmates:
            break
