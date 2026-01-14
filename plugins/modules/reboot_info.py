#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Arillso
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Ansible module for checking if the system requires a reboot.

This module assesses the system state to determine if a reboot is required,
typically useful after applying package updates or system changes that necessitate a restart.
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: reboot_info
version_added: '0.0.2'
short_description: Checks if the system requires a reboot.
description:
  - This module checks if a system requires a reboot, typically after package updates.
author:
  - arillso (@arillso) <hello@arillso.io>
"""

EXAMPLES = r"""
- name: Check if system requires reboot
  arillso.system.reboot_info:
  register: reboot_status

- name: Display reboot requirement
  debug:
    msg: "System reboot required: {{ reboot_status.reboot }}"

- name: Reboot system if needed
  reboot:
  when: reboot_status.reboot
"""

RETURN = r"""
reboot:
    description: Whether the system requires a reboot
    returned: always
    type: bool
"""

# pylint: disable=import-error
import os  # noqa: E402

from ansible.module_utils.basic import AnsibleModule  # noqa: E402


def main():
    """
    Main function for the Ansible Module. It checks if a reboot is required on the system.
    """
    result = {"changed": False, "reboot": False}
    module = AnsibleModule(argument_spec={}, supports_check_mode=True)

    # Check for the presence of the file indicating a reboot is required.
    reboot_required_path = "/var/run/reboot-required"
    if os.path.isfile(reboot_required_path):
        result["reboot"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
