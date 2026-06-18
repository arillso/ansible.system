# Ansible Role: tuning

Comprehensive system performance tuning for Linux systems including sysctl parameters,
I/O schedulers, CPU governors, and resource limits.

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

## Variables

| Variable                           | Default                        | Description                                             |
| ---------------------------------- | ------------------------------ | ------------------------------------------------------- |
| `tuning_sysctl_config`             | `{...}`                        | Kernel sysctl parameters (vm/net/fs/kernel tuning dict) |
| `tuning_network_sysctl_config`     | `{...}`                        | TCP/IP stack sysctl parameters (dict)                   |
| `tuning_cpu_governor`              | `auto`                         | CPU frequency scaling governor                          |
| `tuning_io_scheduler`              | `auto`                         | Block-device I/O scheduler                              |
| `tuning_transparent_hugepages`     | `madvise`                      | Transparent Huge Pages mode                             |
| `tuning_tuned_profile`             | `balanced`                     | tuned profile to apply                                  |
| `tuning_swap_file_enabled`         | `false`                        | Create and enable a swap file                           |
| `tuning_swap_swappiness`           | `10`                           | vm.swappiness value                                     |
| `tuning_security_limits`           | `[...]`                        | ulimit/limits.conf entries (nofile/nproc list)          |
| `tuning_grub_cmdline_linux_append` | `"transparent_hugepage=never"` | Kernel cmdline to append via GRUB                       |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/tuning_role.html) for detailed docs.

## Check Mode

This role is partially `--check` compatible. Tasks that read live kernel/hardware state (CPU governor, I/O scheduler, swap, ethtool ring/offload) are guarded with `when: not ansible_check_mode` and skipped in check mode, so those settings are not evaluated; sysctl/limits/GRUB config remains check-safe.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
