# Scripts for researching ICE detainees in Tulsa

The [Tulsa County Inmate Information Center](http://iic.tulsacounty.org/expInmateBookings/BookingIndex) website provides a page to scroll through a list of inmates.  The dlm-inmates script retrieves all pages and also looks up inmate details.  Inmates with an ICE hold are denoted by the 'TLS' number in their record.

The City Of Tulsa Jail Hub has information about inmates at the [Tulsa City Jail](https://www.cityoftulsa.org/apps/inmateinformationcenter/) for the past 90 days.

The CSV files created by these scripts includes a column to identify inmates on an ICE hold.  The dlm-inmates file uses **'TLS'** and includes a TLS record number.  The tulsa_city_inmates file uses **'hold'** and shows the last hold instructions on the inmates charges list.

## Files
* __dlm-inmates.py__: python script for saving iic.tulsacounty.org info to a csv
* __tulsa-jail.py__: python script for saving www.cityoftulsa.org information
* __settings.py__: details of the tulsacounty url
* __\_helpers.py__: utilities for cleaning text

## Set up
1. Create a Python 3.6.5 virtual env
1. Clone this repo
1. 'cd ice-hold'
1. 'mkdir data' (this is ignored)
1. 'pip install -r requirements.txt'

## Usage

### David L Moss Inmates:
* 'python dlm-inmates.py'
* creates a csv file in data/ called dlm_inmates.csv

### City of Tulsa Jail:
* 'python tulsa-jail.py'
* creates a csv file in data/ called tulsa_city_inmates.csv
