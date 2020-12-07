pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh 'python -V'
                sh 'pip install -r requirements-dev.txt'
		sh 'source /opt/env/dataverse_dv03.env'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest -v'
            }
        }
    }	
}
