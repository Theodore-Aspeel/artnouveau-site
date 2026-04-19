import unittest

from tools.editorial_manager.translation_sync import (
    analyze_translation_sync,
    iter_source_units,
    source_text_hash,
)


def sample_article():
    return {
        "slug": "demo",
        "schema_version": 2,
        "content": {
            "fr": {
                "title": "Titre FR",
                "dek": "Chapeau FR.",
                "epigraph": "Epigraphe FR.",
                "sections": [{"heading": "Intertitre FR", "body": "Corps FR."}],
                "seo": {"meta_description": "Meta FR."},
                "media": {"hero_alt": "Alt FR."},
                "around": {"note": "Autour FR."},
                "practical_items": [
                    {"key": "city", "value": "Lille"},
                    {"key": "address", "value": "Rue de Demo"},
                ],
            },
            "en": {
                "title": "Title EN",
                "dek": "Dek EN.",
                "epigraph": "Epigraph EN.",
                "sections": [{"heading": "Heading EN", "body": "Body EN."}],
                "seo": {"meta_description": "Meta EN."},
                "media": {"hero_alt": "Alt EN."},
                "around": {"note": "Around EN."},
                "practical_items": [
                    {"key": "city", "value": "Lille"},
                    {"key": "address", "value": "Demo Street"},
                ],
            },
        },
    }


class TranslationSyncTests(unittest.TestCase):
    def test_source_units_use_stable_paths_for_main_sections_and_practical_items(self):
        units = dict(iter_source_units(sample_article()["content"]["fr"]))

        self.assertEqual(units["title"], "Titre FR")
        self.assertEqual(units["seo.meta_description"], "Meta FR.")
        self.assertEqual(units["media.hero_alt"], "Alt FR.")
        self.assertEqual(units["sections[1].heading"], "Intertitre FR")
        self.assertEqual(units["sections[1].body"], "Corps FR.")
        self.assertEqual(units["practical_items.city.value"], "Lille")
        self.assertEqual(units["practical_items.address.value"], "Rue de Demo")

    def test_existing_target_without_previous_hash_is_preserved_as_untracked(self):
        report = analyze_translation_sync(sample_article(), "en")
        statuses = {unit.path: unit.status for unit in report.units}

        self.assertEqual(report.slug, "demo")
        self.assertEqual(report.source_locale, "fr")
        self.assertEqual(report.target_locale, "en")
        self.assertEqual(statuses["title"], "localized-untracked")
        self.assertEqual(statuses["sections[1].body"], "localized-untracked")
        self.assertEqual(statuses["practical_items.address.value"], "localized-untracked")

    def test_missing_target_text_is_reported_without_changing_the_article(self):
        article = sample_article()
        article["content"]["nl"] = {"title": "  ", "sections": []}

        report = analyze_translation_sync(article, "nl")
        statuses = {unit.path: unit.status for unit in report.units}

        self.assertEqual(statuses["title"], "missing")
        self.assertEqual(statuses["sections[1].body"], "missing")
        self.assertGreater(report.missing_count, 0)

    def test_previous_matching_source_hash_marks_unit_current(self):
        article = sample_article()
        previous_hashes = {"title": source_text_hash("Titre FR")}

        report = analyze_translation_sync(article, "en", previous_hashes)
        title_unit = next(unit for unit in report.units if unit.path == "title")

        self.assertEqual(title_unit.status, "current")
        self.assertEqual(title_unit.target_text, "Title EN")

    def test_previous_stale_source_hash_marks_unit_source_changed(self):
        article = sample_article()
        previous_hashes = {"title": source_text_hash("Ancien titre FR")}

        report = analyze_translation_sync(article, "en", previous_hashes)
        title_unit = next(unit for unit in report.units if unit.path == "title")

        self.assertEqual(title_unit.status, "source-changed")
        self.assertEqual(title_unit.target_text, "Title EN")
        self.assertEqual(report.source_changed_count, 1)


if __name__ == "__main__":
    unittest.main()
