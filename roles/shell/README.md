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

## Variables

| Variable                             | Default                        | Description                                  |
| ------------------------------------ | ------------------------------ | -------------------------------------------- |
| `shell_motd_enabled`                 | `true`                         | Manage the MOTD                              |
| `shell_motd_style`                   | `"standard"`                   | MOTD style (`standard`, `figlet`, `minimal`) |
| `shell_ssh_banner_enabled`           | `true`                         | Deploy a pre-auth SSH banner                 |
| `shell_company_name`                 | `"Hetzner Cloud K3s Platform"` | Branding name shown in MOTD/banner           |
| `shell_environment`                  | `"production"`                 | Environment label                            |
| `shell_node_type`                    | `"generic"`                    | Free-form node type label in the MOTD footer |
| `shell_configure_aliases`            | `true`                         | Configure shell aliases                      |
| `shell_enable_background_processing` | `true`                         | Precompute MOTD performance data via timer   |
| `shell_facts_dependency`             | `true`                         | Require the `facts` role                     |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/shell_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. The single command task (banner generation) is guarded with `check_mode: false` and `changed_when: false`; all other tasks use idempotent template/file modules.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
