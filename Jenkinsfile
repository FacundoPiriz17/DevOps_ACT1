// Pipeline de CI para la API de notas.
//
// Requisitos en el nodo de Jenkins (agente Windows):
//   - python en el PATH (3.10+), con el modulo venv disponible
//   - docker CLI en el PATH y el daemon corriendo
//   - plugin "JUnit" instalado, para publicar el reporte de tests
//
// El pipeline corre los tests y, solo si pasan, buildea la imagen.
// No hace push a ningun registry ni despliega al cluster.

pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'devopsnotes'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        VENV       = '.venv'
        // Los tests aislan el archivo de notas con una fixture, pero dejamos
        // NOTES_FILE dentro del workspace como red de seguridad: nunca se debe
        // escribir en la ruta de produccion (/data/notes.txt).
        NOTES_FILE = "${env.WORKSPACE}\notes-ci.txt"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                bat """
                    python -m venv %VENV%
                    call %VENV%\Scripts\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements-dev.txt
                """
            }
        }

        stage('Test') {
            steps {
                bat """
                    call %VENV%\Scripts\activate.bat
                    pytest -v --junitxml=test-results.xml
                """
            }
        }

        stage('Build imagen') {
            steps {
                bat """
                    docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                    docker tag %IMAGE_NAME%:%IMAGE_TAG% %IMAGE_NAME%:latest
                    docker images %IMAGE_NAME%
                """
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-results.xml'
        }
        success {
            echo "Build OK - imagen ${IMAGE_NAME}:${IMAGE_TAG} construida"
        }
        failure {
            echo 'Build fallido - revisar el reporte de tests'
        }
        cleanup {
            deleteDir()
        }
    }
}
