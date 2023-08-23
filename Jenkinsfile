
pipeline {
    agent any
    stages {
        stage("Prepare") {
            steps {
                sh "true"
            }
        }
        stage("Build") {
            steps {
                script {
                    def apiImage = docker.build("api:jenkins-pipeline-$BUILD_ID")
                }
            }
        }
        stage("Test") {
            steps {
                sh "true"
            }
        }
        stage("Deploy") {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
