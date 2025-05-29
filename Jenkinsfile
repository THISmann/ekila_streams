pipeline {
    // Run on any available agent
    agent any
    environment {
        DOCKER_IMAGE = "ekilastreams-back:1.0"
        COMPOSE_PROJECT_NAME = "ekila_streams"
    }
    stages {
        // Stage to checkout code from Git repository
        stage('Checkout') {
            steps {
                echo 'Checking out code from Git repository'
                checkout scmGit(
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[url: 'https://github.com/THISmann/ekila_streams']]
                )
            }
        }

        stage('Build Docker Image with Docker Compose') {
            steps {
                script {
                    echo "Building Docker image ${DOCKER_IMAGE} using docker-compose..."
                    sh 'docker compose -f docker-compose.yml up -d --build '
                }
            }
        }

        stage('Trivy Security Scan') {
            steps {
                script {
                    echo "Scanning ${DOCKER_IMAGE} with Trivy for vulnerabilities..."
                    sh '''
                        docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v $HOME/.cache/trivy:/root/.cache/trivy \
                        aquasec/trivy:latest image \
                        --exit-code 1 \
                        --severity CRITICAL,HIGH \
                        --no-progress \
                        --format table \
                        ${DOCKER_IMAGE}
                    '''
                }
            }
        }

        // Stage for SonarQube code analysis
        stage('SonarQube Analysis') {
            steps {
                script {
                    // Get the SonarQube Scanner home directory
                    def scannerHome = tool name: 'SonarQube Scanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    echo "SonarQube Scanner Home: ${scannerHome}"
                    
                    // Ensure workspace is accessible
                    sh 'java -version'
                    
                    // Use withSonarQubeEnv to inject SonarQube server details
                    withSonarQubeEnv() { // Replace 'SonarQube' with your SonarQube server name in Jenkins
                        // sh """
                        //     ${scannerHome}/bin/sonar-scanner \
                        //     -Dsonar.projectKey=RadioManagementDjango \
                        //     -Dsonar.sources=. \
                        //     -Dsonar.host.url=\${SONAR_HOST_URL} \
                        //     -Dsonar.login=\${SONAR_AUTH_TOKEN} \
                        //     -Dsonar.projectBaseDir=${WORKSPACE} \
                        //     -Dsonar.python.version=3 \
                        //     -Dsonar.exclusions=**/tests/**,**/migrations/**,**/static/** \
                        //     -X
                        // """
                            sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
    }

    // Post-build actions
    post {
        always {
            // sh 'ls -la ${WORKSPACE}/.scannerwork/report-task.txt || echo "report-task.txt not found"'
            // echo 'test premier !'
            echo "Cleaning up Docker images and workspace..."
            sh 'docker-compose -f docker-compose.yml down --rmi local'
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
