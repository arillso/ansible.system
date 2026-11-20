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

| Variable                          | Default                                             | Description                                                     |
| --------------------------------- | --------------------------------------------------- | --------------------------------------------------------------- |
| `zram_enabled`                    | `true`                                              | Master switch; `false` disables zramswap (off after reboot)     |
| `zram_percent`                    | `50`                                                | Percentage of physical RAM allocated as zram swap               |
| `zram_algorithm`                  | `zstd`                                              | Kernel compression algorithm                                    |
| `zram_priority`                   | `100`                                               | Swap priority (kept above disk swap)                            |
| `zram_packages`                   | `[zram-tools]`                                      | Distro packages to install                                      |
| `zram_kernel_module_package`      | `linux-modules-extra-<kernel>` on Ubuntu, else `""` | Package providing the zram kernel module                        |
| `zram_kernel_module_meta_package` | `""`                                                | Opt-in metapackage that keeps the module across kernel upgrades |
| `zram_restart_on_change`          | `false`                                             | Restart zramswap even while zram swap holds data                |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/zram_role.html) for detailed docs.

## Config Changes

A changed `/etc/default/zramswap` restarts `zramswap` only while the zram swap
is empty. The restart runs `swapoff`, which moves every page held in zram back
to RAM, so on a host with data in zram the new settings wait for the next
reboot. Set `zram_restart_on_change: true` to restart anyway.

The role fails when `systemd-zram-generator` or `zram-config` is installed,
because both create their own zram swap devices.

## Kernel Upgrades

On Ubuntu the zram module comes from `linux-modules-extra-<kernel>`, which only
covers the running kernel. After a kernel upgrade, run the role again or set
`zram_kernel_module_meta_package` (for example `linux-image-extra-virtual`, or
`linux-modules-extra-aws` on AWS kernels). The role sets no default, because the
generic metapackage also pulls `linux-image-generic` with firmware and microcode,
and on HWE hosts a second kernel series.

## Check Mode

This role is partially `--check` compatible. Package install and config templating are check-safe, but the compression-algorithm validation reads live kernel state (`/sys/block/zram0/comp_algorithm`) which is unavailable until the module is loaded, so validation is skipped in check mode. On a host without `zram-tools`, the service step is skipped too, because the unit does not exist yet.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
