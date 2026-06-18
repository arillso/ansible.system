# Ansible Role: thermal

Manages thermal and sensor monitoring on Linux systems using thermald, lm-sensors, and fancontrol.

## Features

- **Thermal Management**: Configure thermald for intelligent cooling
- **Sensor Detection**: Automatic hardware sensor detection
- **Temperature Thresholds**: Configurable temperature limits
- **Performance Profiles**: QUIET, PERFORMANCE, or BALANCED modes
- **Multi-Zone Support**: ACPI and CPU thermal zone management

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/thermal_role.html](https://guide.arillso.io/collections/arillso/system/thermal_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.thermal
        vars:
            thermal_preference: "PERFORMANCE"
            thermal_cpu_passive_temp: 80000
```

## Variables

| Variable                     | Default                              | Description                                          |
| ---------------------------- | ------------------------------------ | ---------------------------------------------------- |
| `thermal_enabled`            | `true`                               | Master switch for the role                           |
| `thermal_packages`           | `[lm-sensors, fancontrol, thermald]` | Packages to install                                  |
| `thermal_preference`         | `"QUIET"`                            | Thermal profile (`QUIET`, `PERFORMANCE`, `BALANCED`) |
| `thermal_cpu_passive_temp`   | `75000`                              | CPU passive trip point (millidegrees C)              |
| `thermal_cpu_active_temp`    | `85000`                              | CPU active trip point (millidegrees C)               |
| `thermal_enable_acpitz`      | `true`                               | Manage the ACPI thermal zone                         |
| `thermal_enable_cpu_temp`    | `true`                               | Manage the CPU thermal zone                          |
| `thermal_run_sensors_detect` | `false`                              | Run `sensors-detect --auto`                          |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/thermal_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. The `sensors-detect` probe is guarded with `changed_when: false`/`failed_when: false`; thermald and fancontrol config is written via idempotent template tasks.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
