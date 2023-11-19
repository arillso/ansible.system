# arillso.system.apt_keys

This Ansible role is designed for managing APT keys on a system. It utilizes the `ansible.builtin.apt_key` module
to add or remove APT keys as specified in the role's configuration.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Access**: Adequate permissions to manage APT keys on target systems

## Role Variables

Variables for managing APT keys are defined in `defaults/main.yml`. Users can override these in their playbook. Key variables include:

### APT Keys Configuration

- `apt_keys_list`: A list of dictionaries specifying APT keys to manage. Each dictionary should contain:
  - `id`: The ID of the APT key.
  - `url`: The URL from where the APT key can be downloaded.
  - `state`: Optional. The state of the APT key (can be 'present' or 'absent'). If not specified, `apt_keys_state` will be used (default: 'present').

- `apt_keys_state`: The default state of APT keys if not specified in each key dictionary. Can be 'present' or 'absent' (default: 'present').

## Documentation

For detailed information and advanced usage, please refer to our guide:

[Arillso System Guide](https://guide.arillso.io/collections/arillso/system/apt_keys.html#ansible-collections-arillso-system-apt-keys-role)

## Dependencies

This role is standalone and does not require other Ansible roles as dependencies.

## Example Playbook

Example playbook for using `arillso.system.apt_keys`:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.system.apt_keys
  vars:
    apt_keys_list:
      - id: 'E0C56BD4'
        url: 'http://keyserver.ubuntu.com:80'
        state: 'present'
    apt_keys_state: 'present'
```
