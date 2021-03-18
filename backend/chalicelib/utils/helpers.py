from datetime import datetime
from typing import Any, Optional

import arrow


def standardize_timestamp(val: Any) -> Optional[str]:
    """
    This helper function standardizes a value to
    an ISO 8601 formatted representation of the date and time.

    :param val: Any Arrow object compatible inputs
    :return: An ISO 8601 formatted representation of the date and time.
    """

    if val:
        return arrow.get(val).isoformat()

    return None


def get_current_timestamp() -> str:
    """
    This helper function gets an ISO 8601 formatted representation of “now” in UTC time.

    :return: A ISO 8601 formatted representation of “now” in UTC time.
    """

    return arrow.utcnow().isoformat()


def get_datetime_timestamp(val: Any) -> Optional[datetime]:
    """
    This helper function converts a value to
    a datetime representation.

    :param val: Any Arrow object compatible inputs
    :return: A datetime representation:
    """

    if val:
        return arrow.get(val).datetime

    return None


def get_millisecond_timestamp(val: Any) -> Optional[int]:
    """
    This helper function converts a value to
    a rounded millisecond-integer timestamp representation in UTC time.

    :param val: Any Arrow object compatible inputs
    :return: A millisecond-integer timestamp representation in UTC time or None.
    """

    if val:
        round(arrow.get(val).float_timestamp * 1000)

    return None
