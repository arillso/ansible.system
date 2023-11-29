# arillso.system.chocolatey_packages

This Ansible role is designed to manage Chocolatey packages on Windows systems. It facilitates the installation, upgrade, and removal of Chocolatey packages.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Access**: Adequate permissions to manage Chocolatey packages on target systems

## Role Variables

Variables for managing Chocolatey packages are defined in `defaults/main.yml`. Users can override these in their playbook. Key variables include:

### Chocolatey Packages Configuration

- `chocolatey_packages_list`: A list of Chocolatey packages to manage. Each entry is a dictionary with details
such as name, state, version, source, and additional options.

### Additional Options

- `install_args`
- `package_params`
- `ignore_checksums`
- `allow_empty_checksums`
- `allow_multiple`
- `allow_prerelease`
- `architecture`
- `choco_args`
- `force`
- `ignore_dependencies`
- `override_args`
- `pinned`
- `proxy_url`
- `proxy_username`
- `proxy_password`
- `remove_dependencies`
- `skip_scripts`
- `source_username`
- `source_password`
- `timeout`
- `validate_certs`
- `bootstrap_script`

### Default Values for Global Settings

This section outlines the default values for global settings that apply to all Chocolatey packages managed by this role.
 These defaults provide a base configuration which can be overridden on a per-package basis within the `chocolatey_packages_list`.

- `chocolatey_packages_allow_empty_checksums`: Whether to allow empty checksums for packages by default. (Default: `false`)
- `chocolatey_packages_allow_multiple`: Allow multiple versions of a package to be installed by default. (Default: `false`)
- `chocolatey_packages_allow_prerelease`: Include prerelease versions of packages by default. (Default: `false`)
- `chocolatey_packages_architecture`: The default architecture (e.g., 'x86', 'x64') for packages. (Default: `{{ omit }}`)
- `chocolatey_packages_bootstrap_script`: Script for bootstrapping Chocolatey. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_choco_args`: Additional default arguments to pass to Chocolatey. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_force`: Force the installation or upgrade of packages by default. (Default: `false`)
- `chocolatey_packages_ignore_checksums`: Ignore checksums for packages by default. (Default: `false`)
- `chocolatey_packages_ignore_dependencies`: Ignore package dependencies during installation by default. (Default: `false`)
- `chocolatey_packages_install_args`: Default additional arguments for the installer. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_override_args`: Override the default installation arguments for all packages by default. (Default: `false`)
- `chocolatey_packages_package_params`: Default parameters to pass to the package installation. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_pinned`: Pin the package version by default to prevent unintended upgrades. (Default: `false`)
- `chocolatey_packages_proxy_password`: Default password for the proxy server. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_proxy_url`: Default URL of the proxy server. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_proxy_username`: Default username for the proxy server. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_remove_dependencies`: Remove package dependencies by default when a package is uninstalled. (Default: `false`)
- `chocolatey_packages_skip_scripts`: Skip running Chocolatey scripts by default. (Default: `false`)
- `chocolatey_packages_source`: The default source to install the package from. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_source_password`: Default password for the package source. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_source_username`: Default username for the package source. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_timeout`: Default timeout for the installation process. Unset by default. (Default: `{{ omit }}`)
- `chocolatey_packages_validate_certs`: Validate SSL certificates for package sources by default. (Default: `true`)

## Documentation

For detailed information and advanced usage, please refer to our guide:

[Arillso System Guide](https://guide.arillso.io/collections/arillso/system/chocolatey_packages_role.html#ansible-collections-arillso-system-chocolatey-packages-role)

## Dependencies

This role is standalone and does not require other Ansible roles as dependencies.

## Example Playbook

Example playbook for using `arillso.system.chocolatey_packages`:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.system.chocolatey_packages
  vars:
    chocolatey_packages_list:
      - name: 'git'
        state: 'latest'
        install_args: '/NoDesktopShortcut'
        override_args: true
        ignore_checksums: false
```
