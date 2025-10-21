#!/usr/bin/env python3
"""
Script для получения информации о участниках команды через GitHub API
"""

import os
from github import Github, Auth


def get_team_info():
    token = os.getenv('ORG_ACCESS_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')

    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ GITHUB_TOKEN не установлен")
        return

    repo_name = os.getenv('GITHUB_REPOSITORY')
    if not repo_name:
        print("❌ GITHUB_REPOSITORY не установлен")
        return

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

            orgs = collaborator.get_organizations()
            orgs = collaborator.get_orgs()
            org_names = [org.login for org in orgs]
            if org_names:
                print(f"   🏢 Организации: {', '.join(org_names)}")
            else:
                print(f"   🏢 Организации: Не состоит в организациях")

        print("\n" + "=" * 50)

        try:
            teams = repo.get_teams()
            if teams.totalCount > 0:
                print("👨‍👩‍👧‍👦 Команды в репозитории:")
                for team in teams:
                    print(f"\n   🏷️  Название команды: {team.name}")
                    print(f"   📝 Описание: {team.description or 'Нет описания'}")

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