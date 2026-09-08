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

## Build y despliegue con Jenkins

El archivo `Jenkinsfile`, en la raíz del repositorio, define el pipeline:
checkout, verificación de Docker, construcción de la imagen, tests unitarios,
despliegue y comprobación HTTP dentro del contenedor. Si los tests fallan,
no se reemplaza la aplicación que está ejecutándose.

En el job **DevOpsAct1**, abrir **Configurar → Pipeline** y establecer:

| Campo | Valor |
| --- | --- |
| Definition | Pipeline script from SCM |
| SCM | Git |
| Repository URL | `https://github.com/FacundoPiriz17/DevOps_ACT1.git` |
| Branch Specifier | `*/main` |
| Script Path | `Jenkinsfile` |

Seleccionar credenciales si el repositorio es privado. Subir el `Jenkinsfile`
a GitHub antes de ejecutar **Build Now**. Con esta configuración, `checkout scm`
obtiene el código correspondiente al pipeline y no hace falta pegar el script
en la interfaz de Jenkins.

El agente debe ser Linux y disponer del cliente Docker y acceso al daemon.
La instalación actual usa un solo nodo; si se agregan agentes, sustituir
`agent any` por la etiqueta del nodo elegido para el despliegue, de modo que
el contenedor y el volumen permanezcan en el mismo host Docker.

Jenkins sigue en `http://localhost:8081`. La app se publica en
`http://localhost:8082`, con el mapeo `8082:5000`, cuando el host Docker es
el equipo local. Si es remoto, usar su dirección. Las notas se conservan
en el volumen `api-notas-data`, montado en `/data`.

El despliegue detiene y reemplaza el contenedor `api-notas`, con una breve
interrupción y sin rollback automático. La comprobación HTTP valida Flask
dentro del contenedor; no comprueba el acceso externo al puerto 8082.
La limpieza final elimina el workspace del job, no las imágenes Docker.

`Dockerfile` construye la app. `Dockerfile.jenkins` prepara la imagen del
servidor Jenkins con el cliente Docker. `Jenkinsfile` coordina los pasos
del build cada vez que se ejecuta el job.
