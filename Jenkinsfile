pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build') {
            steps { sh 'pip install -r requirements.txt' }
        }
        stage('Test') {
            steps { sh 'pytest --maxfail=1 --disable-warnings -q' }
        }
        stage('Code Quality') {
            steps {
                sh """
                sonar-scanner \
                  -Dsonar.projectKey=ACEest_Fitness \
                  -Dsonar.sources=. \
                  -Dsonar.host.url=http://localhost:9000 \
                  -Dsonar.login=$SONAR_TOKEN
                """
            }
        }
    }
}