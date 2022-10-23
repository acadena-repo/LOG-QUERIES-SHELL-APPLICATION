# rw_handler.py
'''Functions to handle read/write operations into files'''
#import sys
#sys.path.append("..")

import csv
from pathlib import Path
from ..model.models import LogRecord
from ..support.utilities import str_to_datetime, datetime_to_str

def log_parser(log_record: str):
    '''parse and split log record into its sections.

    :param log_record: Representation of a single line in the log file.
    :return: A dictionary with the relevant sections of a logged event.
    '''
    record = {}
    data = log_record.split(',')
    message = data[1].split(':')
    
    if len(message) > 2:
        record['logtime'] = str_to_datetime(data[0].strip())
        record['severity'] = message[1].split('-')[0].strip()
        
        if len(message) > 3:
            record['description'] = message[2].strip()
            record['code'] = message[4].strip()
        else:
            record['description'] = message[2].strip() + data[2].split(':')[0].rstrip()
            record['code'] = data[2].split(':')[-1].strip()
        
        return record
    else:
        return False


def load_log(path: Path):
    '''Load the events from a file and return a collection of records.
    
    :param path: A path where the log file is located.
    :return: A list with log records objects.
    '''
    records = []

    with open(path, 'r') as log_file:
        lines = log_file.readlines()

    for line in lines:
        record = log_parser(line)
        if record:
            records.append(LogRecord(**record))

    return records


def write_to_csv(results, outfile: str):
    '''Write an iterable of `LogRecord` objects to a CSV file.

    :param results: An iterable of `LogRecord` objects.
    :param outfile: A path-like object pointing to where the data should be saved.
    '''
    fieldnames = ('time stamp', 'severity', 'code', 'description')

    with open(outfile, 'w', newline='') as file:
        writter = csv.DictWriter(file, fieldnames=fieldnames)
        writter.writeheader()
        
        for event in results:
            writter.writerow({'time stamp':datetime_to_str(event.logtime),
                              'severity':event.severity,
                              'code':event.code,
                              'description':event.description
                             })