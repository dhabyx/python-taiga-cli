from taiga_cli.cliparser import parser
from taiga_cli.commands.config import load_config, save_config
from taiga_cli.commands.login import get_api_instance


def set_default_project(project_slug):
    """Set a default project by its slug."""
    config = load_config()
    if not config:
        print("Configuration not found. Please run `taiga config` first.")
        return

    api = get_api_instance()
    if not api:
        print("Unable to authenticate. Please log in using `taiga login`.")
        return

    try:
        projects = api.projects.list()
        project = next((p for p in projects if p.slug == project_slug), None)
        if not project:
            print(f"Project with slug '{project_slug}' not found.")
            return

        config["default_project"] = project_slug
        save_config(config)
        print(f"Default project set to '{project.name}' (slug: {project_slug}).")
    except Exception as e:
        print(f"Error setting default project: {e}")


def list_projects(user_only=True):
    """List projects available to the user or all projects based on the flag."""
    api = get_api_instance()
    if not api:
        print("Unable to authenticate. Please log in using `taiga login`.")
        return

    try:
        params = {
            "order_by": "user_order",
            "slight": True
        }

        if user_only:
            params["member"] = api.me().id

        projects = api.projects.list(**params)

        if projects:
            scope = "your" if user_only else "all"
            print(f"Projects ({scope} projects):")
            for project in projects:
                print(f"- {project.name} (slug: {project.slug})")
        else:
            print("No projects found.")
    except Exception as e:
        print(f"Error fetching projects: {e}")


def list_default_project():
    """List the default configured project."""
    config = load_config()
    if not config:
        print("Configuration not found. Please run `taiga config` first.")
        return

    default_project = config.get("default_project")
    if not default_project:
        print("No default project is set. Use `taiga project set-default <slug>` to configure one.")
        return

    print(f"Default project: {default_project}")


def run(args):
    """Handle the `taiga projects` command."""
    if len(args) < 1:
        parser.print_help()
        return

    command = args[0]

    if command == "ls":
        if "--all" in args:
            list_projects(user_only=False)
        else:
            list_projects(user_only=True)
    elif command == "default":
        list_default_project()
    elif command == "set-default" and len(args) >= 2:
        set_default_project(args[1])
    else:
        parser.print_help()
