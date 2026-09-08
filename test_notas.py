# -*- coding: utf-8 -*-
from notas import ensure_file, read_notes, write_note, edit_note


def test_ensure_file_crea_archivo_y_directorios(tmp_path, monkeypatch):
    import notas

    anidado = tmp_path / "uno" / "dos" / "notes.txt"
    monkeypatch.setattr(notas, "NOTES_FILE", anidado)

    ensure_file()

    assert anidado.exists()


def test_ensure_file_es_idempotente(notes_file):
    ensure_file()
    write_note("hola")
    ensure_file()

    assert read_notes() == ["hola"]


def test_read_notes_sin_archivo_devuelve_lista_vacia(notes_file):
    assert not notes_file.exists()
    assert read_notes() == []


def test_write_note_agrega_al_final(notes_file):
    write_note("primera")
    write_note("segunda")
    write_note("tercera")

    assert read_notes() == ["primera", "segunda", "tercera"]


def test_read_notes_descarta_lineas_en_blanco_y_hace_strip(notes_file):
    notes_file.parent.mkdir(parents=True, exist_ok=True)
    notes_file.write_text("  primera  \n\n   \nsegunda\n", encoding="utf-8")

    assert read_notes() == ["primera", "segunda"]


def test_edit_note_reemplaza_solo_el_indice_indicado(notes_file):
    write_note("primera")
    write_note("segunda")
    write_note("tercera")

    assert edit_note(1, "editada") is True
    assert read_notes() == ["primera", "editada", "tercera"]


def test_edit_note_indice_negativo_no_modifica_nada(notes_file):
    write_note("primera")

    assert edit_note(-1, "editada") is False
    assert read_notes() == ["primera"]


def test_edit_note_indice_fuera_de_rango_no_modifica_nada(notes_file):
    write_note("primera")

    assert edit_note(5, "editada") is False
    assert read_notes() == ["primera"]


def test_edit_note_sobre_archivo_vacio_devuelve_false(notes_file):
    assert edit_note(0, "editada") is False
    assert read_notes() == []


def test_notas_con_acentos_hacen_round_trip(notes_file):
    write_note("comprar pan y azúcar — desayuno")
    write_note("revisar la configuración")

    edit_note(0, "reunión de planificación")

    assert read_notes() == [
        "reunión de planificación",
        "revisar la configuración",
    ]
