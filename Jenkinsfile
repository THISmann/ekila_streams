pipeline {
    // Run on any available agent
    agent any

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

        // Stage for SonarQube code analysis
        stage('SonarQube Analysis') {
            steps {
                script {
                    // Get the SonarQube Scanner home directory
                    def scannerHome = tool name: 'SonarQube Scanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    echo "SonarQube Scanner Home: ${scannerHome}"
                    
                    // Ensure workspace is accessible
                    sh 'pwd && ls -la'
                    
                    // Use withSonarQubeEnv to inject SonarQube server details
                    withSonarQubeEnv() { // Replace 'SonarQube' with your SonarQube server name in Jenkins
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=RadioManagementDjango \
                            -Dsonar.sources=. 
                        """
                    }
                }
            }
        }
    }

    // Post-build actions
    post {
        always {
            sh 'ls -la ${WORKSPACE}/.scannerwork/report-task.txt || echo "report-task.txt not found"'
        }
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
