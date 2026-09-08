import os
from pathlib import Path
from threading import Lock


NOTES_FILE = Path(os.getenv("NOTES_FILE", "/data/notes.txt"))
lock = Lock()


def ensure_file():
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    NOTES_FILE.touch(exist_ok=True)


def read_notes():
    ensure_file()

    with lock:
        with NOTES_FILE.open("r", encoding="utf-8") as file:
            return [
                line.strip()
                for line in file
                if line.strip()
            ]


def write_note(note):
    ensure_file()

    with lock:
        with NOTES_FILE.open("a", encoding="utf-8") as file:
            file.write(note + "\n")


def edit_note(index, note):
    ensure_file()

    with lock:
        with NOTES_FILE.open("r", encoding="utf-8") as file:
            notes = [
                line.strip()
                for line in file
                if line.strip()
            ]

        if index < 0 or index >= len(notes):
            return False

        notes[index] = note

        with NOTES_FILE.open("w", encoding="utf-8") as file:
            for existing in notes:
                file.write(existing + "\n")

        return True