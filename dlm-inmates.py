import requests
import csv
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from settings import BOOKINGS_URL
from _helpers import text_values


iic_session = requests.Session()

def param_generator():
    pages = range(1, 200)
    for p in pages:
        yield {'grid-page': p}


def get_details_url(el):
    details_href = el.find('b').find('a')['href']
    parsed_url = urlparse(details_href)
    k,v = parsed_url.query.split('=')
    # separate and return the url and params
    return (f'{BOOKINGS_URL}{parsed_url.path}',{k:v})


def get_inmate_details(inmate_row):
    details_url, details_param = get_details_url(inmate_row)
    response = iic_session.get(details_url, params=details_param)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(details_url)
    print(soup)
    import ipdb; ipdb.set_trace()
    return


def get_inmate_list(params):
    response = iic_session.get(f'{BOOKINGS_URL}/expInmateBookings/BookingIndex', params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    inmate_table = soup.find('table', 'table table-striped grid-table')
    thead = inmate_table.find('thead').find_all('th')
    rows = inmate_table.find('tbody').find_all('tr')
    for row in rows:
        details = get_inmate_details(row)

    # return a list of column headers and a list of table rows
    # each row is a list of the values in the row
    return (text_values(thead), [text_values(row.find_all('td')) for row in rows])

# open a file for writing

with open('data/dlm_inmates.csv', 'w', newline='') as csvfile:
    dlm_writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # get started with the first page
    request_params = param_generator()
    (header, inmates) = get_inmate_list(next(request_params))
    dlm_writer.writerow(header)
    print(header)

    while True:
        last_inmates = inmates
        (header, inmates) = get_values(next(request_params))
        if inmates == last_inmates:
            break

        [print (inmate) for inmate in inmates]
        [dlm_writer.writerow(inmate) for inmate in inmates]
