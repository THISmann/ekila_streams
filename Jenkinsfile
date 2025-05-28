pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building the project...'
                // Ex: sh 'mvn clean package' (pour Java/Maven)
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