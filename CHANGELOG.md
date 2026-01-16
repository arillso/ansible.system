# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
