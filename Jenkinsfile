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
                    try {
                        // Define SonarQube scanner tool
                        def scannerHome = tool 'SonarQube Scanner'

                        // Run SonarQube analysis with environment configuration
                        withSonarQubeEnv('SonarQube') { // Ensure 'SonarQube' matches your Jenkins SonarQube server name
                            sh """
                                ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=simple_webapp \
                                -Dsonar.sources=.
                            """
                        }
                    } catch (Exception e) {
                        echo "SonarQube Analysis failed: ${e.message}"
                        error 'Aborting due to SonarQube analysis failure'
                    }
                }
            }
        }
    }

    // Post-build actions
    post {
        always {
            echo 'Pipeline execution completed'
        }
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
