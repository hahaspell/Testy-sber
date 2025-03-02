import subprocess
import os

# Конфигурация
KUBECONFIG = "path/to/kubeconfig"  # Укажите путь к kubeconfig
HELM_VERSION = "3.12.0"  # Версия Helm
CHART_NAME = "my-app"  # Имя Helm Chart
RELEASE_NAME = "my-app-release"  # Имя релиза
NAMESPACE = "default"  # Namespace в Kubernetes
REPO_URL = "https://github.com/your-username/your-repo.git"  # URL репозитория
BRANCH = "main"  # Ветка репозитория

def run_command(command, check=True):
    """Выполняет команду в терминале."""
    result = subprocess.run(command, shell=True, check=check, text=True)
    return result

def checkout_code():
    """Выполняет checkout кода из репозитория."""
    print("Checkout кода из репозитория...")
    run_command(f"git clone -b {BRANCH} {REPO_URL}")

def install_helm():
    """Устанавливает Helm."""
    print("Установка Helm...")
    run_command(f"""
        curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
        chmod 700 get_helm.sh
        ./get_helm.sh --version v{HELM_VERSION}
    """)
    run_command("helm version")

def deploy_with_helm():
    """Развертывает приложение с использованием Helm."""
    print("Развертывание приложения с использованием Helm...")
    run_command(f"""
        helm upgrade --install {RELEASE_NAME} ./{CHART_NAME} \
            --namespace {NAMESPACE} \
            --kubeconfig {KUBECONFIG}
    """)

def verify_deployment():
    """Проверяет состояние развернутого приложения."""
    print("Проверка состояния развернутого приложения...")
    run_command(f"kubectl get pods -n {NAMESPACE} -l app={RELEASE_NAME} --kubeconfig {KUBECONFIG}")
    run_command(f"kubectl get svc -n {NAMESPACE} -l app={RELEASE_NAME} --kubeconfig {KUBECONFIG}")

def main():
    try:
        # Шаг 1: Checkout кода
        checkout_code()

        # Шаг 2: Установка Helm
        install_helm()

        # Шаг 3: Развертывание приложения
        deploy_with_helm()

        # Шаг 4: Проверка состояния
        verify_deployment()

        print("Приложение успешно развернуто!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при развертывании приложения: {e}")

if __name__ == "__main__":
    main()
