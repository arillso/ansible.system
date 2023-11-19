# arillso.system.apt_repositories

This Ansible role is designed for managing APT repositories on a system. It enables the addition, modification, and removal
of APT repositories using the `ansible.builtin.apt_repository` module.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Access**: Adequate permissions to manage APT repositories on target systems

## Role Variables

Variables for managing APT repositories are defined in `defaults/main.yml`. Users can override these in their playbook. Key variables include:

### APT Repositories Configuration

- `apt_repositories_list`: A list of APT repositories to manage. Each entry should be a dictionary with repository details such as
codename, filename, repo, state, and others.

- `apt_repositories_filename`: Default filename for APT repositories if not specified in each repository dictionary (default: 'default.list').

- `apt_repositories_update_cache_retries`: Default value for the number of retries to update the cache after adding a repository (default: 5).

- `apt_repositories_update_cache_retry_max_delay`: Default maximum delay in seconds between retries to update the cache (default: 12).

- `apt_repositories_update_cache`: Default value to decide whether to update the cache after adding a repository (default: true).

## Documentation

For detailed information and advanced usage, please refer to our guide:

[Arillso System Guide](https://guide.arillso.io/collections/arillso/system/apt_repositories.html#ansible-collections-arillso-system-apt-repositories-role)

## Dependencies

This role is standalone and does not require other Ansible roles as dependencies.

## Example Playbook

Example playbook for using `arillso.system.apt_repositories`:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.system.apt_repositories
  vars:
    apt_repositories_list:
      - repo: 'deb http://myrepo.example.com/debian buster main'
        state: 'present'
    apt_repositories_filename: 'myrepo.list'
    apt_repositories_update_cache: true
```
