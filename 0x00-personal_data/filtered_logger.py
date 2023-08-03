#!/usr/bin/env python3
""" filtered_logger.py """
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str
                 ) -> str:
    """ a function that returns the log message obfuscated."""
    pattern = fr'\b({"|".join(fields)})=([^{separator}]+)'
    return re.sub(pattern, fr'\1={redaction}', message)
