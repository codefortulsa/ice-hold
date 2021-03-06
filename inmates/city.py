import sys
import json
import requests

from .settings import TULSA_JAIL_AJAX as BOOKINGS_URL
from .settings import AJAX_HEADERS as HEADERS
from ._helpers import dict_values

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

    def get_charge_information(details_param):
        def hold_info_from(item):
            return True if item['hold'] else False

        charge_details = {'firstCharge': '', 'hold': ''}
        charges = get_aspx_payload('Incident', params=details_param)
        charge_details['firstCharge'] = (
            charges[0]['crime'] if len(charges) > 0 else '')
        # the charges list includes a hold element
        charges_with_holds = filter(hold_info_from, charges)
        hold_instructions = list(map(lambda c: c['hold'], charges_with_holds))
        charge_details['hold'] = (
            hold_instructions[-1] if len(hold_instructions) > 0 else '')
        # return last hold othewise empty str
        return charge_details

    def get_inmate_details(params):
        # this function collects header and value information
        # in lists call 'detail_header' and 'detail_values'

        # get Inmate details
        inmate = get_aspx_payload('InmateInfo', params=params)
        detail_header = list(inmate.keys())
        detail_values = dict_values(inmate)

        # look up hold information
        charge_info = get_charge_information(params)
        detail_header += [k for k in charge_info.keys()]
        detail_values += dict_values(charge_info)
        return(detail_header, detail_values)

    def inmate_generator():
        print('requesting for city inmates in the past 90 days')

        def id_params(inmate):
            return {'dataId': inmate['IncidentRecordID']}

        all_inmates_list = get_aspx_payload('CompleteInmates', params='')

        # use first inmate dict keys as column headers
        inmates = iter(all_inmates_list)
        first_inmate = next(inmates)
        first_inmate_headers = list(first_inmate.keys())
        first_inmate_values = dict_values(first_inmate)

        # get details from the first inmate
        first_id = id_params(first_inmate)
        first_detail_header, first_detail_values = get_inmate_details(first_id)
        headers = first_inmate_headers + first_detail_header
        yield headers
        #  start a list of rows with the first inmate values
        first_row = first_inmate_values + first_detail_values
        yield first_row

        # get the details on the remaining inmates
        for inmate in inmates:
            inmate_id = id_params(inmate)
            inmate_booking_values = dict_values(inmate)
            detail_header, detail_values = get_inmate_details(inmate_id)
            inmate_row = inmate_booking_values + detail_values
            sys.stdout.write('cty.')
            sys.stdout.flush()
            yield inmate_row
        print('city inmates complete')
