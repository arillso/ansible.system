#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Arillso
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Ansible module to retrieve a list of updatable packages on an APT-based system.
This module fetches and lists all packages that are available for update,
providing current and available versions for each package.
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: apt_update_info
version_added: "0.0.1"
short_description: Retrieves a list of updatable packages.
description:
    - This module fetches a list of all packages on an APT-based system that are available for update.
    - It's intended to be used within an Ansible environment.
    - Upon execution, it returns a detailed list of packages with information on current and available versions,
      aiding in the assessment of pending updates.
author: "arillso (@arillso) <hello@arillso.io>"
"""

EXAMPLES = r"""
- name: Get list of updatable packages
  arillso.system.apt_update_info:
  register: apt_updates

- name: Display updatable packages
  debug:
    var: apt_updates.packages
"""

RETURN = r"""
packages:
    description: List of packages that can be updated
    returned: always
    type: list
    elements: dict
    contains:
        package:
            description: Name of the package
            type: str
            returned: always
        current:
            description: Currently installed version
            type: str
            returned: always
        available:
            description: Available version for update
            type: str
            returned: always
"""

# pylint: disable=import-error
from ansible.module_utils.basic import AnsibleModule  # noqa: E402

try:
    import apt  # noqa: E402
    import apt.progress.text  # noqa: E402
    HAS_APT = True
except ImportError:
    HAS_APT = False


def main():
    """
    Main function to retrieve updatable packages information.
    """
    result = {"changed": False, "packages": []}
    module = AnsibleModule(argument_spec={}, supports_check_mode=True)

    if not HAS_APT:
        module.fail_json(msg="The python-apt package is required for this module")

    try:
        cache = apt.Cache()
        cache.update(fetch_progress=apt.progress.text.AcquireProgress())
        cache.open(None)

        for pkg in cache:
            if pkg.is_upgradable:
                pkg_new = {
                    "package": pkg.name,
                    "current": pkg.installed.version,
                    "available": pkg.candidate.version,
                }
                result["packages"].append(pkg_new)

    except apt.CacheException as e:  # Use a more specific exception if possible
        module.fail_json(msg=f"Failed to fetch update information due to: {e}")
    except Exception as e:  # pylint: disable=broad-except
        module.fail_json(msg=f"An unexpected error occurred: {e}")

    module.exit_json(**result)


if __name__ == "__main__":
    main()
