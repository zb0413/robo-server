// Jenkinsfile (Declarative Pipeline)

pipeline {
    agent any // Runs on any available Jenkins agent

    environment {
        // Define environment variables
        // TARGET_SERVER_IP = "your_server_ip" // Example: "192.168.1.100"
        // TARGET_SERVER_USER = "your_server_user" // Example: "deploy_user"
        // TARGET_SERVER_PATH = "/opt/resource-manager" // Example: Path on server to deploy the app
        // SSH_CREDENTIALS_ID = "jenkins-ssh-credentials-id" // ID of SSH credentials stored in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                // This will typically be a Git checkout step
                // For this example, assuming SCM is configured in Jenkins job
                checkout scm
            }
        }

        stage('Build Docker Images Locally') {
            // Optional: Build images locally first to catch build errors early
            // Or, build directly on the target server if preferred (simplifies SCP)
            // If building on the target server, this stage can be skipped or modified.
            // For now, let's assume we build images on the Jenkins agent first
            // to ensure Dockerfiles are correct, then we SCP the whole project.
            // The target server will then use its own Docker to build from the Dockerfiles.
            steps {
                echo 'Building Docker images locally (for validation)...'
                // This step is more about validating the Dockerfiles can build.
                // The actual images used for deployment will be built on the target server
                // from the SCP'd source code to ensure consistency.
                sh 'docker-compose -f docker-compose.yml build --no-cache backend frontend'
            }
        }

        stage('Deploy to Target Server') {
            steps {
                echo "Starting deployment to server: ${env.TARGET_SERVER_IP}"
                sshagent(credentials: ["${env.SSH_CREDENTIALS_ID}"]) {
                    // Ensure variables are properly quoted if they contain spaces or special chars
                    sh '''
                        echo "Connecting to ${TARGET_SERVER_USER}@${TARGET_SERVER_IP}"
                        
                        echo "Creating target directory if it doesn't exist: ${TARGET_SERVER_PATH}"
                        ssh ${TARGET_SERVER_USER}@${TARGET_SERVER_IP} "mkdir -p ${TARGET_SERVER_PATH}"
                        
                        echo "Copying project files to ${TARGET_SERVER_USER}@${TARGET_SERVER_IP}:${TARGET_SERVER_PATH}"
                        # Using rsync for efficiency, but scp is also an option
                        # Ensure rsync is installed on both Jenkins agent and target server if using rsync
                        # Using tar to bundle and then extract can also be efficient
                        # For simplicity with scp, let's assume we are in the workspace root
                        # We might need to exclude .git, Jenkins workspace artifacts, etc.
                        # A common pattern is to archive the workspace and scp the archive.

                        tar czf resource-manager-app.tar.gz --exclude=.git --exclude=workspace@tmp .
                        scp resource-manager-app.tar.gz ${TARGET_SERVER_USER}@${TARGET_SERVER_IP}:${TARGET_SERVER_PATH}/resource-manager-app.tar.gz
                        
                        echo "Extracting project files on the server"
                        ssh ${TARGET_SERVER_USER}@${TARGET_SERVER_IP} "cd ${TARGET_SERVER_PATH} && tar xzf resource-manager-app.tar.gz && rm resource-manager-app.tar.gz"
                        
                        echo "Executing docker-compose on the server to update the application"
                        # This assumes docker-compose.yml is at the root of the copied project
                        # The --env-file option can be used if environment variables are managed in a .env file
                        ssh ${TARGET_SERVER_USER}@${TARGET_SERVER_IP} "cd ${TARGET_SERVER_PATH} && docker-compose -f docker-compose.yml pull db && docker-compose -f docker-compose.yml up -d --build backend frontend"
                        
                        echo "Deployment complete."
                    '''
                }
            }
        }

        stage('Cleanup Workspace') {
            // Optional: Clean up workspace on Jenkins agent
            steps {
                echo 'Cleaning up workspace...'
                deleteDir() // Deletes the current directory from the workspace
                cleanWs()   // Deletes all files from the workspace, including untracked files
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline executed successfully!'
            // Add notifications (e.g., email, Slack)
        }
        failure {
            echo 'Pipeline failed!'
            // Add notifications
        }
    }
}
```
