# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Arillso
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Lookup plugin for Ansible to curate a list of files based on specific patterns.
This module takes a list of files and patterns, compares them,
and returns a curated list of files that match the patterns.
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
    name: environment_files
    author: arillso (@arillso)
    short_description: returns a curated files list
    description:
      - Takes a files list and returns it curated.
    options:
      _terms:
        description:
          - First item is the list of files, second is the patterns dict.
        required: true
"""

EXAMPLES = """
# Example usage in a playbook
- name: Curate files based on patterns
  debug:
    msg: "{{ lookup('arillso.system.environment_files', files_list, patterns_dict) }}"
"""

RETURN = """
  _list:
    description: A curated list of files matching the patterns.
    type: list
    elements: dict
"""

from ansible.errors import AnsibleError  # noqa: E402
from ansible.plugins.lookup import LookupBase  # noqa: E402

try:
    # Python 2
    string_types = (str, unicode)  # type: ignore  # noqa: F821
except NameError:
    # Python 3
    string_types = (str,)


class LookupModule(LookupBase):  # pylint: disable=too-few-public-methods
    """Lookup module for curating a files list based on provided patterns."""

    def run(self, terms, variables=None, **_kwargs):  # pylint: disable=unused-argument
        """Executes the lookup.

        Args:
            terms (list): First item is the list of files, second is the patterns dict.
            variables (dict, optional): Variables passed to the lookup plugin.
            **_kwargs: Arbitrary keyword arguments (unused).

        Returns:
            list: A curated list of files.
        """
        results = []

        files = self._flatten(terms[0])
        patterns = terms[1]

        item_default = {"export": False}

        for file in files:
            items = []

            # Short syntax
            if isinstance(file, string_types):
                if file not in patterns:
                    raise AnsibleError(f'"{file}" is not a valid pattern')

                item = item_default.copy()
                item.update(patterns.get(file))
                items.append(item)
            else:
                # Must be a dict
                if not isinstance(file, dict):
                    raise AnsibleError(
                        f"Expected a dict but was a {type(file).__name__}"
                    )

                # Check index key
                if "file" not in file:
                    raise AnsibleError('Missing "file" key')

                item = item_default.copy()
                item.update(file)
                items.append(item)

            # Merge by index key
            for item in items:
                item_found = False
                for i, result in enumerate(results):
                    if result["file"] == item["file"]:
                        results[i] = item
                        item_found = True
                        break
                if not item_found:
                    results.append(item)

        return results
