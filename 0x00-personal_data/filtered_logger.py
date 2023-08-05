#!/usr/bin/env python3
""" filtered_logger.py """
import re
from typing import List
import logging
import csv


PII_FIELDS = ('name', 'email', 'phone', 'address', 'ssn')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str
                 ) -> str:
    """ a function that returns the log message obfuscated."""
    pattern = fr'\b({"|".join(fields)})=([^{separator}]+)'
    return re.sub(pattern, fr'\1={redaction}', message)


def get_logger() -> logging.Logger:
    """ a function that takes no argument and returns
    logging.Logger object """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    redacting_formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(redacting_formatter)
    logger.addHandler(stream_handler)

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initialize the class """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ method to filter values in incoming log records
        using filter_datum """
        record.msg = filter_datum(self.fields,
                                  self.REDACTION,
                                  record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
