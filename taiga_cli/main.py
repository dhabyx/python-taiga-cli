from taiga_cli.cliparser import parser
from taiga_cli.commands import config, login, project, sprint, stories


def main():
    parser.add_argument('--version', action='version', version='taiga-cli 1.1')
    subparsers = parser.add_subparsers(title='Commands', dest='command')

    # Comando: config
    config_parser = subparsers.add_parser('config', help='Configure server and user')
    config_parser.set_defaults(func=config.run)

    # Comando: login
    login_parser = subparsers.add_parser('login', help='Login to a taiga instance')
    login_parser.set_defaults(func=login.run)

    # Comando: projects
    project_parser = subparsers.add_parser('project', help='Manage projects')
    project_parser.add_argument('ls', help='List user projects')
    project_parser.add_argument('default', help='Get default project')
    project_parser.add_argument('set-default', nargs='*', help='Set default project')
    project_parser.add_argument('--all', action='store_true', help='List all projects')
    project_parser.set_defaults(func=lambda args: project.run([
        *args.subcommand,
        '--all' if args.all else ''
    ]))

    # Comando: sprint
    sprint_parser = subparsers.add_parser('sprint', help='Manage milestones (sprint)')
    sprint_parser.add_argument('ls', help='List user sprints')
    sprint_parser.add_argument('set-default', nargs='*', help='Set default sprint')
    sprint_parser.add_argument('default', help='Get default sprint')
    sprint_parser.add_argument('user-stats', help='Display user stats of sprint')
    sprint_parser.add_argument('user-stories', help='Display user stories of sprint')
    sprint_parser.add_argument('--user', help='Filter sprint by username', default=None)
    sprint_parser.add_argument('--status', choices=['open', 'closed'], help='Filter sprint by status', default=None)
    sprint_parser.add_argument('--sprint', help='Filter sprint by slug', default=None)
    sprint_parser.add_argument('--project', help='Filter sprint by project slug', default=None)
    sprint_parser.add_argument('--all-users', action='store_true', help='List stories without filtering by user')
    sprint_parser.set_defaults(func=lambda args: sprint.run([
        *args.subcommand,
        f"--user={args.user}" if args.user else "",
        f"--status={args.status}" if args.status else "",
        f"--sprint={args.sprint}" if args.sprint else "",
        f"--project={args.project}" if args.project else "",
        "--all-users" if args.all_users else ""
    ]))

    # Comando: stories
    stories_parser = subparsers.add_parser('stories', help='Manage stories')
    stories_subparsers = stories_parser.add_subparsers(title='Subcommands', dest='stories_command')

    # Subcomando: stories ls
    stories_ls_parser = stories_subparsers.add_parser('ls', help='List user stories')
    stories_ls_parser.add_argument('--user', help='Filter stories by username', default=None)
    stories_ls_parser.add_argument('--status', choices=['open', 'closed'], help='Filter stories by status',
                                   default=None)
    stories_ls_parser.add_argument('--sprint', help='Filter stories by sprint slug', default=None)
    stories_ls_parser.add_argument('--project', help='Filter project by sprint slug', default=None)
    stories_ls_parser.add_argument('--all-users', action='store_true', help='List stories without filtering by user')
    stories_ls_parser.add_argument('--all-sprints', action='store_true', help='List stories from all sprints')
    stories_ls_parser.set_defaults(func=lambda args: stories.run([
        "ls",
        f"--user={args.user}" if args.user else "",
        f"--status={args.status}" if args.status else "",
        f"--sprint={args.sprint}" if args.sprint else "",
        f"--project={args.project}" if args.project else "",
        "--all-users" if args.all_users else "",
        "--all-sprints" if args.all_sprints else ""
    ]))

    # Subcomando: stories stats
    stories_stats_parser = stories_subparsers.add_parser('stats', help='Stats of stories')
    stories_stats_parser.add_argument('--user', help='Filter stories by username', default=None)
    stories_stats_parser.add_argument('--status', choices=['open', 'closed'], help='Filter stories by status',
                                      default=None)
    stories_stats_parser.add_argument('--sprint', help='Filter stories by sprint slug', default=None)
    stories_stats_parser.add_argument('--project', help='Filter project by sprint slug', default=None)
    stories_stats_parser.add_argument('--all-users', action='store_true', help='List stories without filtering by user')
    stories_stats_parser.add_argument('--all-sprints', action='store_true', help='List stories from all sprints')
    stories_stats_parser.set_defaults(func=lambda args: stories.run([
        "stats",
        f"--user={args.user}" if args.user else "",
        f"--status={args.status}" if args.status else "",
        f"--sprint={args.sprint}" if args.sprint else "",
        f"--project={args.project}" if args.project else "",
        "--all-users" if args.all_users else "",
        "--all-sprints" if args.all_sprints else ""
    ]))

    # Subcomando: stories stats-detailed
    stories_stats_detailed_parser = stories_subparsers.add_parser('stats-detailed', help='Stats and stories of stories')
    stories_stats_detailed_parser.add_argument('--user', help='Filter stories by username', default=None)
    stories_stats_detailed_parser.add_argument('--status', choices=['open', 'closed'], help='Filter stories by status',
                                               default=None)
    stories_stats_detailed_parser.add_argument('--sprint', help='Filter stories by sprint slug', default=None)
    stories_stats_detailed_parser.add_argument('--project', help='Filter project by sprint slug', default=None)
    stories_stats_detailed_parser.add_argument('--all-users', action='store_true',
                                               help='List stories without filtering by user')
    stories_stats_detailed_parser.add_argument('--all-sprints', action='store_true',
                                               help='List stories from all sprints')
    stories_stats_detailed_parser.set_defaults(func=lambda args: stories.run([
        "stats-detailed",
        f"--user={args.user}" if args.user else "",
        f"--status={args.status}" if args.status else "",
        f"--sprint={args.sprint}" if args.sprint else "",
        f"--project={args.project}" if args.project else "",
        "--all-users" if args.all_users else "",
        "--all-sprints" if args.all_sprints else ""
    ]))

    # Parse arguments
    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
