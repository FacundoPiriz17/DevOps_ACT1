# DevOps_ACT1

## Pruebas unitarias

Desde la raíz del proyecto, con Python y las dependencias instaladas:

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Las pruebas usan `unittest` de la biblioteca estándar. Cubren las rutas Flask,
la validación y normalización de notas, el orden alfabético y la lectura/escritura
del almacenamiento. Las rutas se prueban con mocks y la persistencia con archivos
temporales; no se modifica `/data/notes.txt` ni se necesita iniciar un servidor.
