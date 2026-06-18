# Ansible Role: facts

Comprehensive system facts collection and caching for use across roles and playbooks.

## Features

- **System Facts Collection**: Gather comprehensive system information
- **Cloud Provider Detection**: Detect and collect cloud provider metadata
- **Facts Caching**: Cache facts for improved performance
- **Custom Facts**: Support for custom fact gathering
- **Cross-Role Integration**: Facts available to all roles in playbook

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/facts_role.html](https://guide.arillso.io/collections/arillso/system/facts_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.facts
        vars:
            facts_cache_ttl: 3600
```

## Variables

| Variable                           | Default                                      | Description                           |
| ---------------------------------- | -------------------------------------------- | ------------------------------------- |
| `facts_node_type`                  | `"generic"`                                  | Node classification label             |
| `facts_cache_enabled`              | `true`                                       | Enable on-disk fact caching           |
| `facts_cache_dir`                  | `/var/cache/ansible-facts`                   | Cache directory                       |
| `facts_cache_default_ttl`          | `300`                                        | Default cache TTL in seconds          |
| `facts_enable_cloud_metadata`      | `true`                                       | Collect cloud provider metadata       |
| `facts_cloud_providers_enabled`    | `[aws, digitalocean, hetzner, gcp, generic]` | Cloud providers to probe              |
| `facts_enable_security_updates`    | `true`                                       | Collect pending security update facts |
| `facts_enable_container_detection` | `true`                                       | Detect container runtimes             |
| `facts_timeout_default`            | `5`                                          | Default probe timeout in seconds      |
| `facts_debug_enabled`              | `false`                                      | Enable debug output                   |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/facts_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. Fact-collection scripts and caches are read-only probes that make no system changes; deployed via idempotent file/template tasks.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
