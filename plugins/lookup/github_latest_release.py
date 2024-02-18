#!/usr/bin/python3
# Copyright: (c) 2024, Arillso
#
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# License available at https://opensource.org/licenses/MIT
"""
Lookup plugin for Ansible to fetch the latest release version from GitHub repositories.
This plugin returns the latest tagged release version of specified public GitHub repositories.
"""

# pylint: disable=import-error
from json import JSONDecodeError, loads
from re import compile as regex_compile

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils._text import to_native, to_text
from ansible.module_utils.urls import open_url
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

DOCUMENTATION = r"""
lookup: latest_release
author:
  - arillso (@arillso) <hello@arillso.io>
version_added: "2.9"
requirements:
  - json
  - re
short_description: Get the latest tagged release version from a public Github repository.
description:
  - This lookup returns the latest tagged release version of a public Github repository.
  - A future version will accept an optional Github token to allow lookup of private repositories.
options:
  repos:
    description: A list of Github repositories from which to retrieve versions.
    required: True
notes:
  - The version tag is returned however it is defined by the Github repository.
  - Most repositories used the convention 'vX.X.X' for a tag, while some use 'X.X.X'.
  - Some may use release tagging structures other than semver.
  - This plugin does not perform opinionated formatting of the release tag structure.
  - Users should format the value via filters after calling this plugin, if needed.
seealso:
  - name: Github Releases API
    description: API documentation for retrieving the latest version of a release.
    link: https://developer.github.com/v3/repos/releases/#get-the-latest-release
"""

EXAMPLES = r"""
- name: Strip the 'v' out of the tag version, e.g. 'v1.0.0' -> '1.0.0'
  set_fact:
    ansible_version: "{{ lookup('arillso.system.github_latest_release', 'ansible/ansible')[1:] }}"

- name: Operate on multiple repositories
  git:
    repo: https://github.com/{{ item }}.git
    version: "{{ lookup('arillso.system.github_latest_release', item) }}"
    dest: "{{ lookup('env', 'HOME') }}/projects"
  with_items:
    - ansible/ansible
    - ansible/molecule
    - ansible/awx
"""

RETURN = r"""
  _list:
    description:
      - List of latest Github repository version(s)
    type: list
"""

display = Display()


class LookupModule(LookupBase):  # pylint: disable=too-few-public-methods
    """Lookup plugin for fetching the latest release version from GitHub repositories."""

    def run(self, terms, variables=None, **kwargs):  # pylint: disable=unused-argument
        """Fetches the latest release version for given GitHub repositories.

        Args:
            terms (list): List of GitHub repositories to lookup.
            variables (dict, optional): Unused in this context.
            **kwargs: Additional keyword arguments.

        Returns:
            list: Versions of the latest releases found for the given repositories.
        """
        versions = []

        if not terms:
            raise AnsibleParserError("You must specify at least one repo name.")

        valid_github_username_and_repo_name = regex_compile(r"[a-z\d\-]+\/[a-z\d\S]+")

        for repo in terms:
            if not valid_github_username_and_repo_name.match(repo):
                raise AnsibleParserError(
                    f"Repo name is incorrectly formatted: {to_text(repo)}"
                )

            display.debug(f"Github version lookup term: '{to_text(repo)}'")

            try:
                response = open_url(
                    f"https://api.github.com/repos/{repo}/releases/latest",
                    headers={"Accept": "application/vnd.github.v3+json"},
                )
                json_response = loads(response.read().decode("utf-8"))

                version = json_response.get("tag_name")
                if version:
                    versions.append(version)
                else:
                    raise AnsibleError(
                        "Error extracting version from Github API response."
                    )
            except JSONDecodeError as e:
                raise AnsibleError(
                    f"Error parsing JSON from Github API response: {to_native(e)}"
                ) from e

            display.vvvv(f"Github version lookup using {repo} as repo")

        return versions
