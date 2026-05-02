# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
