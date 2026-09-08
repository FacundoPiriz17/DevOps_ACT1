import os

from flask import Flask, jsonify
from notas import read_notes, write_note, edit_note

app = Flask(__name__)

@app.get("/")
def index():
    return jsonify({
        "status": "ok",
        "message": "API de notas activa"
    })


@app.get("/add/<path:note>")
def add_note(note):
    note = " ".join(note.split())

    if not note:
        return jsonify({
            "error": "La nota no puede estar vacía"
        }), 400

    write_note(note)

    notes = read_notes()

    return jsonify({
        "status": "ok",
        "note": note,
        "total": len(notes)
    }), 201

@app.get("/edit/<int:number>/<path:note>")
def edit_note_route(number, note):
    note = " ".join(note.split())

    if not note:
        return jsonify({
            "error": "La nota no puede estar vacía"
        }), 400

    # El usuario indica el número de nota (1-based) como aparece en /list
    updated = edit_note(number - 1, note)

    if not updated:
        return jsonify({
            "error": f"No existe la nota número {number}"
        }), 404

    notes = read_notes()

    return jsonify({
        "status": "ok",
        "number": number,
        "note": note,
        "total": len(notes)
    })

@app.get("/list")
def list_notes():
    notes = read_notes()

    return jsonify({
        "total": len(notes),
        "notes": notes
    })

if __name__ == "__main__":
    # host 0.0.0.0 para que la app sea alcanzable desde fuera del contenedor.
    # El puerto por defecto (8080) es el que declara pod.yaml.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
