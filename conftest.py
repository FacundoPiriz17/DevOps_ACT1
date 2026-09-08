import pytest

import notas
from app import app as flask_app


@pytest.fixture(autouse=True)
def notes_file(tmp_path, monkeypatch):
    """Aisla cada test en su propio archivo de notas.

    Se parchea el atributo del modulo (y no la variable de entorno) para no
    depender del orden de import: las funciones de notas.py leen NOTES_FILE
    en tiempo de ejecucion, asi que esto tambien cubre las rutas de app.py.
    """
    path = tmp_path / "notes.txt"
    monkeypatch.setattr(notas, "NOTES_FILE", path)

    return path


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as test_client:
        yield test_client
