# Ansible Collection: arillso.system

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=popout-square)](licence) [![Ansible Galaxy](http://img.shields.io/badge/ansible--galaxy-arillso.system-blue.svg?style=popout-square)](https://galaxy.ansible.com/arillso/system)

## Description

This is an Ansible collection that installs and then configures various system.

## Roles

- [apt_cache](roles/apt_cache/README.md)
- [apt_keys](roles/apt_keys/README.md)
- [apt_packages](roles/apt_packages/README.md)
- [apt_repositories](roles/apt_repositories/README.md)
- [logrotate](roles/logrotate/README.md)
- [maintenance](roles/maintenance/README.md)
- [netplan](roles/netplan/README.md)
- [packages](roles/packages/README.md)
- [reboot](roles/reboot/README.md)
- [resolv](roles/resolv/README.md)
- [ssh](roles/ssh/README.md)
- [sudoers](roles/sudoers/README.md)
- [sysctl](roles/sysctl/README.md)
- [systemd_service](roles/systemd_service/README.md)
- [systemd_unit](roles/systemd_unit/README.md)

## Plugins

plugins/lookup:

- github_latest_release.py

plugins/modules:

- apt_update_info.py
- reboot_info.py

## License

<!-- markdownlint-disable -->

This project is under the MIT License. See the [LICENSE](licence) file for the full license text.

<!-- markdownlint-enable -->

## Copyright

(c) 2022, Arillso
