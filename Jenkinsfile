pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/THISmann/ekila_streams']])
            }
        }

        stage('SCM') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQube Scanner'
                    withSonarQubeEnv() {
                         sh" ${SCANNER_HOME**}**}/bin/sonar-scanner \
                         -Dsonar.projectKey=simple_webapp \
                         -Dsonar.sources=. "
                    }
                }
            }
        }
    }
}