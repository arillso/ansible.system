# arillso.system.dnf_packages

This Ansible role is created to manage DNF packages on systems, providing capabilities for the installation, upgrade, and removal of DNF packages.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Access**: Adequate permissions to manage DNF packages on the target systems

## Role Variables

Variables for managing DNF packages are defined in `defaults/main.yml`. Users can override these in their playbook. The key variables include:

### DNF Packages Configuration

- `dnf_packages_list`: A list of dictionaries specifying DNF packages to manage. Each dictionary includes options like `allow_downgrade`, `allowerasing`, `autoremove`, `bugfix`, `cacheonly`, and others.

### Global Options

- `dnf_packages_allow_downgrade`: Allow downgrading of packages. (Default: `false`)
- `dnf_packages_allowerasing`: Allow erasing of installed packages. (Default: `false`)
- `dnf_packages_autoremove`: Automatic removal of packages. (Default: `false`)
- `dnf_packages_bugfix`: Limit updates to bugfix versions. (Default: `false`)
- `dnf_packages_cacheonly`: Use only the cache. (Default: `false`)
- `dnf_packages_conf_file`: Configuration file for DNF. (Default: `{{ omit }}`)
- `dnf_packages_disable_gpg_check`: Disable GPG check. (Default: `false`)
- `dnf_packages_disable_plugin`: Plugins to disable. (Default: `{{ omit }}`)
- `dnf_packages_disablerepo`: Repositories to disable. (Default: `{{ omit }}`)
- `dnf_packages_download_dir`: Directory for downloading packages. (Default: `{{ omit }}`)
- `dnf_packages_download_only`: Download-only mode. (Default: `false`)
- `dnf_packages_enable_plugin`: Plugins to enable. (Default: `{{ omit }}`)
- `dnf_packages_enablerepo`: Repositories to enable. (Default: `{{ omit }}`)
- `dnf_packages_exclude`: Packages to exclude. (Default: `{{ omit }}`)
- `dnf_packages_install_repoquery`: Install 'repoquery'. (Default: `false`)
- `dnf_packages_install_weak_deps`: Install weak dependencies. (Default: `true`)
- `dnf_packages_installroot`: Installation root. (Default: `{{ omit }}`)
- `dnf_packages_lock_timeout`: Lock timeout. (Default: `30`)
- `dnf_packages_nobest`: Ignore best version of package. (Default: `false`)
- `dnf_packages_releasever`: Release version. (Default: `{{ omit }}`)
- `dnf_packages_security`: Limit updates to security versions. (Default: `false`)
- `dnf_packages_skip_broken`: Skip broken packages. (Default: `false`)
- `dnf_packages_sslverify`: SSL verification. (Default: `true`)
- `dnf_packages_state`: Default package state (present, absent, latest). (Default: `present`)
- `dnf_packages_update_cache`: Update the cache. (Default: `true`)
- `dnf_packages_update_only`: Update-only mode. (Default: `false`)
- `dnf_packages_validate_certs`: Validate certificates. (Default: `true`)

## Documentation

For detailed information and advanced usage, please refer to our guide:

[Arillso System Guide](https://guide.arillso.io/collections/arillso/system/dnf_packages_role.html#ansible-collections-arillso-system-dnf-packages-role)

## Dependencies

This role is standalone and does not require other Ansible roles as dependencies.

## Example Playbook

Example playbook for using `arillso.system.dnf_packages`:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.system.dnf_packages
  vars:
    dnf_packages_list:
      - name: 'httpd'
        state: 'latest'
        allow_downgrade: false
        allowerasing: true
```
