---
name: adding-role-or-plugin
description: Use when adding a new role or a new plugin (module, lookup, or filter) to the arillso.system collection, or when checking that an existing one carries the required files. Covers the mandatory role scaffold including meta/argument_specs.yml, and where plugin documentation lives per plugin type — inline for modules and lookups, sidecar YAML for filters. Not for editing task logic in an existing role.
---

# Adding a Role or Plugin

## Adding a Role

Every one of the 15 roles carries these five files. A new role without them is
incomplete:

- `README.md` — description, variables, example play
- `meta/main.yml`
- `meta/argument_specs.yml` — validates role arguments; mandatory, not optional
- `tasks/main.yml`
- `defaults/main.yml` — every variable documented with a comment

Add when the role needs them (not present in every role today):
`handlers/main.yml`, `vars/main.yml`, `templates/`.

Copy the argument spec shape from an existing role, e.g.
`roles/systemd/meta/argument_specs.yml`.

## Adding a Plugin

All plugins document `DOCUMENTATION`, `EXAMPLES` and `RETURN`. The location
depends on the plugin type:

| Type   | Code                        | Documentation                         |
| ------ | --------------------------- | ------------------------------------- |
| module | `plugins/modules/<name>.py` | inline, same file                     |
| lookup | `plugins/lookup/<name>.py`  | inline, same file                     |
| filter | `plugins/filter/<file>.py`  | `plugins/filter/<filter>.yml` sidecar |

Filters are the trap: `plugins/filter/nftables.py` and `plugins/filter/toml.py`
contain no documentation blocks at all. Each filter gets its own sidecar YAML,
one per filter — not one per Python file. `plugins/filter/to_toml.yml` is the
reference for `requirements` and `seealso`; see `plugins/filter/from_toml.yml`
for an `options` block.

## Before Opening a PR

Run `make lint` and `make test`.

Both targets skip silently when the tool is missing locally
(`SKIP: ansible-lint not installed`, `SKIP: pytest not installed`), so a green
local run proves nothing. The binding gate is the reusable CI in
`.github/workflows/pull-request.yml`.
