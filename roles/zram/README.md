# Ansible Role: zram

Configures compressed RAM swap (zram) on Debian/Ubuntu systems via the
`zram-tools` package.

## Features

- **Compressed RAM Swap**: Allocate a percentage of physical RAM as a zram swap device
- **Kernel Module Bootstrap**: Installs and loads the zram module (incl. `linux-modules-extra` on cloud kernels)
- **Algorithm Validation**: Verifies the requested compression algorithm against kernel capabilities
- **Priority Control**: Swap priority higher than disk swap so the kernel fills zram first
- **Idempotent Service Management**: Deploys `/etc/default/zramswap` and manages the `zramswap` service

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/zram_role.html](https://guide.arillso.io/collections/arillso/system/zram_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.zram
        vars:
            zram_percent: 50
            zram_algorithm: "zstd"
            zram_priority: 100
```

Pair with the `tuning` role for a zram-first layout by setting a lower
`tuning_swap_priority` than `zram_priority`, so disk swap acts as a fallback.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
