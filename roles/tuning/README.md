# Ansible Role: tuning

Comprehensive system performance tuning for Linux systems including sysctl parameters, I/O schedulers, CPU governors, and resource limits.

## Features

- **Sysctl Tuning**: Configure kernel parameters for optimal performance
- **I/O Scheduler**: Auto-detect and configure appropriate I/O scheduler
- **CPU Governor**: Manage CPU frequency scaling governors
- **Security Limits**: Configure ulimit and resource limits
- **Network Tuning**: Optimize TCP/IP stack parameters
- **Swap Management**: Configure swappiness and swap file creation
- **Transparent Huge Pages**: THP configuration for databases and VMs
- **Tuned Integration**: Apply predefined tuned performance profiles

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/tuning_role.html](https://guide.arillso.io/collections/arillso/system/tuning_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.tuning
        vars:
            tuning_cpu_governor: performance
            tuning_tuned_profile: throughput-performance
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
