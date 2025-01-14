from taiga_cli.commands.login import get_api_instance, get_api_and_project, get_api_and_defaults
from taiga_cli.commands.project import load_config, save_config
from taiga_cli.cliparser import parser


def get_project_and_sprint(api, project_slug, sprint_slug=None):
    """Retrieve the project and optional sprint objects based on slugs."""
    projects = api.projects.list()
    project = next((p for p in projects if p.slug == project_slug), None)
    if not project:
        raise ValueError(f"Project with slug '{project_slug}' not found.")

    if sprint_slug:
        sprints = api.milestones.list(project=project.id)
        sprint = next((s for s in sprints if s.slug == sprint_slug), None)
        if not sprint:
            raise ValueError(f"Sprint with slug '{sprint_slug}' not found in project '{project.name}'.")
        return project, sprint

    return project, None


def list_sprints(project_slug=None):
    """List sprints (milestones) for a given project slug or the default project."""
    api, project_slug = get_api_and_project(project_slug)

    try:
        project, _ = get_project_and_sprint(api, project_slug)
        sprints = api.milestones.list(project=project.id)

        if sprints:
            print(f"Sprints for project '{project.name}':")
            for sprint in sprints:
                status_text = "Open" if not sprint.closed else "Closed"
                print(f"- {sprint.name} (slug: {sprint.slug}, Status: {status_text})")
        else:
            print(f"No sprints found for project '{project.name}'.")
    except Exception as e:
        print(f"Error fetching sprints: {e}")


def sprint_user_stats(sprint_slug=None, project_slug=None, user=None, all_users=False):
    """List user statistics for a specific sprint or project, optionally filtered by user."""
    try:
        api, project_slug, sprint_slug = get_api_and_defaults(project_slug=project_slug, sprint_slug=sprint_slug, all_sprints=False)
        project, sprint = get_project_and_sprint(api, project_slug, sprint_slug)

        stories = sprint.user_stories if sprint else []
        user_stats = {}
        total_stories = len(stories)
        open_stories = sum(1 for story in stories if not story.is_closed)
        closed_stories = total_stories - open_stories
        progress_percentage = (closed_stories / total_stories * 100) if total_stories > 0 else 0
        if user is None:
            user = api.me().username

        for story in stories:
            assigned_to = story.assigned_to_extra_info.get("username") if story.assigned_to_extra_info else "Unassigned"
            if not all_users and assigned_to != user:
                continue

            points = story.total_points or 0

            if assigned_to not in user_stats:
                user_stats[assigned_to] = {
                    "stories": 0,
                    "points": 0,
                    "full_name": story.assigned_to_extra_info.get("full_name_display") if story.assigned_to_extra_info else "Unassigned",
                    "open_stories": 0,
                    "closed_stories": 0,
                }

            user_stats[assigned_to]["stories"] += 1
            user_stats[assigned_to]["points"] += points
            if story.is_closed:
                user_stats[assigned_to]["closed_stories"] += 1
            else:
                user_stats[assigned_to]["open_stories"] += 1

        print(f"User statistics for sprint '{sprint.name if sprint else 'Backlog'}':")
        print(f"Total stories: {total_stories}, Open: {open_stories}, Closed: {closed_stories}, Progress: {progress_percentage:.2f}%")
        for user, stats in user_stats.items():
            user_progress = (stats["closed_stories"] / stats["stories"] * 100) if stats["stories"] > 0 else 0
            print(f"- {user}: {stats['stories']} stories (Open: {stats['open_stories']}, Closed: {stats['closed_stories']}), {stats['points']} points, Progress: {user_progress:.2f}%")
    except Exception as e:
        print(f"Error fetching user statistics: {e}")


def list_user_stories(project_slug=None, sprint_slug=None, user=None, all_users=False):
    """List user stories for a specific sprint or project."""
    try:
        api, project_slug, sprint_slug = get_api_and_defaults(project_slug=project_slug, sprint_slug=sprint_slug, all_sprints=False)
        project, sprint = get_project_and_sprint(api, project_slug, sprint_slug)

        stories = sprint.user_stories if sprint else []
        print(f"User stories for sprint '{sprint.name if sprint else 'Backlog'}':")

        if user is None:
            user = api.me().username

        for story in stories:
            assigned_to = story.assigned_to_extra_info.get("username") if story.assigned_to_extra_info else "Unassigned"
            if not all_users and assigned_to != user:
                continue

            status = "Closed" if story.is_closed else "Open"
            points = story.total_points or 0
            print(f"- {story.subject} (Assigned to: {assigned_to}, Status: {status}, Points: {points})")
    except Exception as e:
        print(f"Error fetching user stories: {e}")


def set_default_sprint(sprint_slug):
    """Set a default sprint by its slug."""
    config = load_config()
    if not config:
        print("Configuration not found. Please run `taiga config` first.")
        return

    api = get_api_and_project(None)[0]

    try:
        project_slug = config.get("default_project")
        if not project_slug:
            print("No default project is set. Use `taiga project set-default <slug>` first.")
            return

        _, sprint = get_project_and_sprint(api, project_slug, sprint_slug)
        config["default_sprint"] = sprint_slug
        save_config(config)
        print(f"Default sprint set to '{sprint.name}' (slug: {sprint.slug}).")
    except Exception as e:
        print(f"Error setting default sprint: {e}")


def list_default_sprint():
    """List the default configured sprint."""
    config = load_config()
    if not config:
        print("Configuration not found. Please run `taiga config` first.")
        return

    default_sprint = config.get("default_sprint")
    if not default_sprint:
        print("No default sprint is set. Use `taiga sprint set-default <slug>` to configure one.")
        return

    print(f"Default sprint: {default_sprint}")


def run(args):
    """Handle the `taiga sprint` command."""
    if len(args) < 1:
        parser.print_help()
        return

    command = args[0]
    user = None
    project_slug = None
    sprint_slug = None
    all_users = False

    for arg in args[1:]:
        if arg.startswith("--user="):
            user = arg.split("=", 1)[1]
        elif arg.startswith("--project="):
            project_slug = arg.split("=", 1)[1]
        elif arg.startswith("--sprint="):
            sprint_slug = arg.split("=", 1)[1]
        elif arg == "--all-users":
            all_users = True

    if command == "ls":
        list_sprints(project_slug=project_slug)
    elif command == "user-stats":
        sprint_user_stats(sprint_slug=sprint_slug, project_slug=project_slug, user=user, all_users=all_users)
    elif command == "user-stories":
        list_user_stories(project_slug=project_slug, sprint_slug=sprint_slug, user=user, all_users=all_users)
    else:
        parser.print_help()

