# utilities.py
import argparse
from datetime import datetime


def date_fromisoformat(date_string):
    '''Return a `datetime.date` corresponding to a string in YYYY-MM-DD format.

    :param date_string: A date in the format YYYY-MM-DD.
    :return: A `datetime.date` correspondingo the given date string.
    '''
    try:
        return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{date_string}' is not a valid date. Use YYYY-MM-DD HH:MM:SS.")

def str_to_datetime(date_string):
    '''Convert a calendar date/time description into a datetime object.

    :param date_string: A calendar date in YYYY-MM-DD hh:mm:ss format.
    :return: A naive `datetime` corresponding to the given calendar date and time.
    '''
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")


def datetime_to_str(dt):
    '''Convert a naive Python datetime into a human-readable string.

    :param dt: A naive Python datetime.
    :return: That datetime, as a human-readable string.
    '''
    return datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")