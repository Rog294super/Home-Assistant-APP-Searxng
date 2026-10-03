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
    overrides: dict[str, bool] = {}
    legacy_engines = options.get("engines")
    has_legacy_engine_options = isinstance(legacy_engines, dict) and bool(legacy_engines)
    if isinstance(legacy_engines, dict):
        overrides.update(
            {str(name): not bool(enabled) for name, enabled in legacy_engines.items()}
        )

    disabled_names = _parse_engine_names(options.get("disabled_engines"))
    for name in disabled_names:
        overrides[name] = True

    category_names = [
        name
        for field in CATEGORY_FIELDS
        for name in _parse_engine_names(options.get(field, ""))
    ]
    for name in category_names:
        overrides[name] = True

    if overrides:
        if category_names:
            source = "per-category and legacy"
        elif disabled_names:
            source = (
                "legacy disabled_engines and engines"
                if has_legacy_engine_options
                else "legacy disabled_engines"
            )
        else:
            source = "legacy engines"
        return source, [
            {"name": name, "disabled": disabled}
            for name, disabled in overrides.items()
        ]

    return None