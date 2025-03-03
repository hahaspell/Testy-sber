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
                        curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
                        chmod 700 get_helm.sh
                        echo Ure459605|sudo -S ./get_helm.sh --version v${HELM_VERSION}
                    """
                    sh "helm version"
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
