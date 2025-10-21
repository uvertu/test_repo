#!/usr/bin/env python3
"""
Script для получения информации о участниках команды через GitHub API
"""

import os
from github import Github


def get_team_info():
    # Получаем токен из переменных окружения
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ GITHUB_TOKEN не установлен")
        return

    # Получаем информацию о репозитории из переменных окружения GitHub Actions
    repo_name = os.getenv('GITHUB_REPOSITORY')
    if not repo_name:
        print("❌ GITHUB_REPOSITORY не установлен")
        return

    try:
        # Создаем клиент GitHub
        g = Github(token)
        repo = g.get_repo(repo_name)

        print(f"📊 Информация о команде для репозитория: {repo_name}")
        print("=" * 50)

        # Получаем collaborators (участников с доступом к репозиторию)
        print("👥 Участники команды:")
        collaborators = repo.get_collaborators()

        for collaborator in collaborators:
            print(f"\n👤 Имя: {collaborator.name or collaborator.login}")
            print(f"   📧 Email: {collaborator.email or 'Не указан'}")
            print(f"   🔗 GitHub: {collaborator.html_url}")

            # Получаем организации пользователя
            orgs = collaborator.get_orgs()
            org_names = [org.login for org in orgs]
            if org_names:
                print(f"   🏢 Организации: {', '.join(org_names)}")
            else:
                print(f"   🏢 Организации: Не состоит в организациях")

            # Получаем команды пользователя в этом репозитории
            teams = collaborator.get_teams()
            team_names = [team.name for team in teams if team.repo_id == repo.id]
            if team_names:
                print(f"   👨‍👩‍👧‍👦 Команды в репозитории: {', '.join(team_names)}")

        print("\n" + "=" * 50)
        print(f"✅ Всего участников: {collaborators.totalCount}")

    except Exception as e:
        print(f"❌ Ошибка при получении информации: {str(e)}")


if __name__ == "__main__":
    get_team_info()