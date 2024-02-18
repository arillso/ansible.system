# arillso.system.motd

This Ansible role module is designed to manage the Message of the Day (MOTD) configuration, including the creation, modification, and deletion of MOTD content on your systems.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Access Rights**: Sufficient permissions to manage the MOTD configuration on target systems

## Role Variables

Variables defined in `defaults/main.yml` customize the MOTD configuration. These can be overridden in your playbook. Key variables include:

### MOTD Configuration

- `motd_header`: The header text for the MOTD script. By default, an ASCII art header is set.
- `motd_fqdn`: The Fully Qualified Domain Name of the host.
- `motd_distribution`: The name of the Operating System distribution.
- `motd_distribution_version`: The version of the Operating System distribution.
- `motd_distribution_release`: The release name of the distribution.
- `motd_virtualization_role`: Role in virtualization (host/guest/none).
- `motd_virtualization_type`: Type of virtualization (KVM, VirtualBox, etc.).
- `motd_date_time`: Date and time information.
- `motd_region`: Regional variable.
- `motd_zone`: Zone variable.
- `motd_customer`: Customer variable.
- `motd_projects`: Projects variable (list).
- `motd_project`: Single project variable.
- `motd_exclude_disk_space`: List of filesystem types to exclude in disk space check.

## Dependencies

This role is standalone and does not require other Ansible roles as dependencies.

## Documentation

For detailed information and advanced usage, please refer to our guide:

[Arillso System Guide](https://guide.arillso.io/collections/arillso/system/motd_role.html#ansible-collections-arillso-system-motd-role)

## Example Playbook

An example playbook for using `arillso.system.motd`:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.system.motd
  vars:
    motd_header: "Custom MOTD Header"
    motd_fqdn: "example.com"
    motd_distribution: "Ubuntu"
    motd_distribution_version: "20.04"
    motd_virtualization_type: "KVM"
    motd_date_time:
      year
```
