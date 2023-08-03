#!/usr/bin/env python3
""" filtered_logger.py """
import re


def filter_datum(fields, redaction, message, separator):
    """ a function that returns the log message obfuscated."""
    pattern = fr'\b({"|".join(fields)})=([^{separator}]+)'
    return re.sub(pattern, fr'\1={redaction}', message)
