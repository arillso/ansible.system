# Ansible Role: access

Comprehensive access management role for managing users, groups, sudo configuration and SSH server settings.

## Features

- **User Management**: Create, modify and remove system users
- **Group Management**: Manage system groups and memberships
- **Sudoers Configuration**: Configure sudo access with validation
- **SSH Server Configuration**: Full sshd_config management
- **SSH Key Management**: Deploy and manage SSH authorized keys

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/access_role.html](https://guide.arillso.io/collections/arillso/system/access_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.access
        vars:
            access_users:
                - name: deploy
                  groups: [sudo]
            access_ssh_password_authentication: false
```

## Variables

| Variable                             | Default               | Description                                   |
| ------------------------------------ | --------------------- | --------------------------------------------- |
| `access_users`                       | `[]`                  | Users to create/modify/remove (list of dicts) |
| `access_groups`                      | `[]`                  | Groups to manage (list of dicts)              |
| `access_sudoers`                     | `[]`                  | Sudoers entries to configure (list of dicts)  |
| `access_ssh_keys`                    | `[]`                  | SSH authorized keys to deploy                 |
| `access_ssh_port`                    | `22`                  | SSH server listen port                        |
| `access_ssh_permit_root_login`       | `"prohibit-password"` | sshd `PermitRootLogin` value                  |
| `access_ssh_password_authentication` | `false`               | Allow SSH password authentication             |
| `access_user_shell_default`          | `/bin/bash`           | Default login shell for new users             |
| `access_validate_sudoers`            | `true`                | Validate sudoers files with `visudo -c`       |
| `access_backup_configs`              | `true`                | Back up config files before changes           |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/access_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. Fully supported; all changes go through idempotent modules (user, group, template) with no command output dependencies.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
