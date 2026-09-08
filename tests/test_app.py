import unittest
from unittest.mock import patch

import app as app_module


class NotesApiTests(unittest.TestCase):
    def setUp(self):
        config = patch.dict(app_module.app.config, TESTING=True)
        config.start()
        self.addCleanup(config.stop)
        self.client = app_module.app.test_client()

    def test_index_returns_application_metadata(self):
        with patch.object(app_module, "APP_TITLE", "Mis notas"), patch.object(
            app_module, "INSTANCE_NAME", "test-instance"
        ):
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(response.get_json(), {
            "status": "ok",
            "message": "Mis notas, API de notas activa",
            "instance": "test-instance",
            "version": "V2",
        })

    @patch("app.read_notes", return_value=["Anterior", "Nueva nota"])
    @patch("app.write_note")
    def test_add_normalizes_whitespace_and_returns_total(self, write, read):
        response = self.client.get("/add/%20Nueva%20%20nota%20")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {
            "status": "ok", "note": "Nueva nota", "total": 2,
        })
        write.assert_called_once_with("Nueva nota")
        read.assert_called_once_with()

    @patch("app.read_notes")
    @patch("app.write_note")
    def test_add_rejects_whitespace_without_accessing_storage(self, write, read):
        for note in (" ", "\t", " \t  "):
            with self.subTest(note=repr(note)):
                with app_module.app.test_request_context():
                    response, status = app_module.add_note(note)
                self.assertEqual(status, 400)
                self.assertEqual(response.get_json(), {
                    "error": "La nota no puede estar vacía",
                })
        write.assert_not_called()
        read.assert_not_called()

    @patch("app.read_notes", return_value=[])
    @patch("app.write_note")
    def test_whitespace_url_returns_bad_request(self, write, read):
        response = self.client.get("/add/%20%20")
        self.assertEqual(response.status_code, 400)
        write.assert_not_called()
        read.assert_not_called()

    @patch("app.read_notes", return_value=["Comprar café/pan"])
    @patch("app.write_note")
    def test_add_preserves_unicode_and_slashes(self, write, read):
        response = self.client.get("/add/Comprar%20caf%C3%A9/pan")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["note"], "Comprar café/pan")
        write.assert_called_once_with("Comprar café/pan")

    @patch("app.read_notes", return_value=["zeta", "Beta", "alfa", "Beta"])
    def test_list_sorts_case_insensitively_and_preserves_duplicates(self, read):
        response = self.client.get("/list")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "total": 4,
            "notes": ["alfa", "Beta", "Beta", "zeta"],
            "message": "Notas ordenadas alfabéticamente",
            "version": "v2",
        })
        self.assertEqual(read.return_value, ["zeta", "Beta", "alfa", "Beta"])
        read.assert_called_once_with()

    @patch("app.read_notes", return_value=[])
    def test_list_handles_empty_storage(self, read):
        response = self.client.get("/list")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["notes"], [])
        self.assertEqual(response.get_json()["total"], 0)


if __name__ == "__main__":
    unittest.main()
