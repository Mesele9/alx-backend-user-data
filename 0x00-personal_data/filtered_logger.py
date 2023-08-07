#!/usr/bin/env python3
""" filtered_logger.py """
import re
from typing import List
import logging
import csv
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'password', 'ssn')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str
                 ) -> str:
    """ a function that returns the log message obfuscated."""
    pattern = fr'\b({"|".join(fields)})=([^{separator}]+)'
    return re.sub(pattern, fr'\1={redaction}', message)


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ a function that returns a connector to a database """
    return mysql.connector.connect(
        host=os.environ('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.environ('PERSONAL_DATA_DB_NAME', ''),
        user=os.environ('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.environ('PERSONAL_DATA_DB_PASSWORD', ''),
        port=3306,
    )


def main():
    """create a database connection using function get_db """            
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    sql_logger = get_logger()
    retrieved_data = []
    for row in cursor:
        message = f'name={row[0]}; email={row[1]}; phone={row[2]}; ' \
                  f'ssn={row[3]}; password={row[4]}; ip={row[5]}; ' \
                  f'last_login={row[6]}; user_agent={row[7]};'
        retrieved_data.append(filter_datum(PII_FIELDS, '***', message, '; '))
    for datum in retrieved_data:
        sql_logger.info(datum)
    cursor.close()
