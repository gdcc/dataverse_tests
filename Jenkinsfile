pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -V
                    python3 -m venv venv
                    ./venv/bin/pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Create data') {
            when { expression {env.SUITE == "data"} }
            steps {
                sh './venv/bin/python utils collect'
                sh './venv/bin/python utils generate'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx tests/dataverse/suite_$SUITE.py
                '''
            }
        }

        stage('Cleanup') {
            steps {
                sh 'rm -rf venv'
            }
        }

    }

	post {
		always {
			junit 'report.xml'
		}
	}
}
