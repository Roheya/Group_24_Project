#!/usr/bin/python3
""" calculations.py member 3 
requirements 04, 05, 06."""

PADS_PER_YEAR = 240 #estimated considering 4 pads per day * 5 days * 12 months


class MissingDataError(ValueError):
    """Raised when a value needed for the calculations is missing or invalid"""


def validate_number(value, field, allow_zero=True):
    #validate the value and return it as a float

