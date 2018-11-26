import re
import csv
import json
import requests

from settings import TULSA_JAIL_AJAX as BOOKINGS_URL
from settings import AJAX_HEADERS as HEADERS
from _helpers import dict_values

with requests.Session() as iic_session:

    def get_aspx_payload(script_name, **kwargs):
        response = iic_session.post(
            f'{BOOKINGS_URL}/{script_name}.aspx/ServiceReference',
            data={},
            headers=HEADERS,
            params=kwargs['params']
            )
        payload = json.loads(response.json()['d']['ReturnCode'])
        return payload

    def get_hold_information(details_param):
        hold_info_from = lambda item: True if item['hold'] else False

        # the chages list includes a hold element
        charges = get_aspx_payload('Incident', params=details_param)
        charges_with_holds = filter(hold_info_from, charges)
        hold_instructions = list(map(lambda c: c['hold'], charges_with_holds))

        # return last hold othewise empty str
        # The '[::-1][0]' reverse sorts the list and returns the first item
        return hold_instructions[::-1][0] if len(hold_instructions) > 0 else ''

    def get_inmate_details(params):
        # this function collects header and value information
        # in lists call 'detail_header' and 'detail_values'

        # get Inmate details
        inmate = get_aspx_payload('InmateInfo', params=params)
        detail_header = [k for k in inmate.keys()]
        detail_values = dict_values(inmate)

        # look up hold information
        detail_header.append('hold')
        hold_text = get_hold_information(params)
        detail_values.append(hold_text)

        return(detail_header, detail_values)

    def get_inmate_list():
        print('POSTing request for all inmates in the past 90 days')

        id_params = lambda inmate: {'dataId': inmate['IncidentRecordID']}

        all_inmates_list = get_aspx_payload('CompleteInmates', params='')

        # use first inmate dict keys as column headers
        inmates = iter(all_inmates_list)
        first_inmate = next(inmates)
        first_inmate_values = dict_values(first_inmate)

        # get details header from first inmate
        (first_details_header, first_inmate_details) = (
            get_inmate_details(id_params(first_inmate))
            )
        headers = (
            [k for k in first_inmate.keys()] + first_details_header
            )
        #  start a list of rows with the first inmate values
        inmate_rows = []
        inmate_rows.append(first_inmate_values + first_inmate_details)

        # get the details on the remaining inmates
        for inmate in inmates:
            (detail_header, detail_values) = (
                get_inmate_details(id_params(inmate))
                )
            inmate_rows.append(dict_values(inmate) + detail_values)

        # return a list of column headers and a list of table rows
        return (headers, inmate_rows)

    with open('data/tulsa_city_inmates.csv', 'w', newline='') as csvfile:
        columns, inmates = get_inmate_list()
        dlm_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        dlm_writer.writerow(columns)
        [dlm_writer.writerow(inmate) for inmate in inmates]
