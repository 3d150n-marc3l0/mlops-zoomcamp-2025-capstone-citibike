# Environment Setup
Before starting, ensure that your machine has Python 3.12, Docker, and Docker-Compose already installed.

### 1. **Python 3.12** 

This project requires Python 3.12. Ensure that it is installed by running the following command:

```bash
python3 --version
```
The output should confirm that Python 3.12 is installed.

### 2. **Docker**

Docker is required for containerization. Check if Docker is installed and running:

```bash
docker --version
```
You should see the installed Docker version.

### 3. **Docker Compose**

Docker Compose is used for multi-container Docker applications. To verify that Docker Compose is installed:

```bash
docker-compose --version
```

You should see the installed version of Docker Compose.



## Install Poetry

Poetry is a Python dependency management and packaging tool that simplifies dependency management and project configuration. Here’s how to install and verify it:

### 1. **Install Poetry**

To install Poetry, run the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. **Add Poetry to PATH**

After installation, you need to ensure that Poetry is in your PATH. Depending on the shell you're using, open the corresponding shell configuration file:

- Bash: Open ~/.bashrc or ~/.bash_profile.

- Zsh: Open ~/.zshrc.

- Fish: Open ~/.config/fish/config.fish.

Add the following line to the appropriate file:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

For example, in Bash, you would open ~/.bashrc and add the above line.

### 3. **Reload the Shell Configuration**

After saving the file, reload the shell configuration by running:

- For Bash:

```bash
source ~/.bashrc
```

- For Zsh:

```bash
source ~/.zshrc
```

- For Fish:

```bash
source ~/.config/fish/config.fish
```

### 4. **Verify Poetry Installation**

After adding Poetry to your **PATH**, you can verify that Poetry is installed and accessible by running:

```bash
poetry --version
```

You should see the version of Poetry installed, e.g., Poetry version 1.7.0.


## Install Poetry Shell

**Poetry Shell** is a plugin that allows you to create and manage isolated virtual environments within your project using Poetry. To install Poetry Shell, follow these steps:

### 1. **Install Poetry Shell Plugin**

To enable Poetry Shell, you need to install the `poetry-plugin-shell` plugin. Run the following command:

```bash
poetry self add poetry-plugin-shell
```

### 2. **Verify Poetry Shell Installation**
Once the plugin is installed, you can initialize a new virtual environment by running:

```bash
poetry shell
```

This command creates and activates a virtual environment for your project. You can verify that the virtual environment is active by running:

```bash
which python
```

This should show the path to the Python interpreter inside the virtual environment.