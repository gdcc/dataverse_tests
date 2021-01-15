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
                    . /opt/env/dataverse_dv05.env
                    ./venv/bin/python -m pytest -v --junit-xml=report.xml --cache-clear -rsx    tests/dataverse/test_api.py \
                                                                                                tests/dataverse/test_homepage.py \
                                                                                                tests/dataverse/test_metadata_server.py \
                                                                                                tests/dataverse/test_resources.py \
                                                                                                tests/dataverse/test_robots_txt.py \
                                                                                                tests/dataverse/test_search.py \
                                                                                                tests/dataverse/test_sitemap.py \
                                                                                                tests/dataverse/test_user_authentication.py \
                                                                                                tests/dataverse/test_user_profile.py
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
