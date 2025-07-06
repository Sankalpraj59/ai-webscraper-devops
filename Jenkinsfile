pipeline {
    agent any
    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ai-webscraper .'
            }
        }
        stage('Run App Container') {
            steps {
                sh 'docker stop ai-webscraper-app || true'
                sh 'docker rm ai-webscraper-app || true'
                sh 'docker run -d -p 8501:8501 --env-file .env --name ai-webscraper-app ai-webscraper'
            }
        }
        stage('Verify Container') {
            steps {
                sh 'sleep 5'
                sh 'docker ps'
                sh 'docker logs ai-webscraper-app || echo "Container failed"'
            }
        }
    }
}

