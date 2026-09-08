# -*- coding: utf-8 -*-


def test_index_responde_ok(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_add_crea_la_nota(client):
    response = client.get("/add/mi%20nota")

    assert response.status_code == 201

    body = response.get_json()

    assert body["status"] == "ok"
    assert body["note"] == "mi nota"
    assert body["total"] == 1

    assert client.get("/list").get_json()["notes"] == ["mi nota"]


def test_add_multiples_notas_mantiene_el_orden(client):
    client.get("/add/primera")
    response = client.get("/add/segunda")

    assert response.get_json()["total"] == 2

    body = client.get("/list").get_json()

    assert body["total"] == 2
    assert body["notes"] == ["primera", "segunda"]


def test_add_colapsa_espacios_internos(client):
    response = client.get("/add/hola%20%20%20mundo")

    assert response.status_code == 201
    assert response.get_json()["note"] == "hola mundo"


def test_add_solo_espacios_devuelve_400(client):
    response = client.get("/add/%20%20")

    assert response.status_code == 400
    assert "error" in response.get_json()
    assert client.get("/list").get_json()["total"] == 0


def test_list_vacio(client):
    response = client.get("/list")

    assert response.status_code == 200
    assert response.get_json() == {"total": 0, "notes": []}


def test_edit_usa_numeracion_1_based(client):
    client.get("/add/primera")
    client.get("/add/segunda")

    response = client.get("/edit/1/editada")

    assert response.status_code == 200

    body = response.get_json()

    assert body["number"] == 1
    assert body["note"] == "editada"
    assert body["total"] == 2

    assert client.get("/list").get_json()["notes"] == ["editada", "segunda"]


def test_edit_nota_inexistente_devuelve_404(client):
    client.get("/add/primera")

    response = client.get("/edit/99/editada")

    assert response.status_code == 404
    assert "error" in response.get_json()
    assert client.get("/list").get_json()["notes"] == ["primera"]


def test_edit_indice_cero_devuelve_404(client):
    client.get("/add/primera")

    response = client.get("/edit/0/editada")

    assert response.status_code == 404
    assert client.get("/list").get_json()["notes"] == ["primera"]


def test_edit_con_nota_vacia_devuelve_400_sin_tocar_el_archivo(client):
    client.get("/add/primera")

    response = client.get("/edit/1/%20%20")

    assert response.status_code == 400
    assert "error" in response.get_json()
    assert client.get("/list").get_json()["notes"] == ["primera"]
