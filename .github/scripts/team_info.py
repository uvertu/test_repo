import os
import sys
from github import Github, Auth


def get_team_info():
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')

    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)

    print("👥 Участники команды:")
    collaborators = repo.get_collaborators()

    for collaborator in collaborators:
        print(f"Имя: {collaborator.name or collaborator.login}")
        print(f"Email: {collaborator.email}")
        print(f"GitHub: {collaborator.html_url}")

        orgs = collaborator.get_orgs()
        org_names = [org.login for org in orgs]
        if org_names:
            print(f"Организации: {', '.join(org_names)}")
        else:
            print(f"Организации: Не состоит в организациях")

        teams = repo.get_teams()
        if teams.totalCount > 0:
            print("‍Команды в репозитории:")
            for team in teams:
                print(f"Название команды: {team.name}")
                print(f"Описание: {team.description or 'Нет описания'}")

                members = team.get_members()
                member_names = [member.login for member in members]
                if member_names:
                    print(f"Участники команды: {', '.join(member_names)}")
                else:
                    print(f"Участники команды: Нет участников")
        else:
            print("Команды в репозитории: Нет команд")


def check_mr_size():
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('PR_NUMBER')

    if not pr_number:
        print("❌ PR_NUMBER не установлен")
        return False

    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)
    pull_request = repo.get_pull(int(pr_number))

    # Получаем изменения в PR
    additions = pull_request.additions
    deletions = pull_request.deletions
    total_changes = additions + deletions

    # Определяем тип MR по labels или branch name
    mr_type = "feature"  # по умолчанию
    labels = [label.name.lower() for label in pull_request.labels]
    branch_name = pull_request.head.ref.lower()

    if any(label in ['refactor', 'bugfix'] for label in labels):
        mr_type = next(label for label in ['refactor', 'bugfix'] if label in labels)
    elif 'refactor' in branch_name:
        mr_type = 'refactor'
    elif 'bugfix' in branch_name or 'fix' in branch_name:
        mr_type = 'bugfix'
    elif any(label in ['feature', 'feat'] for label in labels):
        mr_type = 'feature'

    # Проверяем размер согласно типу MR
    max_lines = 0
    if mr_type == 'feature':
        max_lines = 300
    elif mr_type == 'refactor':
        max_lines = 400
    elif mr_type == 'bugfix':
        max_lines = 150

    print(f"🔍 Проверка MR #{pr_number}")
    print(f"📊 Тип MR: {mr_type}")
    print(f"📈 Изменения: {total_changes} строк (+{additions}/-{deletions})")
    print(f"📏 Максимально допустимо: {max_lines} строк")

    if total_changes > max_lines:
        print(f"❌ Превышен размер MR! {total_changes} > {max_lines}")
        return False
    else:
        print(f"✅ Размер MR в пределах нормы")
        return True


if __name__ == "__main__":
    # Если передан аргумент 'check-mr', проверяем размер MR
    if len(sys.argv) > 1 and sys.argv[1] == 'check-mr':
        success = check_mr_size()
        sys.exit(0 if success else 1)
    else:
        get_team_info()