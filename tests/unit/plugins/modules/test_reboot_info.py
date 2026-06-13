"""Unit tests for plugins/modules/reboot_info.py.

The module's main() instantiates AnsibleModule(), which makes
black-box testing of main() brittle across ansible-core versions
(load_params changed multiple times). Until the marker check is
extracted into a standalone helper, the only assertion that touches
real module state is the marker-path constant — a regression guard
against an accidental rename of the Debian-family marker path.
"""

from __future__ import annotations

from ansible_collections.arillso.system.plugins.modules import reboot_info


def test_marker_path_constant_matches_debian_default():
    source = reboot_info.__file__
    with open(source, encoding="utf-8") as fh:
        body = fh.read()
    assert '"/var/run/reboot-required"' in body, (
        "module should still probe the Debian-family reboot marker path"
    )
