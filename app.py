import os

from flask import Flask, jsonify
from notas import read_notes, write_note

app = Flask(__name__)

APP_TITLE = os.getenv("APP_TITLE", "API de notas")
INSTANCE_NAME = os.getenv("INSTANCE_NAME", "local")
@app.get("/")
def index():
    return jsonify({
        "status": "ok",
        "message": APP_TITLE + ", API de notas activa",
        "instance": INSTANCE_NAME,
        "version" : "V2"
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
    notes = sorted(notes, key=str.lower)

    return jsonify({
        "total": len(notes),
        "notes": notes,
        "message": "Notas ordenadas alfabéticamente",
        "version": "v2"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)