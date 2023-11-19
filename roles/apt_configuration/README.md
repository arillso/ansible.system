# arillso.system.apt_configuration

This Ansible role is designed for managing Advanced Package Tool (APT) configurations on Debian and Ubuntu systems.
It provides flexibility in configuring APT settings at both host and group levels, as well as detailed configurations for various APT aspects.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Access**: Adequate permissions to manage APT configurations on target systems

## Role Variables

Variables for managing APT configurations are defined in `defaults/main.yml`. Users can override these in their playbook. Key variables include:

### Host and Group Specific Configurations

- `apt_configuration_host_list`: A list of host-specific APT configurations. Each entry can customize APT settings for a particular host.
- `apt_configuration_group_list`: A list of group-specific APT configurations. Useful for applying settings across a group of hosts.

### General APT Configurations

- `apt_configuration_list`: A main list of APT configurations, each with a filename and specific configuration content. Examples include:
  - Auto-removal settings for specific packages and kernel packages.
  - Automatic update and upgrade configurations.
  - Settings for the `apt-listchanges` tool.
  - Configurations for unattended upgrade behaviors.
  - Archive handling settings.
  - General APT configuration settings such as `Install-Recommends`, `AutoRemove`, and `Install-Suggests`.

## Documentation

For detailed information and advanced usage, please refer to our guide:

[Arillso System Guide](https://guide.arillso.io/collections/arillso/system/apt_configuration.html#ansible-collections-arillso-system-apt-configuration-role)

## Dependencies

This role is standalone and does not require other Ansible roles as dependencies.

## Example Playbook

Example playbook for using `arillso.system.apt_configuration`:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.system.apt_configuration
  vars:
    apt_configuration_list:
      - filename: "01autoremove"
        config:
          APT:
            NeverAutoRemove:
              - "^firmware-linux.*"
            # ... other configurations ...
```
