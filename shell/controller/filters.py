# filters.py

def check_dates(start_date, end_date):
    '''Returns a checker function with user's selection criteria'''

    if start_date and end_date is None:
        def checker_dates(event):
            return event.logtime >= start_date
        return checker_dates
    elif end_date and start_date is None:
        def checker_dates(event):
            return event.logtime <= end_date
        return checker_dates
    elif start_date and end_date:
        def checker_dates(event):
            return event.logtime >= start_date and event.logtime <= end_date
        return checker_dates


def check_severity(severity):
    '''Returns a checker funtion with user's selection criteria'''

    def checker_severity(event):
        return event.severity == severity
    return checker_severity


def check_code(code):
    '''Returns a checker funtion with user's selection criteria'''

    def checker_code(event):
        return event.code == code
    return checker_code


def create_filters(start_date=None, end_date=None,
                   severity=None, code=None):
    '''Create a collection of filters from user-specified criteria.

    :param start_date: A `date` on or after which a matching logged event occurs.
    :param end_date: A `date` on or before which a matching logged event occurs.
    :param severity: A `severity level` which a matching logged event has.
    :param code: An `error code` which a matching logged event has.
    :return: A collection of filters for use with `query`.
    '''
    filters = []

    if start_date or end_date:
        filters.append(check_dates(start_date, end_date))

    if severity:
        filters.append(check_severity(severity))

    if code:
        filters.append(check_code(code))

    return filters


def limit(iterator, number=None):
    '''Produce a limited stream of values from an iterator.
    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    '''
    if number is not None and number > 0:
        for _ in range(number):
            try:
                yield next(iterator)
            except StopIteration:
                return
        return
            
    else:
        yield from iterator