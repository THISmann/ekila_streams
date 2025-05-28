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

        Stage for SonarQube code analysis
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


        // stage('Security Scan & Code Analysis') {
        //     steps {
        //         script {
        //             // --------------------------------------------
        //             // 1. SonarQube Analysis (with Java 17 enforcement)
        //             // --------------------------------------------
        //             try {
        //                 def scannerHome = tool name: 'SonarQube Scanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                        
        //                 // Force Java 17 for SonarQube on Mac M1
        //                 withEnv(["JAVA_HOME=${tool 'openjdk-17'}", "PATH+JDK=${tool 'openjdk-17'}/bin"]) {
        //                     withSonarQubeEnv('SonarQube') { // Match your Jenkins SonarQube server name
        //                         sh """
        //                             ${scannerHome}/bin/sonar-scanner \
        //                             -Dsonar.projectKey=RadioManagementDjango \
        //                             -Dsonar.sources=. \
        //                             -Dsonar.host.url=\${SONAR_HOST_URL} \
        //                             -Dsonar.login=\${SONAR_AUTH_TOKEN} \
        //                             -Dsonar.projectBaseDir=${WORKSPACE} \
        //                             -Dsonar.python.version=3 \
        //                             -Dsonar.exclusions=**/tests/**,**/migrations/**,**/static/** \
        //                             -X
        //                         """
        //                     }
        //                 }
        //             } catch (Exception e) {
        //                 error "SonarQube analysis failed: ${e.message}"
        //             }

        //             // --------------------------------------------
        //             // 2. Trivy Vulnerability Scan (Container/FS)
        //             // --------------------------------------------
        //             try {
        //                 // Install Trivy if not present
        //                 sh '''
        //                     if ! command -v trivy &> /dev/null; then
        //                         brew install aquasecurity/trivy/trivy
        //                     fi
        //                 '''
                        
        //                 // Run Trivy scans (both filesystem and container)
        //                 sh '''
        //                     echo "Running Trivy filesystem scan..."
        //                     trivy fs --security-checks vuln,config ${WORKSPACE} --exit-code 1
                            
        //                     # Uncomment if you have Dockerfiles to scan
        //                     # echo "Running Trivy container scan..."
        //                     # trivy image --input ${WORKSPACE}/Dockerfile --exit-code 1
        //                 '''
        //             } catch (Exception e) {
        //                 unstable "Trivy scan found vulnerabilities: ${e.message}"
        //                 // Continue pipeline but mark as unstable
        //             }
        //         }
        //     }
        // }
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
