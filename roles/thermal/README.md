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

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
