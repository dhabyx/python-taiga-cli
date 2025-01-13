from taiga_cli.commands.login import get_api_and_defaults
from taiga_cli.cliparser import parser


def fetch_stories(api, project_slug, sprint_slug, all_sprints, all_users, user, status):
    """Fetch user stories based on provided filters."""
    projects = api.projects.list()
    project = next((p for p in projects if p.slug == project_slug), None)
    if not project:
        raise ValueError(f"Project with slug '{project_slug}' not found.")

    query_params = {"project": project.id}

    if not all_sprints:
        sprints = api.milestones.list(project=project.id)
        sprint = next((s for s in sprints if s.slug == sprint_slug), None)
        if not sprint:
            raise ValueError(f"Sprint with slug '{sprint_slug}' not found in project '{project.name}'.")
        query_params["milestone"] = sprint.id

    if not all_users:
        query_params["assigned_to"] = api.me().id

    if user:
        users = api.users.list(project=project.id)
        user_details = next((u for u in users if u.username == user), None)
        if user_details:
            query_params["assigned_to"] = user_details.id
        else:
            raise ValueError(f"User '{user}' not found in project '{project.name}'.")

    if status == "open":
        query_params["is_closed"] = False
    elif status == "closed":
        query_params["is_closed"] = True

    return api.user_stories.list(**query_params), project


def list_assigned_stories(project_slug=None, sprint_slug=None, all_sprints=False, all_users=False, user=None, status=None):
    """List user stories based on project and milestone configuration."""
    try:
        api, project_slug, sprint_slug = get_api_and_defaults(project_slug, sprint_slug, all_sprints)
        stories, project = fetch_stories(api, project_slug, sprint_slug, all_sprints, all_users, user, status)

        if stories:
            print(f"User Stories for Project '{project.name}':")
            stories_by_sprint = {}
            for story in stories:
                sprint_name = story.milestone_name or "Backlog"
                if sprint_name not in stories_by_sprint:
                    stories_by_sprint[sprint_name] = []
                stories_by_sprint[sprint_name].append(story)

            for sprint_name, sprint_stories in stories_by_sprint.items():
                print(f"* Sprint '{sprint_name}':")
                for story in sprint_stories:
                    status = "Closed" if story.is_closed else "Open"
                    print(f"  * {story.subject} (Assigned to: {story.assigned_to_extra_info.get('username')}, Status: {status}, Points: {story.total_points or 0})")
        else:
            print(f"No user stories found for Project '{project.name}'.")
    except Exception as e:
        print(f"Error fetching user stories: {e}")


def user_stories_stats(detailed=False, project_slug=None, sprint_slug=None, all_sprints=False, all_users=False, user=None, status=None):
    """List statistics for user stories based on filters."""
    try:
        api, project_slug, sprint_slug = get_api_and_defaults(project_slug, sprint_slug, all_sprints)
        stories, project = fetch_stories(api, project_slug, sprint_slug, all_sprints, all_users, user, status)

        if not stories:
            print(f"No user stories found for Project '{project.name}'.")
            return

        print(f"User Story Statistics for Project '{project.name}':")
        stories_by_sprint = {}
        for story in stories:
            sprint_name = story.milestone_name or "Backlog"
            if sprint_name not in stories_by_sprint:
                stories_by_sprint[sprint_name] = []
            stories_by_sprint[sprint_name].append(story)

        for sprint_name, sprint_stories in stories_by_sprint.items():
            total_points = sum(story.total_points or 0 for story in sprint_stories)
            open_points = sum(story.total_points or 0 for story in sprint_stories if not story.is_closed)
            closed_stories = sum(1 for story in sprint_stories if story.is_closed)
            open_stories = len(sprint_stories) - closed_stories
            progress_percentage = (closed_stories / len(sprint_stories) * 100) if sprint_stories else 0

            print(f"* Sprint '{sprint_name}':")
            print(f"  - Total Points: {total_points}")
            print(f"  - Open Points: {open_points}")
            print(f"  - Closed Stories: {closed_stories}")
            print(f"  - Open Stories: {open_stories}")
            print(f"  - Progress: {progress_percentage:.2f}%")

            if detailed:
                print("\nDetailed User Stories:")
                for story in sprint_stories:
                    status = "Closed" if story.is_closed else "Open"
                    print(f"  * {story.subject} (Assigned to: {story.assigned_to_extra_info.get('username')}, Status: {status}, Points: {story.total_points or 0})")
    except Exception as e:
        print(f"Error fetching user story statistics: {e}")


def run(args):
    """Handle the `taiga stories` command."""
    if len(args) < 1:
        parser.print_help()
        return

    command = args[0]
    user = None
    status = None
    sprint_slug = None
    all_users = False
    all_sprints = False
    project_slug = None

    for arg in args[1:]:
        if arg.startswith("--user="):
            user = arg.split("=", 1)[1]
        elif arg.startswith("--status="):
            status = arg.split("=", 1)[1]
        elif arg.startswith("--sprint="):
            sprint_slug = arg.split("=", 1)[1]
        elif arg.startswith("--project="):
            project_slug = arg.split("=", 1)[1]
        elif arg == "--all-users":
            all_users = True
        elif arg == "--all-sprints":
            all_sprints = True

    if command == "ls":
        list_assigned_stories(project_slug=project_slug, user=user, status=status, sprint_slug=sprint_slug, all_users=all_users, all_sprints=all_sprints)
    elif command == "stats":
        user_stories_stats(project_slug=project_slug, detailed=False, sprint_slug=sprint_slug, all_users=all_users, all_sprints=all_sprints, user=user, status=status)
    elif command == "stats-detailed":
        user_stories_stats(project_slug=project_slug, detailed=True, sprint_slug=sprint_slug, all_users=all_users, all_sprints=all_sprints, user=user, status=status)
    else:
        parser.print_help()
