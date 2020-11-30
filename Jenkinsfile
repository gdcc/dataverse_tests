pipeline {
    agent {
        docker { image 'python:3.6.12-slim-buster' }
    }

    stages {
        stage('Setup') {
            steps {
                sh 'python -V'
                sh 'pip install -r requirements/development.txt'
            }
        }

        stage('Test') {
            steps {

            }
        }

        stage('Cleanup') {
            deleteDir()
        }
    }
}
