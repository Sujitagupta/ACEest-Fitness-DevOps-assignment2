pipeline {
  agent any
  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
    DOCKERHUB_REPO = 'yourdockerhubusername/aceest'
    KUBE_CONFIG_CREDENTIALS = 'kubeconfig'
    SONARQUBE = 'sonarqube'
  }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Unit Test') {
      steps { sh 'pytest -q --junitxml=reports/junit.xml --cov=app --cov-report=xml:reports/coverage.xml' }
      post { always { junit 'reports/junit.xml' } }
    }
    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv("${SONARQUBE}") {
          sh 'sonar-scanner -Dsonar.projectKey=ACEest-Fitness'
        }
      }
    }
    stage('Quality Gate') {
      steps { script { timeout(time: 2, unit: 'MINUTES') { def qg = waitForQualityGate(); if (qg.status != 'OK') { error "Pipeline aborted: ${qg.status}" } } } }
    }
    stage('Build & Push Docker') {
      steps { script { def tag = "v${env.BUILD_NUMBER}"; docker.withRegistry('', "${DOCKERHUB_CREDENTIALS}") { def img = docker.build("${env.DOCKERHUB_REPO}:${tag}", "--build-arg APP_VERSION=${tag} ."); img.push(); img.push('latest'); env.IMAGE_TAG = tag } } }
    }
    stage('Deploy') {
      steps {
        withCredentials([file(credentialsId: "${KUBE_CONFIG_CREDENTIALS}", variable: 'KUBECONF')]) {
          sh 'export KUBECONFIG=$KUBECONF; kubectl apply -f kubernetes/namespace.yaml; kubectl set image -n aceest deploy/aceest-deployment aceest=${DOCKERHUB_REPO}:${IMAGE_TAG} --record'
        }
      }
    }
  }
  post { success { echo "Pipeline completed." } failure { echo "Pipeline failed." } }
}
