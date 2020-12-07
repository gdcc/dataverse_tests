pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -V
                    pip3 install -r requirements-dev.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    source /opt/env/dataverse_dv03.env
                    pytest -v
                '''
            }
        }
    }
}
