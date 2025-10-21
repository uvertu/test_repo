#!/usr/bin/env python3
"""
Script для получения информации о участниках команды через GitHub API
"""

import os
from github import Github, Auth


def get_team_info():
    # Получаем токен из переменных окружения
    token = os.getenv('ORG_ACCESS_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')


    try:
        # Создаем клиент GitHub с правильной аутентификацией
        auth = Auth.Token(token)
        g = Github(auth=auth)
        repo = g.get_repo(repo_name)

        print(f"📊 Информация о команде для репозитория: {repo_name}")
        print("=" * 50)

        print("👥 Участники команды:")
        collaborators = repo.get_collaborators()

        for collaborator in collaborators:
            print(f"\n👤 Имя: {collaborator.name or collaborator.login}")
            print(f"   📧 Email: {collaborator.email or 'Не указан'}")
            print(f"   🔗 GitHub: {collaborator.html_url}")

            # Получаем организации пользователя
            orgs = collaborator.get_organizations()
            org_names = [org.login for org in orgs]
            if org_names:
                print(f"   🏢 Организации: {', '.join(org_names)}")
            else:
                print(f"   🏢 Организации: Не состоит в организациях")

        print("\n" + "=" * 50)

        # Получаем команды репозитория (если репозиторий принадлежит организации)
        try:
            teams = repo.get_teams()
            if teams.totalCount > 0:
                print("👨‍👩‍👧‍👦 Команды в репозитории:")
                for team in teams:
                    print(f"\n   🏷️  Название команды: {team.name}")
                    print(f"   📝 Описание: {team.description or 'Нет описания'}")

                    # Получаем участников команды
                    members = team.get_members()
                    member_names = [member.login for member in members]
                    if member_names:
                        print(f"   👥 Участники команды: {', '.join(member_names)}")
                    else:
                        print(f"   👥 Участники команды: Нет участников")
            else:
                print(
                    "👨‍👩‍👧‍👦 Команды в репозитории: Нет команд (репозиторий принадлежит пользователю, а не организации)")

        except Exception as team_error:
            print(f"👨‍👩‍👧‍👦 Команды в репозитории: Не удалось получить информацию о командах - {team_error}")

        print("\n" + "=" * 50)
        print(f"✅ Всего участников: {collaborators.totalCount}")

    except Exception as e:
        print(f"❌ Ошибка при получении информации: {str(e)}")


if __name__ == "__main__":
    get_team_info()