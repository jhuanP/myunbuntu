pipeline {
    agent any

    stages {
        stage('install dependencies') {
            steps {
                echo 'installing dependencies'
                script{
                    sh 'printenv'
                    sh 'echo $PATH'
                    sh """ 
                        mkdir mythings && 
                        cd mythings && 
                        echo '#!/bin/bash
                            echo "hello world"'> test.sh &&
                        chmod +x test.sh &&
                        ./test.sh
                    
                    """
                    
                }
            }
        }
        stage('install things') {
            steps {
                echo 'installing the things'
                script{
                    sh """
                        sudo apt-get update && 
                        sudo apt install -g node npm && 
                        node -v && 
                        npm -v && 
                        
                    """
            }
        }
    }
        stage('Deploy') {
            steps {
             script{
                dir('mythings')
                echo 'Deploying'
                sh  'npm run'
             }
            }
        }        
    }
  }
