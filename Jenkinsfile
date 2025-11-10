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
    }
}