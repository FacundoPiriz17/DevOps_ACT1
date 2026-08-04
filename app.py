from flask import Flask, jsonify
from notas import read_notes, write_note

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

@app.get("/list")
def list_notes():
    notes = read_notes()

    return jsonify({
        "total": len(notes),
        "notes": notes
    })

if __name__ == "__main__":
    app.run()