def runCmd(String cmd) {
    if (isUnix()) {
        sh cmd
    } else {
        bat cmd
    }
}

pipeline {
    agent any

    environment {
        IMAGE_NAME = "tanmayfalke7/loan-approval-app"
        IMAGE_TAG  = "v1"
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo 'Fetching latest source code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                runCmd 'python -m pip install --upgrade pip && pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo 'Running unit tests on loan eligibility logic...'
                runCmd 'python -m unittest test_app.py -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
                runCmd "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline succeeded: Source checked out, tests passed, and Docker image built.'
        }
        failure {
            echo 'CI Pipeline failed: Check the stage logs above for errors.'
        }
    }
}