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

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
