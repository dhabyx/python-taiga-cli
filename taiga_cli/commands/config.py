import os
import json
from getpass import getpass
from taiga import TaigaAPI
from pathlib import Path
import platform


def get_config_dir():
    """Determine the appropriate configuration directory based on the OS."""
    if platform.system() == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "taiga-cli"
    else:  # Default for Linux and others
        return Path.home() / ".config" / "taiga-cli"


CONFIG_DIR = get_config_dir()
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_config_directory():
    """Ensure the configuration directory exists."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def save_config(data):
    """Save the configuration data to a file."""
    with CONFIG_FILE.open('w') as config_file:
        json.dump(data, config_file, indent=4)


def load_config():
    """Load the configuration data from the file."""
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open('r') as config_file:
            return json.load(config_file)
    return {}


def validate_credentials(api_url, username, password):
    """Validate the user credentials with Taiga server."""
    api = TaigaAPI(host=api_url)
    try:
        api.auth(username=username, password=password)
        print("Authentication successful!")
        return True
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False


def run(args):
    """Handle the `taiga config` command."""
    ensure_config_directory()

    print("--- Configure Taiga CLI ---")

    api_url = input("Enter Taiga API URL (e.g., https://taiga.example.com): ").strip()
    username = input("Enter your Taiga username: ").strip()
    password = getpass("Enter your Taiga password: ")

    print("\nValidating credentials...")
    if not validate_credentials(api_url, username, password):
        print("Invalid credentials. Please try again.")
        return

    # Save the configuration without the password
    config_data = {
        "api_url": api_url,
        "username": username
    }
    save_config(config_data)

    print("Configuration saved successfully!")
