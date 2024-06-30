pipeline {
    agent any

    environment {
        EC2_HOST = credentials('host')
    }

    stages {
        stage('Deploy on EC2') {
            steps {
                script {
                    sshagent(['ssh']) {
                        sh "ssh -o StrictHostKeyChecking=no \${EC2_HOST} 'sudo su -c \" cd TEP-Backend && git pull origin main && docker compose stop web && docker compose build web && docker compose up\"'"
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
