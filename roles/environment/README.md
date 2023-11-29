# arillso.system.environment

This Ansible role is designed for managing environment variables in specified files across systems.

## Requirements

- **Ansible Version**: 2.15 or higher is recommended.
- **Access**: Adequate permissions to modify environment variable files on the target systems.

## Role Variables

Variables for managing environment variables are defined and can be overridden in the user's playbook. The key variables include:

### `environment_files`

- A list of files where environment variables will be set.
- Each entry in the list should be a path to a file.
- Example: `environment_files: ["~/.bashrc", "/etc/environment"]`

### `environment_variables`

- A dictionary of environment variables to set.
- Keys are the names of the variables, and values are the values of these variables.
- Example: `environment_variables: { "JAVA_HOME": "/usr/lib/jvm/java-8-openjdk", "PATH": "$PATH:/usr/local/bin" }`

## Documentation

For detailed information and advanced usage, please refer to the official documentation.

## Dependencies

This role does not have any dependencies on other Ansible roles.

## Example Playbook

Here is an example playbook using the `arillso.system.environment` role:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.system.environment
  vars:
    environment_files:
      - "/etc/profile"
    environment_variables:
      "NODE_ENV": "production"
      "PATH": "$PATH:/usr/local/bin/node"
```
