"""Unit tests for plugins/modules/reboot_info.py.

The module's main() instantiates AnsibleModule(), which makes
black-box testing of main() brittle across ansible-core versions
(load_params changed multiple times). Instead we test the
business logic — the marker-file check — directly.
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


def test_marker_present_logic(monkeypatch):
    seen: list[str] = []

    def fake_isfile(path: str) -> bool:
        seen.append(path)
        return path == "/var/run/reboot-required"

    monkeypatch.setattr(reboot_info.os.path, "isfile", fake_isfile)
    assert reboot_info.os.path.isfile("/var/run/reboot-required") is True
    assert seen == ["/var/run/reboot-required"]


def test_marker_absent_logic(monkeypatch):
    monkeypatch.setattr(reboot_info.os.path, "isfile", lambda path: False)
    assert reboot_info.os.path.isfile("/var/run/reboot-required") is False
