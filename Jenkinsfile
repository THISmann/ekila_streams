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
                    sh 'java -version'
                    
                    // Use withSonarQubeEnv to inject SonarQube server details
                    withSonarQubeEnv(["JAVA_HOME=${tool 'openjdk-17'}"]) { // Replace 'SonarQube' with your SonarQube server name in Jenkins
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
            echo 'test premier !'
        }
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
