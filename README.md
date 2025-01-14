# Taiga CLI

`taiga-cli` is a command-line interface (CLI) tool designed to interact with a **Taiga** instance, an agile project management platform. This CLI allows users to manage configurations, projects, sprints, and user stories efficiently and quickly from the terminal.

---

## **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dhabyx/python-taiga-cli.git
   cd taiga-cli
   ```

2. **Install the tool**:
   Use `pip` to install the project as a global CLI application:
   ```bash
   pip install .
   ```

   This will install the tool and set up the `taiga` command to be executed from anywhere in your terminal.

3. **Verify the installation**:
   ```bash
   taiga --help
   ```

   If you see the help menu, everything is set!

4. **Update the tool**:
   If you make local changes or want to update from the repository, reinstall it:
   ```bash
   pip install --upgrade .
   ```

5. **Uninstall the tool**:
   If you need to remove the CLI, use:
   ```bash
   pip uninstall taiga-cli
   ```

---

## **Commands**

### **1. Configuration (`config`)**
Set up the server and user credentials.

```bash
taiga config
```

Follow the interactive instructions to configure the Taiga server and user credentials.

---

### **2. Login (`login`)**
Authenticate with your Taiga instance.

```bash
taiga login
```

---

### **3. Project Management (`project`)**

- **List your own projects**:
  ```bash
  taiga project ls
  ```

- **List all projects**:
  ```bash
  taiga project ls --all
  ```

- **Show default project**:
  ```bash
  taiga project default
  ```

- **Set a project as the default**:
  ```bash
  taiga project set-default <project-slug>
  ```

---

### **4. Sprint Management (`sprint`)**

- **Set a sprint as the default**:
  ```bash
  taiga sprint set-default <sprint-slug>
  ```

- **List sprints of the default project**:
  ```bash
  taiga sprint ls
  ```

- **List sprints of a specific project**:
  ```bash
  taiga sprint ls --project=<project-slug>
  ```

- **View user statistics for a sprint**:
  ```bash
  taiga sprint user-stats
  ```

- **View statistics of a specific user**:
  ```bash
  taiga sprint user-stats --user=<username>
  ```

- **View statistics for all users**:
  ```bash
  taiga sprint user-stats --all-users
  ```

- **View statistics for a specific project**:
  ```bash
  taiga sprint user-stats --project=<project-slug>
  ```

- **View statistics for a specific sprint**:
  ```bash
  taiga sprint user-stats --sprint=<sprint-slug>
  ```

- **List user stories for a sprint**:
  ```bash
  taiga sprint user-stories
  ```

- **List stories for a specific user**:
  ```bash
  taiga sprint user-stories --user=<username>
  ```

- **List stories for all users**:
  ```bash
  taiga sprint user-stories --all-users
  ```

---

### **5. User Stories Management (`stories`)**

- **List your own stories**:
  ```bash
  taiga stories ls
  ```

- **List stories from all sprints**:
  ```bash
  taiga stories ls --all-sprints
  ```

- **Filter stories by user**:
  ```bash
  taiga stories ls --user=<username>
  ```

- **Filter stories by status**:
  ```bash
  taiga stories ls --status=open
  taiga stories ls --status=closed
  ```

- **Filter stories by sprint**:
  ```bash
  taiga stories ls --sprint=<sprint-slug>
  ```

- **Filter stories by a specific project**:
  ```bash
  taiga sprint user-stats --project=<project-slug>
  ```

---

### **6. Configuration Management**

`taiga-cli` stores its configuration in a file on the user's system. This configuration includes details such as the Taiga server, user credentials, and default values for projects and sprints.

---

#### **Configuration File Location**
The configuration file is located in the following paths depending on the operating system:

- **Linux**:
  ```bash
  ~/.config/taiga-cli/config.json
  ```

- **macOS**:
  ```bash
  ~/Library/Application Support/taiga-cli/config.json
  ```

- **Windows**:
  (Explicit support for Windows is not designed, but you could adapt it).

---

#### **Clear Configuration**
If you want to reset all stored configuration and restart the tool:

1. **Delete the configuration file**:
   - On Linux:
     ```bash
     rm ~/.config/taiga-cli/config.json
     ```
   - On macOS:
     ```bash
     rm ~/Library/Application\\ Support/taiga-cli/config.json
     ```

2. **Recreate the configuration**:
   After deleting the file, running `taiga config` will prompt you to re-enter the details:
   ```bash
   taiga config
   ```

---

#### **Warning**
Deleting this configuration file:
- Resets the server, credentials, and any configured default values.
- Does not affect data stored in the Taiga instance you are using.

---

## **Help**
To view all available options and commands:
```bash
taiga --help
```

For a specific command:
```bash
taiga <command> --help
```

---

## **Contributing**
1. **Fork this repository.**
2. **Create a new branch:**
   ```bash
   git checkout -b feature/new-functionality
   ```

3. **Make changes and commit:**
   ```bash
   git commit -m "Add new functionality"
   ```

4. **Push and open a Pull Request.**

---

## **License**
`taiga-cli` is under the MIT License. See the `LICENSE` file for more information.

---

If you have further improvements or additional details, let me know!
