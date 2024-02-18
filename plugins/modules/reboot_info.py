#!/usr/bin/python3
# Copyright: (c) 2024, Arillso
#
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# License available at https://opensource.org/licenses/MIT
"""
Ansible module for checking if the system requires a reboot.

This module assesses the system state to determine if a reboot is required,
typically useful after applying package updates or system changes that necessitate a restart.
"""

# pylint: disable=import-error
import os

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: arillso.system.reboot_info
version_added: '0.0.2'
short_description: Checks if the system requires a reboot.
description:
  - This module checks if a system requires a reboot, typically after package updates.
author:
  - arillso (@arillso) <hello@arillso.io>
"""


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
