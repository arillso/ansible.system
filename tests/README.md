# Tests — arillso.system

This collection ships three complementary test suites:

| Layer               | Path                          | What it verifies                                                | When it runs                             |
| ------------------- | ----------------------------- | --------------------------------------------------------------- | ---------------------------------------- |
| Unit tests          | `tests/unit/`                 | Plugin code in `plugins/{filter,lookup,modules}` (pure Python). | Every push (`enable_unit_tests` in CI).  |
| Integration targets | `tests/integration/targets/`  | The custom modules end-to-end against a live host.              | Every push (`enable_integration_tests`). |
| Molecule scenarios  | `extensions/molecule/<role>/` | Role behaviour against real containers, one scenario per role.  | Manual locally, opt-in matrix in CI.     |

The unit suite is the fast gate (sub-second). Integration targets sit in
between: they run the modules for real via `ansible-test`, but only cover
`plugins/modules/`, not the roles. Molecule is the slow gate
(minutes per scenario) and lives under `extensions/` so it ships inside
the published collection tarball and runs from a Galaxy-installed
collection without re-cloning the repo.

## Unit tests

```bash
# Install runtime + test deps (one-time)
make install-dev

# Run the suite
make test
# …which is equivalent to:
pytest tests/unit/
```

The suite covers:

- `plugins/filter/toml.py` — `from_toml`, `to_toml`, `to_nice_toml`
  round-trips and error paths.
- `plugins/filter/nftables.py` — hierarchical merge precedence, rule
  rendering, port formatting.
- `plugins/lookup/environment_files.py` — short vs. dict syntax, error
  paths, idempotent merge on duplicate `file:` keys.
- `plugins/modules/reboot_info.py` — marker-file detection logic
  (without instantiating `AnsibleModule`, which couples to the
  ansible-core version).

## Integration targets

One target per custom module under `plugins/modules/`:

```text
tests/integration/targets/
├── apt_update_info/
│   ├── aliases                     # non_destructive
│   └── tasks/main.yml
└── reboot_info/
    ├── aliases                     # non_destructive
    └── tasks/main.yml
```

- `reboot_info` — creates and removes `/var/run/reboot-required` (the path
  the module hardcodes) and asserts both return branches plus check mode.
  The original marker state is restored in an `always` block, so a host
  that really does have a pending reboot is left as it was found.
- `apt_update_info` — asserts the _shape_ of the returned `packages` list:
  it is a list, and every entry carries `package`, `current` and
  `available`. The number of upgradable packages depends on how old the
  container image is, so asserting a non-empty list would be flaky.

Both targets guard themselves and end the host with a `debug` message when
their preconditions are not met — `reboot_info` needs a writable `/var/run`,
`apt_update_info` needs an APT-based host with `python-apt` and root. The
guards are task-level on purpose: under `ansible-test integration --docker`
only `skip/docker`, `skip/python*` and `skip/<arch>` aliases are honoured,
so a `skip/<platform>` alias would silently not skip anything.

```bash
# ansible-test requires the collection to sit in an ansible_collections tree.
# A symlink does not work — ansible-test resolves the real path.
mkdir -p /tmp/ac/ansible_collections/arillso/system
git archive HEAD | tar -x -C /tmp/ac/ansible_collections/arillso/system
cd /tmp/ac/ansible_collections/arillso/system

make test-integration
# …which is equivalent to:
ansible-test integration --docker --color

# Run a single target
ansible-test integration reboot_info --docker --color
```

CI does the same relocation with `actions/checkout` and a `path:` input, so
the reusable workflow can call `ansible-test` directly.

## Molecule scenarios

### Layout

```text
extensions/
└── molecule/
    ├── .config/
    │   └── requirements.yml         # Galaxy collection deps for every scenario
    ├── access/                      # Full converge + verify
    ├── ansible/                     # Full converge + verify
    ├── bitwarden_secrets/           # Full converge + verify (downloads bws)
    ├── facts/                       # Full converge + verify
    ├── firewall/                    # Container-safe: renders + nft -c syntax check
    ├── logging/                     # Full converge + verify
    ├── network/                     # Container-safe: resolv path only
    ├── packages/                    # Full converge + verify
    ├── python/                      # Full converge + verify (creates venv)
    ├── ready/                       # Smoke-only converge
    ├── shell/                       # Full converge + verify
    ├── systemd/                     # Full converge + verify (deploys unit + journald drop-in)
    ├── thermal/                     # Syntax-only (needs real kernel)
    └── tuning/                      # Syntax-only (needs real kernel)
```

### Driver and platforms

All scenarios use the `docker` driver with the
[`geerlingguy/docker-*-ansible`][geerlingguy] systemd-enabled images.
Each scenario lists its target platforms explicitly. The default matrix is:

- `debian-bookworm` (12)
- `ubuntu-noble` (24.04)
- `rocky-9` (EL9)

Container-incompatible work (`tuning`, `thermal`) and
kernel-namespace-bound work (`firewall`, `network/netplan`) deviates:

- `firewall` runs **converge + verify in a render-only mode**: the
  nftables template is rendered, then `nft -c` syntax-checks the
  ruleset without loading it into the kernel.
- `network` covers only the `network_resolv_enabled` path.
- `tuning` and `thermal` use a `test_sequence` of
  `dependency → destroy → syntax → create → destroy` — Ansible's
  `--syntax-check` runs, but converge is skipped. To exercise these
  fully, run them locally against a VM (e.g. Vagrant + libvirt) by
  swapping the driver.

[geerlingguy]: https://hub.docker.com/u/geerlingguy

### Running scenarios

From the repository root:

```bash
# One-time setup
pip install -r requirements.txt
ansible-galaxy collection install -r extensions/molecule/.config/requirements.yml

# Build + install the collection so molecule can resolve arillso.system.*
ansible-galaxy collection install . --force

# Run one scenario
cd extensions
molecule test -s access

# Run the syntax-only scenario for tuning
cd extensions
molecule test -s tuning

# Iterate without tearing the container down between runs
cd extensions
molecule create -s access
molecule converge -s access
molecule verify -s access
molecule destroy -s access
```

### Adding a platform

1. Add a new `- name: …` entry under `platforms:` in the scenario's
   `molecule.yml`.
2. Use a `geerlingguy/docker-*-ansible:latest` image with systemd
   support; the standard mounts (`/sys/fs/cgroup`, `tmpfs /run`,
   `cgroupns_mode: host`) are required for any role that touches
   `systemd_unit` or restarts services.

### Adding a scenario

The shortest path is to copy an adjacent role's directory and adjust:

1. Copy `extensions/molecule/access` to
   `extensions/molecule/<role>`.
2. Edit `molecule.yml` and rename the platform `name:` fields so two
   scenarios don't collide on container names.
3. Replace the role under `include_role:` in `converge.yml`.
4. Replace the `verify.yml` assertions with ones that check the
   side-effects produced by the role's defaults.

### Running the full matrix in CI

Every scenario is wired into CI via
`arillso/.github/.github/workflows/ci-ansible-molecule.yml`, called three
times from `.github/workflows/pull-request.yml`:

- the `molecule` job runs the docker-driver scenarios (`access`,
  `ansible`, `bitwarden_secrets`, `facts`, `firewall`, `logging`,
  `network`, `packages`, `python`, `ready`, `shell`, `systemd`,
  `thermal`),
- `molecule-zram` and `molecule-tuning` run their kernel-bound scenario
  under the `qemu` (KVM) driver, because a docker-driver job does not
  provision QEMU/KVM.

The matrix is pinned explicitly rather than auto-discovered so those two
scenarios can be routed to the right driver.
