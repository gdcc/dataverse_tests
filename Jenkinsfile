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

        stage('Test') {
            steps {
                sh '''
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx tests/dataverse/test_api.py
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx tests/dataverse/test_homepage.py
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx tests/dataverse/test_metadata_server.py
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx tests/dataverse/test_resources.py
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx tests/dataverse/test_robots_txt.py
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx tests/dataverse/test_search.py
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx tests/dataverse/test_sitemap.py
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx tests/dataverse/test_user_authentication.py
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx tests/dataverse/test_user_profile.py
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
