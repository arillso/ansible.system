# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Align the release workflow with the org convention: set
  `name: Release - Ansible Collection`, simplify `run-name` to
  `Release <ref>`, use a `release-<ref>` concurrency group, and pin the
  reusable workflow to `@2026-06-17`.
- `.python-version` `3.14` → `3.13` (org-wide target — `3.14` is rejected by
  `ansible-test`, which supports at most `3.13`).

### Added

- Test infrastructure: 14 molecule scenarios (one per role) under
  `extensions/molecule/`, plus a `pytest` unit suite under `tests/unit/`
  covering the filter, lookup, and module plugins. Scenarios that touch
  the kernel (sysctl, swap, ethtool, zram, nftables) use a syntax-only
  `test_sequence` since the docker driver cannot exercise those
  reliably; shared collection requirements live in
  `extensions/molecule/.config/requirements.yml`.
- New `zram` role: compressed RAM swap via the Debian/Ubuntu `zram-tools`
  package. Bootstraps the zram kernel module (incl.
  `linux-modules-extra-<kernel>` on cloud images), validates the
  requested compression algorithm against the kernel, deploys
  `/etc/default/zramswap`, and manages the `zramswap` service.
  Configurable via `zram_percent`, `zram_algorithm`, `zram_priority`,
  `zram_packages`, and `zram_kernel_module_package`. Pairs with the
  `tuning` role for a zram-first layout (set `zram_priority` higher than
  `tuning_swap_priority` so disk swap is the fallback).
- `tuning` role: new `tuning_swap_priority` variable (default `0`,
  backward-compatible) to set the Linux swap priority. The swap file is
  now activated with `swapon -p <priority>` and the `/etc/fstab` entry
  carries `pri=<priority>`, enabling multi-backend layouts such as
  zram-first with disk-swap as a lower-priority fallback.

### Fixed

- `tuning` role: replace the two swap-validation `fail` tasks with
  `assert`. The previous `when:` lists were AND-joined, but the
  conditions were mutually exclusive (a variable cannot be both
  undefined and `== ""`), so the guards never fired. `assert` makes the
  OR-semantics explicit and reads as a pre-condition.
- `tuning` role: round `current_swap_size` up by 0.5 MiB before the
  byte→MiB conversion. `swapon` reports the swap size minus the mkswap
  header overhead (~4 KB), so a 2048 MiB file read back as 2047 MiB and
  triggered a recreate loop on every run, breaking idempotency.
- `tuning` role: stop backing up the swap file before a resize. Swap
  holds only volatile pages, so the copy preserved nothing usable, while
  each resize wrote a multi-GB `.backup.<epoch>` file that could fill
  small disks and fail the disk-space assertion. Replaced with an
  explicit refusal to shrink an existing swap file.
- `tuning` role: refresh the `swap_file_active` fact to `false` after
  `swapoff` so downstream tasks see the swap as disabled during a
  resize.
- `tuning` role: write the fstab swap entry unconditionally so the
  `pri=` option is reconciled on hosts that already had an `sw 0 0`
  entry. Previously the entry was only added when absent, so the swap
  priority never survived a reboot on the upgrade path.
- `tuning` role: reapply the swap priority at runtime (via
  `swapoff`/`swapon -p`) when it drifts from `tuning_swap_priority` on
  an already-active, correctly-sized swap; a bare `swapon -p` does not
  change the priority of an active device.
- `tuning` role: skip the remove/recreate sequence for an existing but
  inactive swap file (`current_swap_size == ""`), which previously
  rebuilt a correctly-sized file on every run, and only re-run `mkswap`
  on a freshly created file.
- `zram` role: update the apt cache before installing packages (via the
  `packages` role `cache` task), so installs on a freshly provisioned
  host or right after a kernel upgrade no longer fail on a stale index.
- `zram` role: leave `zram_kernel_module_package` empty on Debian, which
  ships the zram module in the stock kernel and has no
  `linux-modules-extra-*` package; the module install is skipped there
  instead of failing with "Unable to locate package".
- `zram` role: load the kernel module with `num_devices=1` so
  `/sys/block/zram0` is guaranteed to exist for the algorithm
  validation, even on hosts that override the modprobe default.
- `tuning` role: split the network sysctl loop into a required and an
  optional task, gated by `_net_sysctl_item.key in
tuning_optional_network_sysctl_params`. The previous single task
  self-referenced its own `register` result inside `failed_when`, which
  relies on subtle ansible-core semantics and was brittle to refactor.
  Optional sysctl misses are now reported via a follow-up debug task.
  Same audit class applied to ethtool, splitting it into required +
  best-effort branches with explicit `failed_when:` semantics.
- `facts` role: report the `Update motd` handler as `changed: true`
  instead of `false`. Handlers only fire when something upstream
  notified them, so the run is by definition not a no-op — the prior
  configuration triggered an update of `/run/motd.dynamic`. Marking the
  run as unchanged hid real configuration drift from the play recap.
- Audit `failed_when: false` across all roles and remove or justify per
  call. Removed from write operations that must fail loudly
  (`tuning/handlers/main.yml`: Reload udev, Enable network tuning
  service, Enable disable-thp service, Restart cpufrequtils, Restart
  cpupower; `tuning/tasks/cpu_governor.yml`: Enable CPU frequency
  service). Kept with explanatory comments on read-only probes,
  best-effort sysfs writes paired with persistent service config, and
  opt-in features (THP sysfs write, fallocate fast-path, I/O scheduler
  sysfs write).

### Changed

- All roles: consolidate privilege escalation on the principle of least
  privilege. `become` now lives on the single privileged task (the
  `ansible.builtin.systemd` task inside the shared `systemd` sub-role),
  and callers no longer re-declare it. Removed six redundant escalation
  declarations that broadened the `become` surface without effect: five
  `apply: become: true` blocks on the `systemd` includes (one each in
  the `access`, `logging` and `network` roles, and two in the
  `packages` role — the included task already escalates), plus the
  `block`-level `become: true` in the `network` role (every task in
  `resolv.yml`/`netplan.yml` escalates on its own). `apply:`/`block:` escalation applies `become` to _every_
  task in scope; task-level escalation applies it only where it is
  needed. No functional change — the privileged tasks still run as root.
- All roles: rework handlers into a `<role>: <action>` event-bus
  schema. `listen:` becomes the stable contract used by `notify:`
  callers, `name:` becomes a human-readable description of what the
  handler does. The `listen:` namespace (e.g. `access: restart sshd`,
  `facts: restart ssh`, `zram: restart zramswap`) prevents
  cross-role name collisions — previously `Restart ssh service` was
  defined identically in both `facts` and `shell`, and the dispatch
  was ambiguous. Includes the `zram` role's handler so it follows the
  same schema as the rest of the collection.
- `firewall` role: collapse the two near-identical 50-line
  `include_role` blocks in `main.yml` (Tailscale-aware and
  Tailscale-less) into a single block parameterised over the systemd
  unit's `After:`/`Wants:`. Bug fixes previously had to be applied
  twice — and one of them had drifted between branches.
- `packages` role: dispatch repository-key handling per entry via
  `include_tasks`. The old monolithic `keys.yml` (~400 lines, ~10
  shells of nested logic per key type) was refactored into per-key-type
  files (`_keys_normalise.yml`, `_key_apply.yml`) called once per key
  in the list. Per-key includes mean a key-type addition is a new
  file, not another branch in a 400-line conditional.
- CI: switch the molecule job from an in-repo workflow to the reusable
  `arillso/.github/.github/workflows/ci-ansible-molecule.yml` (auto-
  discovers scenarios from `extensions/molecule/`) and pin all four
  reusable workflows (ci, molecule, security-secrets, claude-review)
  to the same `2026-06-12` tag.
- CI/Renovate: close the remaining version-tracking gaps. All 15
  molecule platform images (`geerlingguy/docker-*-ansible`) are pinned
  to `latest@sha256:...`. Tracking is handled by the shared
  `renovate-ansible` preset, which now carries a dedicated `docker`
  customManager for molecule `image:` lines (parses the line directly so
  `currentValue` is the bare tag and `@sha256:...` is the digest — the
  form Renovate's Docker datasource needs to refresh it) plus a
  `pinDigests` rule; the preset pin is bumped to `2026-06-14`. The images
  publish only a `latest` tag, so digest pinning is the only way to track
  them. A local marker-comment approach was tried first but the generic
  comment manager captured `repo:tag` as `currentValue`, which Renovate
  could not resolve ("Could not determine new digest"); the preset-side
  manager needs no markers. Each `python_version` CI input carries a
  `# renovate: datasource=github-releases depName=python/cpython` marker.

## [1.1.6] - 2026-05-17

### Fixed

- `access` role: wrap the `runas` field in the rendered sudoers file in
  parentheses, as required by the sudoers(5) grammar
  (`Runas_Spec ::= '(' Runas_List? (':' Runas_List)? ')'`). The
  `sudoer.j2` template emitted `host=runas` instead of `host=(runas)`,
  so every entry created from `access_sudoers` was syntactically
  invalid: `visudo -cf` rejected the file and the templating task
  failed at deploy time (`access_validate_sudoers` defaults to `true`).
  Hosts that disabled the validate hook would have silently shipped a
  broken sudoers drop-in. Both the user and group branches now render
  `=({{ runas | default('ALL') }})`, so existing example configs like
  `runas: ALL` produce valid syntax without changes. The bug was
  introduced in the access-role rewrite (`ab1b3be`, 2026-01-14) and
  affects all 1.1.x releases up to and including 1.1.5.

## [1.1.5] - 2026-05-15

### Fixed

- `firewall` role: scope nftables flush to managed tables instead of running
  a global `flush ruleset`. Both the rendered `/etc/nftables.conf` and the
  systemd-override `ExecStop` previously wiped _all_ nftables state on each
  reload/restart, including tables managed by other sources (Docker's
  iptables-nft `ip nat` / `ip filter` chains, kube-proxy, manually added
  entries). Container recreates after a firewall handler run failed with
  `iptables: No chain/target/match by that name`. The template now emits an
  empty `table <family> <name> { }` stub before each `flush table` so the
  first apply on a fresh host succeeds, and the systemd `ExecStop` flush
  commands are prefixed with `-` so systemd treats a missing table on stop
  as non-fatal
- `access` role: only set `append` on the `ansible.builtin.user` module when
  `groups` is also defined for the entry. The previous unconditional
  `append` emitted the warning `'append' is set, but no 'groups' are
specified` and would have failed hard once that warning is promoted to an
  error in `ansible-core` 2.14
- All `include_role` calls to the `systemd` role now pass `become: true`
  through `apply:` (in `access/ssh_server`, `logging/rsyslog`,
  `network/resolv`, and both `packages/unattended_upgrades` branches).
  `become` directly on `ansible.builtin.include_role` only escalates the
  include itself, not the tasks inside the included role, so `systemctl`
  tasks ran unprivileged and failed on hosts where the play did not
  globally `become`

## [1.1.4] - 2026-05-02

### Fixed

- `packages` role now stats the target keyring on the host before deciding
  whether to (re-)download armored key material to `/tmp`. The previous
  `is file` Jinja test ran on the controller, so a controller that already
  had the keyring cached would skip the download even when the target was
  fresh, leaving the host without a keyring and the dearmor task without
  its source file
- `packages` role dearmor and keyserver shell tasks no longer use a folded
  scalar (`>-`) with multi-line Jinja path expressions in `cmd:`. The
  more-indented Jinja continuation lines preserved their newlines through
  YAML folding, which split the rendered command into two shell statements
  — `gpg --dearmor -o <path>` (with no stdin redirect, producing an empty
  keyring at exit 0 because of `-o`) and an orphan `< "$_tmp"` redirect.
  The result was a 0-byte keyring file that apt rejected with `NO_PUBKEY`,
  silently breaking package installs (e.g. `alloy` from the Grafana repo).
  Paths are now precomputed via task-level `vars:` and the command body is
  written as a literal block (`|`) with one shell statement per line

## [1.1.3] - 2026-05-02

### Fixed

- Ensure the destination directory exists before deploying systemd unit files in the
  `systemd` role; previously `unit.yml` only worked when `systemd_unit_path` was the
  default `/etc/systemd/system`. Callers passing a drop-in directory such as
  `/etc/systemd/system/<unit>.d` (e.g. the `firewall` role for `nftables.service.d`)
  failed on hosts where the directory did not yet exist

## [1.1.2] - 2026-05-02

### Changed

- Update `arillso/.github` reusable workflows and Renovate preset to v2026-03-25
- Update Python dev dependencies: ansible-lint v26.4.0, ruff v0.15.12, black v26.3.1,
  molecule v26.4.0, pytest v9.0.3, pytest-ansible v26.4.0, pytest-cov v7.1.0

### Fixed

- Align handler notify names in tuning role with handler definitions; the lowercase
  notify entries (`reload systemd`, `enable network tuning service`,
  `enable disable-thp service`) silently never matched the capitalized handlers,
  so the systemd daemon-reload and the network-tuning/disable-thp service activations
  never ran when their templates changed

## [1.1.1] - 2026-03-18

### Added

- Comprehensive argument specs with full option definitions for all roles: access (SSH,
  sudoers, users, groups with nested dict specs), ansible (pipx, timer, retry, debug options),
  bitwarden_secrets (download, retry options), facts (granular collection flags for hardware,
  network, storage, containers), logging (logrotate entries/globals, rsyslog entries/remote
  servers/globals), network (DNS, systemd-resolved, netplan options), packages (proxy, mirror,
  periodic, acquire, pinning, unattended upgrades), python (virtualenv, requirements, dev
  packages), shell (MOTD, prompt, aliases, history, caching options), systemd (unit file
  paths, journald rate limits/forwarding/runtime), thermal, tuning
- Key rotation support for packages role via `packages_keys_force_update` option that
  removes existing keyrings before re-downloading
- New facts collection granularity variables (`facts_system_collect_hardware`,
  `facts_network_collect_interfaces`, `facts_container_collect_inventory`, etc.)
- Explicit key removal task for `state: absent` in packages keys management

### Changed

- Migrate all `apt_key` usage (URL, keyserver, data) to modern `signed-by` keyring approach
  using `get_url`, `gpg --dearmor`, and shell-based keyserver fetching instead of deprecated
  `ansible.builtin.apt_key` module
- Split dearmor operations into separate download and dearmor steps with proper temp file
  cleanup (trap-based)
- Change `packages_apt_force_confdef` default from `true` to `false`
- Update `arillso/.github` reusable workflows to v2026-03-09
- Claude workflow now only triggers on `@claude` mentions in comments (removed
  `pull_request_review` and `issues` triggers)
- Update workflow permissions: `pull-requests` and `issues` changed from `read` to `write`

### Fixed

- Add privilege check with clear error message for cache update in `apt_update_info` module
- Fix formatting in AGENTS.md, renovate.json, and PR template

## [1.1.0] - 2026-03-09

### Added

- Claude AI code review integration for pull requests
- Claude AI workflow for issue and PR comment automation
- CONTRIBUTING.md with development guidelines and coding standards

### Changed

- Migrate CI workflow to reusable org-level workflows from `arillso/.github`
- Migrate publish workflow to reusable `release-ansible-collection.yml`
- Update minimum Python version from 3.11 to 3.12 (required by Sphinx 9.1+)
- Update dependencies: ansible-lint v26.3, black v26, molecule v26, molecule-plugins v25,
  pytest v9, pytest-ansible v26, pytest-cov v7, sphinx v9.1
- Consolidate Python linter configuration into `pyproject.toml`
- Update GitHub Actions dependencies
- Improve README badge formatting with reference-style links
- Update GitHub issue and pull request templates

### Removed

- Remove standalone linter config files (`.flake8`, `.isort.cfg`, `.mypy.ini`,
  `.pylintrc`, `.ruff.toml`, `pyrightconfig.json`, `.yamllint.yml`, `.markdownlint.jsonc`)
- Remove `tomli` runtime dependency (use stdlib `tomllib` with Python 3.12+)
- Remove inaccurate `windows` tag from `galaxy.yml`

### Fixed

- Fix Python plugin lint errors (remove legacy coding comments, `__future__` imports,
  `__metaclass__` assignments, and `object` base class)
- Fix YAML indentation in filter plugin documentation files (2-space to 4-space)
- Fix markdown lint errors in README, AGENTS.md, and template files
- Add `no_log` to user management task when password is defined
- Fix `apt_update_info` module using text progress that pollutes Ansible JSON output

## [1.0.5] - 2026-01-16

### Fixed

- Fix Sphinx documentation build warning for to_toml filter examples
- Convert bare Jinja2 expressions to valid YAML playbook tasks in filter documentation

### Changed

- Improve README.md formatting and installation instructions
- Add requirements.yml installation example to README
- Clarify dependencies section in README

## [1.0.4] - 2026-01-16

### Fixed

- Add `-` prefix to systemd ExecStartPre commands to allow failure without stopping service
- Fix environment variable building by replacing dict2items with keys/zip/values
  for better compatibility
- Ensures git pull and galaxy install failures don't prevent playbook execution

## [1.0.3] - 2026-01-16

### Fixed

- Fix pipx module usage by replacing unsupported parameters (pipx_home, global_bin_dir)
  with environment variables (PIPX_HOME, PIPX_BIN_DIR)
- Resolves error: "Unsupported parameters for (community.general.pipx) module"

## [1.0.2] - 2026-01-16

### Added

- Automatic Galaxy requirements installation for ansible role in both pull and playbook modes
- New variables `ansible_install_collections` (default: true), `ansible_install_roles` (default: false), and `ansible_requirements_file`
- Collections and roles are now automatically installed before playbook execution via systemd ExecStartPre
- GitHub issue templates (bug report, feature request, documentation)
- GitHub pull request template with contribution checklist

### Fixed

- ansible-pull does not automatically install collections/roles from requirements.yml
  (addresses upstream issues #76535 and #70309)

## [1.0.1] - 2026-01-14

### Fixed

- Added missing filter documentation for `from_toml` and `to_nice_toml`
- Resolves ansible-doc errors during Galaxy import

## [1.0.0] - 2026-01-14

### Added

- Added AGENTS.md for AI agent documentation
- Added CLAUDE.md for Claude integration
- Added .editorconfig for editor consistency
- Added .github/CODEOWNERS
- Added .github/renovate.json for automated dependency updates
- Added nftables filter plugin for firewall rule generation

#### New Unified Roles

- **access**: User/group/SSH/sudo management (replaces users, groups, sudoers, ssh)
- **ansible**: Ansible automation with systemd timer (pull/push modes)
- **bitwarden_secrets**: Bitwarden CLI secret management
- **facts**: Extended system facts (cloud, container, security)
- **firewall**: NFTables firewall (replaces iptables)
- **logging**: Log management (replaces rsyslog, logrotate)
- **network**: Network configuration (replaces resolv, netplan)
- **python**: Python & pip management (replaces pip)
- **ready**: System readiness checks
- **shell**: Shell environment & MOTD (replaces motd)
- **systemd**: Systemd service/unit/journald management
- **thermal**: CPU thermal management
- **tuning**: System performance tuning (CPU, IO, network, swap)

#### Enhanced Roles

- **packages**: Massively expanded with APT management, unattended upgrades, keys, repositories
  (integrates apt_cache, apt_configuration, apt_keys, apt_packages, apt_repositories, dnf_packages, chocolatey_packages)

### Changed

- Renamed workflow linter.yml to ci.yml
- Migrated CHANGELOG.rst to CHANGELOG.md
- Updated publish.yml to automatically create GitHub Releases with changelog notes
- Use systemd role for all systemd operations (DRY principle)
- Inline systemd units as structured YAML (remove separate template files)
- Unify defaults/main.yml format (remove banners, keep examples)
- Updated ansible.posix dependency from >=1.4.0 to >=2.0.0
- Removed unused devsec.hardening dependency

### Fixed

- Fixed firewall Tailscale service dependency handling (#82)
- Fixed systemd_journald_runtime variables (#67)

### Security

- Apply `become: true` only at task level (principle of least privilege)
- Remove all block-level privilege escalation
- Fix reserved Ansible variable names (ansible_limit → ansible_host_limit)

### Removed

#### Consolidated Roles

The following roles have been removed and consolidated into new unified roles:

- apt_cache, apt_configuration, apt_keys, apt_packages, apt_repositories → **packages**
- chocolatey_packages, dnf_packages → **packages**
- users, groups, ssh, sudoers → **access**
- iptables → **firewall**
- logrotate, rsyslog → **logging**
- netplan, resolv → **network**
- pip → **python**
- motd → **shell**
- systemd_journald, systemd_service, systemd_unit → **systemd**
- environment, maintenance, reboot, timezone → removed (functionality integrated elsewhere)
- yum_repositories → **packages**

**BREAKING CHANGE:** Many roles have been removed and consolidated into new unified roles.
Users need to migrate to the new role structure. See role documentation for migration guidance.

## Previous Releases

For releases prior to this changelog format change, see: <https://github.com/arillso/ansible.system/releases>

[Unreleased]: https://github.com/arillso/ansible.system/compare/1.1.4...HEAD
[1.1.4]: https://github.com/arillso/ansible.system/compare/1.1.3...1.1.4
[1.1.3]: https://github.com/arillso/ansible.system/compare/1.1.2...1.1.3
[1.1.2]: https://github.com/arillso/ansible.system/compare/1.1.1...1.1.2
[1.1.1]: https://github.com/arillso/ansible.system/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/arillso/ansible.system/compare/1.0.5...1.1.0
[1.0.5]: https://github.com/arillso/ansible.system/compare/1.0.4...1.0.5
[1.0.4]: https://github.com/arillso/ansible.system/compare/1.0.3...1.0.4
[1.0.3]: https://github.com/arillso/ansible.system/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/arillso/ansible.system/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/arillso/ansible.system/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/arillso/ansible.system/releases/tag/1.0.0
