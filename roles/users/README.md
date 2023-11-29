# Ansible Role: arillso.system.users

## Overview

This Ansible role is designed for cross-platform user management, handling the creation and configuration of
user accounts on Linux and Windows systems with specific attributes and settings.

## Requirements

No special requirements; note that this role requires root access.

## Role Variables

Variables are defined in `vars/main.yml`. Each variable is described in detail, specifying if it's required and its expected data type.
The primary variable is `users_list`, which is a list of user definitions. This list is essential for the role,
as it defines the users to be managed across the systems.

`users_host_list` and `users_group_list` are derivatives of `users_list`, tailored for host-specific or group-specific user definitions.
These lists allow for more granular control of user accounts based on the host or group context.

Additional variables include:

- `users_home`: Specifies the default home directory path for users.
- `users_group`: Defines the default primary group for users.
- `users_groups`: A list of default secondary groups for users.
- `users_home_mode`: Sets the default permissions for users' home directories.
- `users_ssh_key_type`: Determines the default SSH key type for users.
- `users_ssh_key_bits`: Specifies the default SSH key bit length.
- `users_authorized_keys_exclusive`: Controls whether to exclusively manage the 'authorized_keys' file.

These variables provide default values and configurations that apply to all users defined in the role unless overridden by individual user settings.
They ensure consistent and standardized user account management across different environments.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  roles:
    - arillso.system.users
