# Scripts for researching ICE detainees in Tulsa

The [Tulsa County Inmate Information Center](http://iic.tulsacounty.org/expInmateBookings/BookingIndex) website provides a page to scroll through a list of inmates.  The dlm-inmates script retrieves all pages and also looks up inmate details.  Inmates with an ICE hold are denoted by the 'TLS' number in their record.

## Files
* __dlm-inmates.py__: python script for saving iic.tulsacounty.org info to a csv
* __settings.py__: details of the tulsacounty url
* __\_helpers.py__: utilities for cleaning text

## Set up
1. Create a Python 3.6.5 virtual env
1. Clone this repo
1. 'cd ice-hold'
1. 'mkdir data' (this is ignored)
1. 'pip install -r requirements.txt'

## Usage

1. 'python dlm-inmates.py'
1. creates a csv file in data/ called dlm_inmates.csv
