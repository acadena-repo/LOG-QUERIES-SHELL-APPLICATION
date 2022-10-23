# database.py
from typing import List
from ..model.models import LogRecord

class Database:

    def __init__(self, records: List[LogRecord]):
        self._records = records


    def get_head(self, number: int):
        head = number
        return self._records[:head]

    def get_tail(self, number: int):
        tail = int(-1*number)
        return self._records[tail:]

    def query(self, filters=()):
        if len(filters) > 0:
            checker = filters.pop(0)
            results = filter(checker, self._records)

            for checker in filters:
                results = filter(checker, results)

            return results
        else:
            return []
