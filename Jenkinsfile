pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh 'python -V'
                sh 'pip install -r requirements/development.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest -v'
            }
        }

        stage('Cleanup') {
            deleteDir()
        }
    }
}
