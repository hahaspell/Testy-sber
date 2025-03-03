pipeline {
    agent any

    environment {
        KUBECONFIG = credentials('kubeconfig')  // Укажите kubeconfig
        HELM_VERSION = "3.12.0"  // Версия Helm
        CHART_NAME = "nginx-chart"  // Имя Helm Chart
        RELEASE_NAME = "nginx-release"  // Имя релиза
        NAMESPACE = "default"  // Namespace в Kubernetes
        GITHUB_TOKEN = credentials('github-token')  // Укажите ID вашего credential
        PATH = "/home/jenkins/bin:${env.PATH}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/hahaspell/Testy-sber.git'
            }
        }

        stage('Install Helm') {
            steps {
                script {
                    sh """
                        mkdir -p /home/jenkins/bin
                        curl -LO https://get.helm.sh/helm-v3.12.0-linux-amd64.tar.gz
                        tar -zxvf helm-v3.12.0-linux-amd64.tar.gz
                        mv linux-amd64/helm /home/jenkins/bin/helm
                        echo 'PATH updated to: $PATH'
                        helm version
                    """
                }
            }
        }

        stage('Deploy with Helm') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        helm upgrade --install nginx-release ./nginx-chart \
                            --namespace default \
                            --kubeconfig ${KUBECONFIG}
                    """
                }
            }
        }

        // Шаг 4: Проверка состояния развернутого приложения
        stage('Verify Deployment') {
            steps {
                script {
                    sh """
                        kubectl get pods -n ${NAMESPACE} -l app=nginx --kubeconfig ${KUBECONFIG}
                    """
                    sh """
                        kubectl get svc -n ${NAMESPACE} -l app=nginx --kubeconfig ${KUBECONFIG}
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Приложение успешно развернуто!"
        }
        failure {
            echo "Ошибка при развертывании приложения."
        }
    }
}
