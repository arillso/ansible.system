# Ansible Role: arillso.system.users

## Overview

This Ansible role is designed for cross-platform user management, handling the creation and configuration of
user accounts on Linux and Windows systems with specific attributes and settings.

## Requirements

No special requirements; note that this role requires root access.

## Role Variables

Variables are defined in `vars/main.yml`. Each variable is described in detail, specifying if it's required and its expected data type.
The primary variable is `users_list`, which is a list of user definitions.

`users_host_list` and `users_group_list` are derivatives of `users_list`, tailored for host-specific or group-specific user definitions.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  roles:
    - arillso.system.users
