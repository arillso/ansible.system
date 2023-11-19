# arillso.system.apt_packages

This Ansible role is designed for managing APT packages on a system. It enables the installation, update, and removal
of APT packages using the `ansible.builtin.apt` module.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Access**: Adequate permissions to manage APT packages on target systems

## Role Variables

Variables for managing APT packages are defined in `defaults/main.yml`. Users can override these in their playbook. Key variables include:

### APT Packages Configuration

- `apt_packages_list`: A list of APT packages to manage. Each entry can be a package name or a dictionary with additional options such as
 version, install recommends, allow downgrade, purge, force apt-get, lock timeout, and state.

- `apt_packages_install_recommends`: Default value for installing recommended packages along with the main package (default: true).

- `apt_packages_allow_downgrade`: Default value for allowing package downgrades (default: false).

- `apt_packages_purge`: Default value for purging packages (default: false).

- `apt_packages_force_apt_get`: Default value for forcing the use of apt-get instead of apt (default: false).

- `apt_packages_lock_timeout`: Default value for the lock timeout when installing packages (default: 30 seconds).

- `apt_packages_state`: Default state of APT packages if not specified in each package dictionary (default: 'present').

## Documentation

For detailed information and advanced usage, please refer to our guide:

[Arillso System Guide](https://guide.arillso.io/collections/arillso/system/apt_packages.html#ansible-collections-arillso-system-apt-packages-role)

## Dependencies

This role is standalone and does not require other Ansible roles as dependencies.

## Example Playbook

Example playbook for using `arillso.system.apt_packages`:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.system.apt_packages
  vars:
    apt_packages_list:
      - name: 'vim'
        state: 'latest'
      - name: 'curl'
        install_recommends: false
    apt_packages_state: 'present'
```
