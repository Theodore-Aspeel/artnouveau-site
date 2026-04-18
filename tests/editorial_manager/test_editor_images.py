from pathlib import Path
import tempfile
import unittest

from tools.editorial_manager.editor_images import (
    IMAGE_IMPORT_MAX_BYTES,
    import_editor_image,
    is_valid_editor_image_src,
    list_editor_image_options,
    normalized_image_filename,
)


class EditorImageImportTests(unittest.TestCase):
    def test_normalized_image_filename_keeps_allowed_extension_and_removes_risky_parts(self):
        filename = normalized_image_filename("../Façade Art Deco 2026!!.JPG")

        self.assertEqual(filename, "facade-art-deco-2026.jpg")

    def test_normalized_image_filename_rejects_disallowed_extension(self):
        with self.assertRaises(ValueError):
            normalized_image_filename("notes.txt")

    def test_import_editor_image_copies_under_imported_articles_folder(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = import_editor_image("Maison Demo.PNG", b"fake image", project_root=root)
            copied = root / "src" / result["src"]

            self.assertEqual(result["src"], "assets/images/articles/imported/maison-demo.png")
            self.assertEqual(result["label"], "articles/imported/maison-demo.png")
            self.assertTrue(copied.is_file())
            self.assertEqual(copied.read_bytes(), b"fake image")

    def test_import_editor_image_avoids_collision_with_clear_suffix(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            first = import_editor_image("Maison Demo.png", b"first", project_root=root)
            second = import_editor_image("Maison Demo.png", b"second", project_root=root)

            self.assertEqual(first["src"], "assets/images/articles/imported/maison-demo.png")
            self.assertEqual(second["src"], "assets/images/articles/imported/maison-demo-2.png")
            self.assertEqual((root / "src" / second["src"]).read_bytes(), b"second")

    def test_imported_image_is_available_in_catalog_and_valid_for_editor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = import_editor_image("New Hero.webp", b"fake image", project_root=root)
            options = list_editor_image_options(root)

            self.assertIn(result, options)
            self.assertTrue(is_valid_editor_image_src(result["src"], root))

    def test_import_editor_image_rejects_empty_and_oversized_payloads(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            with self.assertRaises(ValueError):
                import_editor_image("empty.png", b"", project_root=root)
            with self.assertRaises(ValueError):
                import_editor_image("large.png", b"x" * (IMAGE_IMPORT_MAX_BYTES + 1), project_root=root)


if __name__ == "__main__":
    unittest.main()
