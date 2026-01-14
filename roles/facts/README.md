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

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
