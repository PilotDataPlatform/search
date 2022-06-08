pipeline {

    agent { label 'small' }

    environment {
        imagename = 'ghcr.io/pilotdataplatform/search'
        commit = sh(returnStdout: true, script: 'git describe --always').trim()
        registryCredential = 'pilot-ghcr'
    }

    stages {

        stage('DEV: Git clone') {
            when { branch 'develop' }
            steps {
                git branch: 'develop',
                    url: 'https://github.com/PilotDataPlatform/search.git',
                    credentialsId: 'pilot-gh'
            }
        }

        stage('DEV: Build and push image') {
            when { branch 'develop' }
            steps {
                script {
                    docker.withRegistry('https://ghcr.io', registryCredential) {
                        customImage = docker.build('$imagename:$commit', '--target search-image .')
                        customImage.push()
                    }
                }
            }
        }

        stage('DEV: Remove image') {
            when { branch 'develop' }
            steps {
                sh 'docker rmi $imagename:$commit'
            }
        }

        stage('DEV: Deploy') {
            when { branch 'develop' }
            steps {
                build(job: '/VRE-IaC/UpdateAppVersion', parameters: [
                    [$class: 'StringParameterValue', name: 'TF_TARGET_ENV', value: 'dev'],
                    [$class: 'StringParameterValue', name: 'TARGET_RELEASE', value: 'search'],
                    [$class: 'StringParameterValue', name: 'NEW_APP_VERSION', value: "$commit"]
                ])
            }
        }

    }

}
