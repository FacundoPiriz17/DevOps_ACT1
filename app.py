import os
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify

app = Flask(__name__)

NOTES_FILE = Path(os.environ.get('NOTES_FILE', '/data/notes.txt'))
_lock = Lock()


def ensure_file():
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    NOTES_FILE.touch(exist_ok=True)


def read_notes():
    if not NOTES_FILE.exists():
        return []
    with NOTES_FILE.open('r', encoding='utf-8') as f:
        return [line.rstrip('\n') for line in f if line.strip()]


@app.route('/')
def index():
    return jsonify(
        status='ok',
        message='API de notas activa',
        endpoints=['/', '/add/<note>', '/list'],
    )


@app.route('/add/<path:note>')
def add(note):
    text = note.strip()
    if not text:
        return jsonify(error='La nota no puede estar vacia'), 400

    # Una nota por linea: los saltos de linea internos se aplanan.
    text = ' '.join(text.splitlines())

    with _lock:
        ensure_file()
        with NOTES_FILE.open('a', encoding='utf-8') as f:
            f.write(text + '\n')
        total = len(read_notes())

    return jsonify(status='ok', note=text, total=total), 201


@app.route('/list')
def list_notes():
    with _lock:
        notes = read_notes()
    return jsonify(total=len(notes), notes=notes)


if __name__ == '__main__':
    ensure_file()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
