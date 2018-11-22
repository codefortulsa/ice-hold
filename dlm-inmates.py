import re
import csv
import requests
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from settings import BOOKINGS_URL
from _helpers import text_values, clean_string


iic_session = requests.Session()


def param_generator():
    pages = range(1, 200)
    for p in pages:
        yield {'grid-page': p}


def get_details_url(el):
    details_href = el.find('b').find('a')['href']
    parsed_url = urlparse(details_href)
    key, val = parsed_url.query.split('=')
    return (f'{BOOKINGS_URL}{parsed_url.path}', {key: val})


def get_inmate_details(inmate_row):
    # this function collects header and value information
    # in lists call 'detail_header' and 'detail_values'
    # there are records with no details so a default header and
    # no values are returned
    detail_header = []
    detail_values = []

    # get the detail page
    details_url, details_param = get_details_url(inmate_row)
    response = iic_session.get(details_url, params=details_param)
    soup = BeautifulSoup(response.text, 'html.parser')

    arrest_start = soup.find('h4',string=re.compile(r'Arrest Information'))

    if arrest_start:
        arrest_thead = arrest_start.find_next('div','details').find_next('thead')
        arrest_header = text_values(arrest_thead.find_all('th'))
        detail_header = detail_header + arrest_header

        detail_row = arrest_thead.find_next('tbody').find('tr')
        row_values = text_values(detail_row.find_all('td'))
        detail_values = detail_values + row_values

        # This section will find string after a {key_word} and
        # add the values after ':'
        # key words available but not used: Height, Weight, Hair, Eyes
        key_words = ['Race']
        for word in key_words:
            word_element = soup.find(string=re.compile(word))
            if word_element:
                detail_header.append(word)
                word_value =word_element.split(':')[1]
                detail_values.append(clean_string(word_value))

        # look for a TLS record
        tls_element = soup.find(string=re.compile(r'TLS\d*'))
        if tls_element:
            detail_values.append(clean_string(tls_element))
        else:
            detail_values.append('')
        # add TLS even if not found
        detail_header.append('TLS')
    else:
        # this could be wrong, but will only matters if the first inmate
        # on the first page has no arrrest details
        detail_header = ['Arrest Date', 'Arrest Time', 'Arrested By', 'Booking Date', 'Booking Time', 'Release Date', 'Release Time', 'Race', 'TLS']

    return (detail_header, detail_values)


def get_inmate_list(params):
    response = iic_session.get(f'{BOOKINGS_URL}/expInmateBookings/BookingIndex', params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    inmate_table = soup.find('table', 'table table-striped grid-table')
    thead = inmate_table.find('thead').find_all('th')
    rows = inmate_table.find('tbody').find_all('tr')

    inmate_rows = []
    for row in rows:
        (detail_header, detail_values) = get_inmate_details(row)
        inmate_rows.append(text_values(row.find_all('td')) + detail_values)
    headers = text_values(thead) + detail_header
    # return a list of column headers and a list of table rows
    # each row is a list of the values in the row
    return (headers, inmate_rows)

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
        (header, inmates) = get_inmate_list(next(request_params))
        if inmates == last_inmates:
            break

        [print (inmate) for inmate in inmates]
        [dlm_writer.writerow(inmate) for inmate in inmates]
