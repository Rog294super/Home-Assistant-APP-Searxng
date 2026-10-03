import unittest

from engine_overrides import get_engine_overrides


class TestEngineOverrides(unittest.TestCase):
    def test_category_fields_add_to_legacy_options_and_deduplicate_names(self):
        source, overrides = get_engine_overrides(
            {
                "disabled_engines_general": "google, bing",
                "disabled_engines_news": "google",
                "disabled_engines": ["reddit"],
                "engines": {"google": True, "startpage": False},
            }
        )

        self.assertEqual(source, "per-category and legacy")
        self.assertEqual(
            overrides,
            [
                {"name": "google", "disabled": True},
                {"name": "startpage", "disabled": True},
                {"name": "reddit", "disabled": True},
                {"name": "bing", "disabled": True},
            ],
        )

    def test_legacy_disabled_engine_list_is_preserved(self):
        source, overrides = get_engine_overrides(
            {"disabled_engines": ["google", "bing"]}
        )

        self.assertEqual(source, "legacy disabled_engines")
        self.assertEqual(
            overrides,
            [
                {"name": "google", "disabled": True},
                {"name": "bing", "disabled": True},
            ],
        )

    def test_legacy_engine_switches_are_preserved(self):
        source, overrides = get_engine_overrides(
            {"engines": {"google": True, "startpage": False}}
        )

        self.assertEqual(source, "legacy engines")
        self.assertEqual(
            overrides,
            [
                {"name": "google", "disabled": False},
                {"name": "startpage", "disabled": True},
            ],
        )

    def test_no_overrides_leaves_upstream_configuration_untouched(self):
        self.assertIsNone(get_engine_overrides({"engines": {}}))


if __name__ == "__main__":
    unittest.main()