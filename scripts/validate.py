#!/usr/bin/env python3
"""Validate Sublime Sylvan theme and color scheme package files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "Sylvan.sublime-theme",
    "Sylvan.sublime-color-scheme",
    "Widget - Sylvan.sublime-settings",
    "Widget - Sylvan.hidden-color-scheme",
    "LICENSE",
    "README.md",
]

SYLVAN_PALETTE = {
    "bg_base": "#0f0f11",
    "bg_sidebar": "#131416",
    "bg_layer_1": "#18191b",
    "bg_layer_2": "#202124",
    "bg_layer_3": "#26272b",
    "border_l1": "#27282c",
    "border_l2": "#35373c",
    "border_l3": "#46494f",
    "label_primary": "#e3e4e6",
    "label_secondary": "#a7aab1",
    "label_tertiary": "#82858d",
    "brand_primary": "#4fa66b",
    "brand_text": "#75bd8a",
    "brand_tertiary": "#21392a",
    "interactive_hover": "#232529",
    "interactive_active": "#23372a",
    "state_success": "#69c967",
    "state_error": "#ff7e78",
}

VAR_PATTERN = re.compile(r"var\(([^)]+)\)")
HEX_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

INHERITED_THEME_VARS = {
    "font_face",
    "font_size_sm",
    "font_size",
    "font_size_lg",
    "font_size_title",
}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"{path.name}: invalid JSON: {exc}") from exc


def iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for value in obj.values():
            yield from iter_strings(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_strings(item)


def check_vars(name: str, data: dict, allowed_extra: set[str]) -> list[str]:
    errors: list[str] = []
    defined = set(data.get("variables", {}).keys()) | allowed_extra
    for text in iter_strings(data):
        for match in VAR_PATTERN.finditer(text):
            ref = match.group(1).strip()
            if ref.startswith("--"):
                continue
            if ref not in defined:
                errors.append(f"{name}: unresolved variable var({ref})")
    return errors


def validate() -> list[str]:
    errors: list[str] = []

    for filename in REQUIRED_FILES:
        if not (ROOT / filename).is_file():
            errors.append(f"missing required file: {filename}")

    theme_path = ROOT / "Sylvan.sublime-theme"
    scheme_path = ROOT / "Sylvan.sublime-color-scheme"
    widget_settings_path = ROOT / "Widget - Sylvan.sublime-settings"
    widget_scheme_path = ROOT / "Widget - Sylvan.hidden-color-scheme"

    theme = load_json(theme_path)
    scheme = load_json(scheme_path)
    widget_settings = load_json(widget_settings_path)
    widget_scheme = load_json(widget_scheme_path)

    if theme.get("extends") != "Default Dark.sublime-theme":
        errors.append("Sylvan.sublime-theme: expected extends = 'Default Dark.sublime-theme'")

    if widget_settings.get("color_scheme") != "Widget - Sylvan.hidden-color-scheme":
        errors.append("Widget - Sylvan.sublime-settings: color_scheme must point to Widget - Sylvan.hidden-color-scheme")

    errors.extend(check_vars(theme_path.name, theme, INHERITED_THEME_VARS))
    errors.extend(check_vars(scheme_path.name, scheme, set()))
    errors.extend(check_vars(widget_scheme_path.name, widget_scheme, set()))

    for label, data in [(theme_path.name, theme), (scheme_path.name, scheme)]:
        variables = data.get("variables", {})
        for key, expected in SYLVAN_PALETTE.items():
            actual = variables.get(key)
            if actual is None:
                errors.append(f"{label}: missing Sylvan palette variable '{key}'")
            elif actual.lower() != expected.lower():
                errors.append(f"{label}: variable '{key}' = {actual}, expected {expected}")

    for label, data in [(scheme_path.name, scheme), (widget_scheme_path.name, widget_scheme)]:
        rules = data.get("rules", [])
        if not rules:
            errors.append(f"{label}: rules must not be empty")
        for idx, rule in enumerate(rules):
            if not rule.get("scope"):
                errors.append(f"{label}: rule #{idx} missing scope")
            for color_key in ("foreground", "background"):
                val = rule.get(color_key)
                if val and not (val.startswith("var(") or val.startswith("color(") or HEX_PATTERN.match(val)):
                    errors.append(f"{label}: rule #{idx} invalid {color_key}: {val}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("OK: all Sylvan Sublime package checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
