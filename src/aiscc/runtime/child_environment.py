"""Explicit child environment; hosted credentials are never inherited."""

import os


def child_environment() -> dict[str, str]:
    # No user-selected names or values, credential variables, proxy settings,
    # Python startup hooks, or dynamic-loader injection.
    allowed = {"SYSTEMROOT", "WINDIR", "PATH", "PATHEXT", "TEMP", "TMP", "LANG"}
    return {key: value for key, value in os.environ.items() if key.upper() in allowed}
