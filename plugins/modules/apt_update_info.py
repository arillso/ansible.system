#!/usr/bin/python3
# Copyright: (c) 2022, Arillso
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import apt
import apt.debfile

__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: arillso.system.apt_update_info
version_added: '0.0.1'
short_description: List all packages to be updated.
author:
- Simon Bärlocher (@sbaerlocher)
"""


def main():
    result = dict(changed=False, packages=[])
    module = AnsibleModule(argument_spec=dict(), supports_check_mode=True)

    packages = []

    cache = apt.Cache()
    cache.update()
    cache.upgrade()
    for pkg in sorted(cache.get_changes()):
        pkg_versions = pkg.versions
        if cache[pkg.name].is_installed:
            for pkg_version in pkg_versions:
                if pkg_version.is_installed:
                    pkg_new = {
                        "package": pkg.name,
                        "current": pkg_version.version,
                        "available": pkg_versions[0].version,
                    }
                    packages.append(pkg_new)

    result["packages"] = packages

    module.exit_json(**result)


if __name__ == "__main__":
    main()
