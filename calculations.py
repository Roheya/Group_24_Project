#!/usr/bin/python3
""" calculations.py member 3 
requirements 04, 05, 06."""

PADS_PER_YEAR = 240 #estimated considering 4 pads per day * 5 days * 12 months


class MissingDataError(ValueError):
    """Raised when a value needed for the calculations is missing or invalid"""


def validate_number(value, field, allow_zero=True):
    #validate the value and return it as a float
    if value is None or value == "":
        raise MissingDataError(f"Missing value for '{field}'.")
    try:
        number =float(value)
    except (TypeError, ValueError):
        raise MissingDataError(f"'{field}' must be a number")
    if number < 0:
        raise MissingDataError(f"{number}, '{field}' cannot be negative")
    if not allow_zero and number == 0:
        raise MissingDataError(f" '{field}' cannot be zero.")
    return number

def girls_affected(school_aged_girls):
    """the number of girls affected = number of girls in period poverty"""
    return int(validate_number(shool_aged_girls, "school_aged_girls"))

def days_lost(school_aged_girls, days_missed):
    #return the days lost yearly by the school, estimating the days missed by the girls around 5 days per month.
    girls = validate_number(school_aged_girls, "school_aged_girls")
    days_missed = validate_number(days_missed, "days_missed")
    return round(girls * missed, 1)
