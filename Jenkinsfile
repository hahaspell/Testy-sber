pipeline {
    agent any

    environment {
        KUBECONFIG = credentials('kubeconfig')  // Укажите kubeconfig
        HELM_VERSION = "3.12.0"  // Версия Helm
        CHART_NAME = "nginx-chart"  // Имя Helm Chart
        RELEASE_NAME = "nginx-release"  // Имя релиза
        NAMESPACE = "default"  // Namespace в Kubernetes
        GITHUB_TOKEN = credentials('github-token')  // Укажите ID вашего credential
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: "https://${GITHUB_TOKEN}@github.com/hahaspell/Testy-sber.git"
            }
        }

        // Шаг 2: Установка Helm
stage('Install Helm') {
    steps {
        script {
            sh """
                mkdir -p /home/jenkins/bin
                curl -LO https://get.helm.sh/helm-v3.12.0-linux-amd64.tar.gz
                tar -zxvf helm-v3.12.0-linux-amd64.tar.gz
                mv linux-amd64/helm /home/jenkins/bin/helm
                export PATH=/home/jenkins/bin:$PATH
                echo 'PATH updated to: $PATH'
                helm version
            """
        }
    }
}


        // Шаг 3: Развертывание приложения с использованием Helm
        stage('Deploy with Helm') {
            steps {
                script {
                    sh """
                        helm upgrade --install ${RELEASE_NAME} ./${CHART_NAME} \
                            --namespace ${NAMESPACE} \
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
