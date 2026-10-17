import unittest
from pathlib import Path

import yaml


class TestConfigCompatibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config_path = Path(__file__).with_name("config.yaml")
        with config_path.open(encoding="utf-8") as config_file:
            cls.config = yaml.safe_load(config_file)

    def test_legacy_option_types_are_preserved(self):
        options = self.config["options"]
        schema = self.config["schema"]

        self.assertIsInstance(options["autocomplete"], str)
        self.assertEqual(schema["autocomplete"], "str")
        self.assertIsInstance(options["disabled_engines"], list)
        self.assertEqual(schema["disabled_engines"], ["str"])
        self.assertIsInstance(options["engines"], dict)
        self.assertIsInstance(schema["engines"], dict)

    def test_category_options_are_additive_strings(self):
        category_fields = (
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
        for field in category_fields:
            with self.subTest(field=field):
                self.assertEqual(self.config["options"][field], "")
                self.assertEqual(self.config["schema"][field], "str")


if __name__ == "__main__":
    unittest.main()