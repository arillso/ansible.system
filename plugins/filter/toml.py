# -*- coding: utf-8 -*-

"""
Ansible Filter Plugin for TOML conversion.

This module provides filters for converting between TOML strings and Python objects,
with support for Python versions before and after 3.11.
"""

from __future__ import absolute_import, division, print_function

import sys
from datetime import datetime

# pylint: disable=import-error
from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_text
from ansible.module_utils.common._collections_compat import Mapping

# Importing libraries for reading and writing TOML
TOMLLIB_IMPORT_ERROR = None
TOMLW_IMPORT_ERROR = None

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError as exc:
        tomllib = None
        TOMLLIB_IMPORT_ERROR = 'The Python library "tomli" is required for reading TOML.'

try:
    import tomli_w as tomlw
except ImportError:
    try:
        # pylint: disable=import-self
        import toml as tomlw
    except ImportError as exc:
        tomlw = None
        TOMLW_IMPORT_ERROR = 'A Python library for writing TOML is required ("tomli-w" or "toml").'


def from_toml(toml_string):
    """
    Converts a TOML-formatted string into a Python dictionary.

    :param toml_string: The TOML string to parse.
    :type toml_string: str
    :return: The Python dictionary generated from the TOML string.
    :rtype: dict
    :raises AnsibleFilterError: If the input string is not a valid TOML string or another
        error occurs.
    """
    if TOMLLIB_IMPORT_ERROR:
        raise AnsibleFilterError(TOMLLIB_IMPORT_ERROR)
    if not isinstance(toml_string, str):
        raise AnsibleFilterError(
            f"from_toml requires a string, received: {type(toml_string).__name__}"
        )
    try:
        return tomllib.loads(toml_string)
    except Exception as e:
        raise AnsibleFilterError(f"Error parsing TOML: {e}") from e


def to_toml(data):
    """
    Converts a Python dictionary into a TOML-formatted string.

    :param data: The Python dictionary to convert.
    :type data: Mapping
    :return: A string in TOML format.
    :rtype: str
    :raises AnsibleFilterError: If the object cannot be converted or another error occurs.
    """
    if TOMLW_IMPORT_ERROR:
        raise AnsibleFilterError(TOMLW_IMPORT_ERROR)
    if not isinstance(data, Mapping):
        raise AnsibleFilterError(
            f"to_toml requires a dict, received: {type(data).__name__}"
        )
    try:
        return to_text(tomlw.dumps(data), errors="surrogate_or_strict")
    except Exception as e:
        raise AnsibleFilterError(f"Error generating TOML: {e}") from e


def to_nice_toml(data):
    """
    Convert a Python dictionary to a nicely formatted TOML string.

    This function formats a Python dictionary into a TOML string, taking special care to handle
    nested dictionaries and arrays of dictionaries. It ensures proper indentation and formatting
    to produce a readable TOML representation of the input dictionary.

    :param data: The Python dictionary to convert.
    :type data: Mapping
    :return: A nicely formatted TOML string representing the input dictionary.
    :rtype: str
    :raises AnsibleFilterError: If the object cannot be converted or another error occurs.
    """
    if TOMLW_IMPORT_ERROR:
        raise AnsibleFilterError(TOMLW_IMPORT_ERROR)
    if not isinstance(data, Mapping):
        raise AnsibleFilterError(
            f"to_nice_toml requires a dict, received: {type(data).__name__}"
        )

    def format_toml_value(value):
        """
        Format a Python value into a TOML-friendly string representation, ensuring
        date-time values are correctly formatted as YYYY-MM-DDTHH:MM:SSZ.
        """
        if isinstance(value, str):
            # Check if the value is a date-time string in ISO format.
            try:
                # Attempt to parse the string as a datetime object.
                parsed_datetime = datetime.fromisoformat(value.rstrip("Z"))
                # Reformat to the specific desired format with 'Z'.
                return parsed_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                # If parsing fails, return the value as a regular string.
                return f'"{value}"'
        elif isinstance(value, datetime):
            # Format datetime objects directly.
            return value.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            # Ensure that each item in the list is correctly formatted.
            return "[" + ", ".join(map(format_toml_value, value)) + "]"
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    def recurse(data, indent=0, parent_key=""):
        """
        Recursively traverses the data structure, formatting it into a TOML string.

        This helper function handles the recursion needed for nested dictionaries
        and arrays of dictionaries,ensuring proper TOML structure and indentation.
        """
        toml_str = ""
        for key, value in data.items():
            # Construct the full key path for nested dictionaries
            full_key = f"{parent_key}.{key}" if parent_key else key

            if isinstance(value, dict):
                # For nested dictionaries, add a section header
                if indent <= 0:  # Not for the top-level
                    toml_str += "\n"
                prefixed_key = full_key if parent_key else key
                toml_str += "  " * indent + f"[{prefixed_key}]\n"
                toml_str += recurse(value, indent + 1, full_key)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # For arrays of dictionaries, add array of tables header
                for item in value:
                    toml_str += "\n" + "  " * indent + f"[[{full_key}]]\n"
                    toml_str += recurse(item, indent + 1, full_key)
            else:
                # Simple key-value pairs
                toml_str += "  " * indent + f"{key} = {format_toml_value(value)}\n"
        return toml_str

    try:
        return recurse(data)
    except Exception as e:
        raise AnsibleFilterError(f"Error generating nice TOML: {e}") from e


# pylint: disable=R0903
class FilterModule:
    """
    Ansible Filter Module for converting between TOML and Python objects.

    Provides three filters:
    - from_toml: Converts TOML strings to Python dictionaries.
    - to_toml: Converts Python dictionaries to TOML strings.
    - to_nice_toml: Converts Python dictionaries to nicely formatted TOML strings.

    Requirements:
    - Python 3.11+ (uses built-in tomllib) OR tomli package for reading TOML
    - tomli-w package (or toml as fallback) for writing TOML
    """

    def filters(self):
        """
        Defines the filters provided by this module.

        :return: A dictionary of filter names to filter functions.
        :rtype: dict
        """
        return {
            "from_toml": from_toml,
            "to_toml": to_toml,
            "to_nice_toml": to_nice_toml,
        }
