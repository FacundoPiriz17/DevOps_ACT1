from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import notas


class NotesStorageTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.notes_file = Path(directory.name) / "nested" / "data" / "notes.txt"
        storage = patch.object(notas, "NOTES_FILE", self.notes_file)
        storage.start()
        self.addCleanup(storage.stop)

    def test_ensure_file_creates_parent_directories_and_empty_file(self):
        notas.ensure_file()
        self.assertTrue(self.notes_file.is_file())
        self.assertEqual(self.notes_file.read_text(encoding="utf-8"), "")

    def test_ensure_file_does_not_truncate_existing_notes(self):
        notas.ensure_file()
        self.notes_file.write_text("Existente\n", encoding="utf-8")
        notas.ensure_file()
        self.assertEqual(self.notes_file.read_text(encoding="utf-8"), "Existente\n")

    def test_read_missing_file_returns_empty_list(self):
        self.assertEqual(notas.read_notes(), [])
        self.assertTrue(self.notes_file.is_file())

    def test_read_strips_whitespace_and_ignores_blank_lines(self):
        notas.ensure_file()
        self.notes_file.write_text("  Primera  \n\n \t\nSegunda\t\n", encoding="utf-8")
        self.assertEqual(notas.read_notes(), ["Primera", "Segunda"])

    def test_read_preserves_order_duplicates_and_unicode(self):
        notas.ensure_file()
        self.notes_file.write_text("Última\nÁrbol 🌳\nÚltima\n", encoding="utf-8")
        self.assertEqual(notas.read_notes(), ["Última", "Árbol 🌳", "Última"])

    def test_write_creates_missing_file_with_newline(self):
        notas.write_note("Primera")
        self.assertEqual(self.notes_file.read_text(encoding="utf-8"), "Primera\n")

    def test_write_appends_without_overwriting_existing_notes(self):
        notas.write_note("Primera")
        notas.write_note("Café ☕")
        notas.write_note("Primera")
        self.assertEqual(
            self.notes_file.read_text(encoding="utf-8"),
            "Primera\nCafé ☕\nPrimera\n",
        )


if __name__ == "__main__":
    unittest.main()
