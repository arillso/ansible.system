"""Shared pytest configuration for collection unit tests.

Tests import plugins via the fully-qualified collection namespace
``ansible_collections.arillso.system.plugins.*`` so that both
``ansible-test units --docker`` (the CI gate) and a plain
``pytest tests/unit/`` (the developer loop) work without divergence.

When running outside ``ansible-test``, the collection is usually not
yet installed under that import path; this conftest registers the
repository checkout as the ``ansible_collections.arillso.system``
package so the same imports resolve.
"""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_NAMESPACE = "ansible_collections"
_COLLECTION = "ansible_collections.arillso.system"


def _ensure_namespace_package(name: str, path: Path | None = None) -> types.ModuleType:
    if name in sys.modules:
        return sys.modules[name]
    module = types.ModuleType(name)
    module.__path__ = [str(path)] if path else []  # type: ignore[attr-defined]
    sys.modules[name] = module
    return module


# When ansible-test runs us, the collection is already installed at
# ansible_collections/arillso/system; in that case we leave sys.modules
# alone and let the real package take precedence.
try:
    importlib.import_module(_COLLECTION)
except ModuleNotFoundError:
    _ensure_namespace_package(_NAMESPACE)
    _ensure_namespace_package(f"{_NAMESPACE}.arillso")
    coll = _ensure_namespace_package(_COLLECTION, _REPO_ROOT)
    coll.__path__ = [str(_REPO_ROOT)]  # type: ignore[attr-defined]
