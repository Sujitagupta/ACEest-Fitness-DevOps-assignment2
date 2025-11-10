pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        DOCKERHUB_REPO = 'sujitagupta/aceest-fitness'
        KUBE_CONFIG_CREDENTIALS = 'kubeconfig'
        SONARQUBE = 'sonarqube'
    }
    stages {
        stage('Checkout') { 
            steps { 
                checkout scm 
            } 
        }

	stage('Unit Test') {
    		steps {
        		sh '''
            		/Library/Frameworks/Python.framework/Versions/3.13/bin/pytest -q \
            		--junitxml=reports/junit.xml \
            		--cov=app \
            		--cov-report=xml:reports/coverage.xml
        		'''
    		}
    		post { always { junit 'reports/junit.xml' } }
	}

	stage('SonarQube Analysis') {
    steps {
        withSonarQubeEnv('sonarqube') {
            withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                sh '''
                    /opt/homebrew/bin/sonar-scanner \
                        -Dsonar.projectKey=ACEest-Fitness \
                        -Dsonar.host.url=http://localhost:9000 \
                        -Dsonar.login=$SONAR_TOKEN
                '''
            }
        }
    }
}	

        stage('Quality Gate') {
            steps { 
                script { 
                    timeout(time: 5, unit: 'MINUTES') { 
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') { 
                            error "Pipeline aborted: ${qg.status}" 
                        } 
                    } 
                } 
            }
        }

stage('Build and Push Docker') {
    steps {
        script {
            sh '''
                /usr/local/bin/docker build -t myimage:latest .
                /usr/local/bin/docker tag myimage:latest yourdockerhubuser/myimage:latest
                /usr/local/bin/docker push yourdockerhubuser/myimage:latest
            '''
        }
    }
}


        stage('Deploy') {
            steps {
                withCredentials([file(credentialsId: "${KUBE_CONFIG_CREDENTIALS}", variable: 'KUBECONF')]) {
                    sh 'export KUBECONFIG=$KUBECONF; kubectl apply -f kubernetes/namespace.yaml; kubectl set image -n aceest deploy/aceest-deployment aceest=${DOCKERHUB_REPO}:${IMAGE_TAG} --record'
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed."
        }
        failure {
            echo "Pipeline failed."
        }
    }
}

