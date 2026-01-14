# Ansible Role: shell

Configures shell environment, MOTD (Message of the Day), and SSH banners for system login customization.

## Features

- **MOTD Configuration**: Customizable message of the day
- **Multiple Styles**: Standard, figlet, and minimal MOTD styles
- **SSH Banners**: Pre-authentication security banners
- **System Information**: Display system stats on login
- **Company Branding**: Customizable branding and environment labels

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/shell_role.html](https://guide.arillso.io/collections/arillso/system/shell_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.shell
        vars:
            shell_company_name: "My Company"
            shell_motd_style: "figlet"
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
