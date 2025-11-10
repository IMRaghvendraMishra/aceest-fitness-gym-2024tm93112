pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Install Dependencies') { steps { sh 'pip install -r requirements.txt' } }
    stage('Run Tests') { steps { sh 'pytest -v' } }
    stage('Code Quality') {
      steps {
        sh '''
        sonar-scanner \
          -Dsonar.projectKey=ACEest_Fitness \
          -Dsonar.sources=. \
          -Dsonar.host.url=http://localhost:9000 \
          -Dsonar.login=$SONAR_TOKEN
        '''
      }
    }
    stage('Build Docker Image') {
      steps { sh 'docker build -t aceest-fitness:latest .' }
    }
    stage('Push to Docker Hub') {
      steps {
        withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_PASS')]) {
          sh '''
          echo $DOCKER_PASS | docker login -u imrmishra --password-stdin
          docker tag aceest-fitness imrmishra/aceest-fitness:latest
          docker push imrmishra/aceest-fitness:latest
          '''
        }
      }
    }
    stage('Deploy to Minikube') {
      steps {
        sh '''
        kubectl apply -f k8s/deployment.yaml
        kubectl apply -f k8s/service.yaml
        '''
      }
    }
  }
}