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

## Variables

| Variable                     | Default                                             | Description                                       |
| ---------------------------- | --------------------------------------------------- | ------------------------------------------------- |
| `zram_enabled`               | `true`                                              | Master switch; `false` makes every task a no-op   |
| `zram_percent`               | `50`                                                | Percentage of physical RAM allocated as zram swap |
| `zram_algorithm`             | `zstd`                                              | Kernel compression algorithm                      |
| `zram_priority`              | `100`                                               | Swap priority (kept above disk swap)              |
| `zram_packages`              | `[zram-tools]`                                      | Distro packages to install                        |
| `zram_kernel_module_package` | `linux-modules-extra-<kernel>` on Ubuntu, else `""` | Package providing the zram kernel module          |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/zram_role.html) for detailed docs.

## Check Mode

This role is partially `--check` compatible. Package install and config templating are check-safe, but the compression-algorithm validation reads live kernel state (`/sys/block/zram0/comp_algorithm`) which is unavailable until the module is loaded, so validation is skipped in check mode.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
