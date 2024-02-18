#!/usr/bin/python3
# Copyright: (c) 2024, Arillso
#
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# License available at https://opensource.org/licenses/MIT
"""
Ansible module to retrieve a list of updatable packages on an APT-based system.
This module fetches and lists all packages that are available for update,
providing current and available versions for each package.
"""

# pylint: disable=import-error
import apt
import apt.progress.text
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: arillso.system.apt_update_info
version_added: "0.0.1"
short_description: Retrieves a list of updatable packages.
description:
    - This module fetches a list of all packages on an APT-based system that are available for update.
    - It's intended to be used within an Ansible environment.
    - Upon execution, it returns a detailed list of packages with information on current and available versions,
      aiding in the assessment of pending updates.
author: "arillso (@arillso) <hello@arillso.io>"
"""


def main():
    """
    Main function to retrieve updatable packages information.
    """
    result = {"changed": False, "packages": []}
    module = AnsibleModule(argument_spec={}, supports_check_mode=True)

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
