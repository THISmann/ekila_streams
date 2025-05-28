pipeline {
    agent any
    stages {
        stage('Scan Sonarqube') {
            steps {
                echo 'SonarQube Scan !! '
                withSonarQubeEnv('SonarQube') { // 'SonarQube' is the name of the SonarQube server configured in Jenkins
                    sh 'mvn clean package sonar:sonar' // Runs Maven build and SonarQube scan
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                // Ex: sh 'npm test' (pour Node.js)
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Ex: sh 'docker push my-image'
            }
        }
    }
}