# arillso.system.groups

This Ansible role is designed for the management of user groups on systems. It allows for adding, modifying, or removing groups, as well as managing group IDs and system group flags.

## Variables and Default Values

This role uses various variables to customize group management. The following sections describe these variables and their default values.

### `groups_list`

A list of groups to be added. By default, this list is empty.

Example:

```yaml
groups_list:
  - name: admin
    state: present
    system: no
```

### groups_host_list

A list of groups to be added by host-specific variables. By default, this list is empty.

Example:

```yaml
groups_host_list:
  - name: developers
    state: present
    system: no
```

### groups_group_list

A list of groups to be added by group vars. By default, this list is empty.

Example:

```yaml
groups_group_list:
  - name: testers
    state: present
    system: no
```

### groups_gid

The default GID (Group Identifier) for groups. Not set by default.

Variable:

```yaml
groups_gid: "{{ omit }}"
```

### groups_system

Whether the group is a system group. Default is 'no'.

Variable:

```yaml
groups_system: "no"
```

### groups_state

The default state for groups. Default is 'present'.

Variable:

```yaml
groups_state: present
```

### groups_non_unique

Whether the group should have a unique GID. Default is 'yes'.

Variable:

```yaml
groups_non_unique: "no"
```

## Documentation

For detailed information and advanced usage, please refer to our guide:

[Arillso System Guide](https://guide.arillso.io/collections/arillso/system/groups_role.html#ansible-collections-arillso-system-groups-role)

## Dependencies

This role is standalone and does not require other Ansible roles as dependencies.
