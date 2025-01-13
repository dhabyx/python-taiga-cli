import os
import json
from getpass import getpass
from taiga import TaigaAPI
from pathlib import Path
import datetime
from taiga_cli.commands.config import load_config, ensure_config_directory
from taiga_cli.cliparser import parser


# Define paths for the token file
CONFIG_DIR = Path.home() / ".config" / "taiga-cli"
TOKEN_FILE = CONFIG_DIR / "token.json"


def save_token(token_data):
    """Save the token data to a file."""
    ensure_config_directory()
    with TOKEN_FILE.open('w') as token_file:
        json.dump(token_data, token_file, indent=4)


def load_token():
    """Load the token data from the file."""
    if TOKEN_FILE.exists():
        with TOKEN_FILE.open('r') as token_file:
            return json.load(token_file)
    return {}


def is_token_valid(token_data):
    """Check if the stored token is still valid."""
    if not token_data:
        return False

    expiration = token_data.get("expiration")
    if not expiration:
        return False

    expiration_time = datetime.datetime.fromisoformat(expiration)
    return datetime.datetime.now() < expiration_time


def login_and_save_token(api_url, username, password):
    """Perform login and save the token."""
    api = TaigaAPI(host=api_url)
    try:
        api.auth(username=username, password=password)
        token = api.token
        expiration = (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat()

        save_token({
            "token": token,
            "expiration": expiration
        })

        print(f"Login successful! Token valid until {expiration}")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False


def get_api_instance():
    """Get a TaigaAPI instance with the stored token if valid."""
    config = load_config()
    if not config:
        print("Configuration not found. Please run `taiga config`.")
        return None

    token_data = load_token()
    if is_token_valid(token_data):
        return TaigaAPI(token=token_data["token"], host=config["api_url"])
    else:
        print("Token is invalid or expired. Attempting re-login...")
        username = config.get("username")
        api_url = config.get("api_url")
        password = getpass("Enter your Taiga password: ")

        if login_and_save_token(api_url, username, password):
            return TaigaAPI(token=load_token()["token"], host=config["api_url"])
        else:
            print("Re-login failed. Please run `taiga login` manually.")
            return None


def get_api_and_defaults(project_slug=None, sprint_slug=None, all_sprints=False):
    """Retrieve API instance and defaults for project and sprint."""
    api = get_api_instance()
    if not api:
        raise RuntimeError("Unable to authenticate. Please log in using `taiga login`.")

    config = load_config()

    if not project_slug:
        project_slug = config.get("default_project")
        if not project_slug:
            raise ValueError("No default project set. Use `taiga projects set-default <slug>`.")

    if not sprint_slug and not all_sprints:
        sprint_slug = config.get("default_sprint")
        if not sprint_slug:
            raise ValueError("No default sprint set. Use `taiga sprint set-default <slug>`.")

    return api, project_slug, sprint_slug


def get_api_and_project(project_slug=None):
    """Retrieve API instance and project."""
    api = get_api_instance()
    if not api:
        raise RuntimeError("Unable to authenticate. Please log in using `taiga login`.")

    config = load_config()

    if not project_slug:
        project_slug = config.get("default_project")
        if not project_slug:
            raise ValueError("No default project set. Use `taiga projects set-default <slug>`.")

    return api, project_slug


def run(args):
    """Handle the `taiga login` command."""
    config = load_config()
    if not config:
        print("Configuration not found. Please run `taiga config` first.")
        return

    print("--- Login to Taiga CLI ---")

    api_url = config["api_url"]
    username = config["username"]
    password = getpass("Enter your Taiga password: ")

    if login_and_save_token(api_url, username, password):
        print("You are now logged in.")
    else:
        print("Login failed. Please check your credentials and try again.")
