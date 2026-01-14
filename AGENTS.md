# Ansible Collection: arillso.system

## Context

This is an Ansible collection that provides roles for system configuration and management. The collection includes roles for access control, package management, network configuration, firewall setup, logging, systemd services, and system tuning.

## Structure

### Roles Directory (`roles/`)

Each role follows standard Ansible role structure with:

- `tasks/` - Main task files
- `defaults/` - Default variables
- `vars/` - Role variables
- `handlers/` - Handlers for service restarts, etc.
- `templates/` - Jinja2 templates
- `meta/` - Role metadata and dependencies

Key roles:

- **access** - User access and permissions management
- **ansible** - Ansible configuration
- **bitwarden_secrets** - Bitwarden secrets integration
- **facts** - System facts gathering
- **firewall** - Firewall configuration
- **logging** - Log management
- **network** - Network configuration
- **packages** - Package installation and management
- **python** - Python environment setup
- **shell** - Shell configuration
- **systemd** - Systemd service management
- **thermal** - Thermal management
- **tuning** - System performance tuning

### Plugins Directory (`plugins/`)

- `lookup/` - Lookup plugins (e.g., github_latest_release.py)
- `modules/` - Custom modules (e.g., apt_update_info.py, reboot_info.py)

### Configuration Files

- `galaxy.yml` - Ansible Galaxy collection metadata
- `.ansible-lint` - Ansible lint configuration
- `.mega-linter.yml` - MegaLinter configuration
- `.yamllint.yml` - YAML linting rules

## Conventions

### Code Style

- Use 4 spaces for indentation in YAML files
- Follow Ansible best practices and naming conventions
- Use descriptive variable names with role prefixes
- Document variables in `defaults/main.yml`
- Use handlers for service management

### Testing

- Roles should be linted with ansible-lint
- MegaLinter runs on push and pull requests
- Test roles in molecule when available

### Documentation

- Each role should have a README in the role directory
- Document role variables in defaults/main.yml with comments
- Keep collection-level documentation in main README.md

## Workflows

### CI/CD

- **ci.yml** - Runs MegaLinter on all commits
- **publish.yml** - Publishes to Ansible Galaxy and creates GitHub Release on tag push

### Release Process

**IMPORTANT: Always update CHANGELOG.md before releasing!**

1. **Update CHANGELOG.md** (REQUIRED - DO NOT SKIP!)
   - Add new version section (e.g., `## [1.0.1] - 2026-01-14`)
   - Document all changes under appropriate sections:
     - Added - new features
     - Changed - changes in existing functionality
     - Deprecated - soon-to-be removed features
     - Removed - removed features
     - Fixed - bug fixes
     - Security - security fixes
   - Move items from `## [Unreleased]` to the new version section

2. **Update galaxy.yml version**
   - Change `version:` field to match the new release version

3. **Create and push git tag**
   - Use version without 'v' prefix (e.g., `1.0.1` not `v1.0.1`)
   - Follow Ansible Collections best practice (no v prefix)
   - Command: `git tag 1.0.1 && git push origin 1.0.1`

4. **Automated workflow triggers**
   - Tag push automatically triggers `publish.yml` workflow
   - Workflow extracts changelog for the version
   - Publishes to Ansible Galaxy
   - Creates GitHub Release with changelog notes

**Release Checklist:**
- [ ] CHANGELOG.md updated with new version
- [ ] galaxy.yml version updated
- [ ] All CI tests passing
- [ ] README.md reflects current state (if needed)
- [ ] Git tag created and pushed (without v prefix)

## Do Not

- Do not commit secrets or sensitive data
- Do not modify roles without testing with ansible-lint
- Do not create roles without proper defaults and documentation
- Do not use deprecated Ansible syntax
- Do not hardcode values that should be variables
- Do not skip handlers or use `meta: flush_handlers` unnecessarily
