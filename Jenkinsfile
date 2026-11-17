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
                echo 'Creating an isolated Python environment and installing dependencies...'
                script {
                    if (isUnix()) {
                        sh '''python -m venv .venv
                              .venv/bin/python -m pip install --upgrade pip
                              .venv/bin/python -m pip install -r requirements.txt'''
                    } else {
                        bat '''python -m venv .venv
                               .venv\\Scripts\\python -m pip install --upgrade pip
                               .venv\\Scripts\\python -m pip install -r requirements.txt'''
                    }
                }
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo 'Running unit tests on loan eligibility logic...'
                script {
                    if (isUnix()) {
                        sh '.venv/bin/python -m unittest test_app.py -v'
                    } else {
                        bat '.venv\\Scripts\\python -m unittest test_app.py -v'
                    }
                }
            }
        }

        stage('Build Application') {
            steps {
                echo 'Compiling the application as a build verification step...'
                runCmd 'python -m compileall -q app.py'
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline succeeded: source checked out, dependencies installed, tests passed, and application built.'
        }
        failure {
            echo 'CI Pipeline failed: Check the stage logs above for errors.'
        }
    }
}
