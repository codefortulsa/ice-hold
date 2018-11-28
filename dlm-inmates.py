import re
import requests
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from settings import DLM_BOOKINGS_URL as BOOKINGS_URL
from _helpers import text_values, clean_string
from save_csv import save_csv


def param_generator():
    for page_num in range(1, 200):
        yield {'grid-page': page_num}


def get_details_url(el):
    details_href = el.find('b').find('a')['href']
    parsed_url = urlparse(details_href)
    key, val = parsed_url.query.split('=')
    return (f'{BOOKINGS_URL}{parsed_url.path}', {key: val})


with requests.Session() as iic_session:

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

        arrest_start = soup.find('h4',
                                 string=re.compile(r'Arrest Information'))

        if arrest_start:
            arrest_thead = arrest_start.find_next(
                'div', 'details').find_next('thead')
            arrest_header = text_values(arrest_thead.find_all('th'))
            detail_header = detail_header + arrest_header

            detail_row = arrest_thead.find_next('tbody').find('tr')
            row_values = text_values(detail_row.find_all('td'))
            detail_values = detail_values + row_values

            # This section will find the string after a '{key_word}: and
            # add the values after ':'
            # key words available but not used: Height, Weight, Hair, Eyes
            key_words = ['Race']
            for word in key_words:
                word_element = soup.find(string=re.compile(word))
                if word_element:
                    detail_header.append(word)
                    word_value = word_element.split(':')[1]
                    detail_values.append(clean_string(word_value))

            # look for a TLS record
            # add TLS even if not found
            detail_header.append('TLS')
            tls_element = soup.find(string=re.compile(r'TLS\d*'))
            if tls_element:
                detail_values.append(clean_string(tls_element))
            else:
                detail_values.append('')
        else:
            # this could be wrong, but will only matters if the first inmate
            # on the first page has no arrrest details
            detail_header = ['Arrest Date',
                             'Arrest Time',
                             'Arrested By',
                             'Booking Date',
                             'Booking Time',
                             'Release Date',
                             'Release Time',
                             'Race',
                             'TLS']

        return (detail_header, detail_values)

    def get_inmate_list(params):
        print("GETting page %s." % params['grid-page'])
        response = iic_session.get(
            f'{BOOKINGS_URL}/expInmateBookings/BookingIndex',
            params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        inmate_table = soup.find('table', 'table table-striped grid-table')
        thead = inmate_table.find('thead').find_all('th')
        inmate_rows = inmate_table.find('tbody').find_all('tr')

        columns_headers = text_values(thead)
        output_rows = []
        for inmate in inmate_rows:
            (detail_header, detail_values) = get_inmate_details(inmate)
            inmate_booking_values = text_values(inmate.find_all('td'))
            output_rows.append(inmate_booking_values + detail_values)
        # return a list of column headers and a list of table rows
        # each row is a list of the values in the row
        columns_headers = columns_headers + detail_header

        return (columns_headers, output_rows)

    def inmate_generator():
        # get started with the first page
        request_params = param_generator()
        (header, inmates) = get_inmate_list(next(request_params))
        yield header
        while True:
            for inmate in inmates:
                yield inmate
            last_inmates = inmates
            (header, inmates) = get_inmate_list(next(request_params))
            if inmates == last_inmates:
                break

    save_csv('data/dlm_inmates.csv', inmate_generator())
