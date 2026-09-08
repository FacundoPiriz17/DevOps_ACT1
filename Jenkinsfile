// Pipeline de CI para la API de notas.
//
// Requisitos en el nodo de Jenkins (agente Linux):
//   - docker CLI en el PATH y acceso al daemon (docker.sock montado)
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
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker run --rm \
                        -v "$WORKSPACE":/app \
                        -w /app \
                        -e NOTES_FILE=/app/notes-ci.txt \
                        python:3.12-slim \
                        sh -c "pip install --upgrade pip && pip install -r requirements-dev.txt && pytest -v --junitxml=test-results.xml"
                '''
            }
        }

        stage('Build imagen') {
            steps {
                sh '''
                    docker build -t "$IMAGE_NAME:$IMAGE_TAG" .
                    docker tag "$IMAGE_NAME:$IMAGE_TAG" "$IMAGE_NAME:latest"
                    docker images "$IMAGE_NAME"
                '''
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