# models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogRecord:
    logtime: datetime
    severity: str
    description: str
    code: str

    def __str__(self):
        '''Returns `str(self)`'''
        rep = f'{datetime.strftime(self.logtime, "%Y-%m-%d %H:%M:%S")} - validation code: {self.code} - with level [{self.severity}]\n' \
              f'{self.description}'

        return rep