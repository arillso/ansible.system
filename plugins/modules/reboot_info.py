#!/usr/bin/python3
# Copyright: (c) 2022, Arillso
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import os.path

import distro

__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: arillso.system.reboot_info
version_added: '0.0.1'
short_description: checks if the system has to be restarted.
author:
- Simon Bärlocher (@sbaerlocher)
"""


def main():
    result = dict(changed=False, reboot=False)
    module = AnsibleModule(argument_spec=dict(), supports_check_mode=True)

    if distro.linux_distribution()[0] == "Ubuntu":
        if os.path.isfile("/var/run/reboot-required"):
            result["reboot"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
