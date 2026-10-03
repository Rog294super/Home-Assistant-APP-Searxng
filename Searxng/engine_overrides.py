"""Resolve new and legacy engine options without changing saved option types."""

from typing import Any

CATEGORY_FIELDS = (
    "disabled_engines_general",
    "disabled_engines_images",
    "disabled_engines_videos",
    "disabled_engines_news",
    "disabled_engines_maps",
    "disabled_engines_music",
    "disabled_engines_it",
    "disabled_engines_science",
    "disabled_engines_files",
    "disabled_engines_social_media",
)


def _parse_engine_names(values: Any) -> list[str]:
    if isinstance(values, str):
        return [part.strip() for part in values.split(",") if part.strip()]
    if isinstance(values, list):
        return [str(value).strip() for value in values if str(value).strip()]
    return []


def get_engine_overrides(
    options: dict[str, Any],
) -> tuple[str, list[dict[str, Any]]] | None:
    category_names = [
        name
        for field in CATEGORY_FIELDS
        for name in _parse_engine_names(options.get(field, ""))
    ]
    if category_names:
        return "per-category", [
            {"name": name, "disabled": True}
            for name in dict.fromkeys(category_names)
        ]

    disabled_names = _parse_engine_names(options.get("disabled_engines"))
    if disabled_names:
        return "legacy disabled_engines", [
            {"name": name, "disabled": True}
            for name in dict.fromkeys(disabled_names)
        ]

    legacy_engines = options.get("engines")
    if isinstance(legacy_engines, dict) and legacy_engines:
        return "legacy engines", [
            {"name": str(name), "disabled": not bool(enabled)}
            for name, enabled in legacy_engines.items()
        ]

    return None