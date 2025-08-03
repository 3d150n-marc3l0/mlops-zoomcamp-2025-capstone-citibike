# mlops-zoomcamp-2025-capstone-citibike
mlops-zoomcamp 2025 capstone


# Environment

- **Poetry**.
- **Zenml**.
- **Mlflow**.
- **Optuna**.
- **Bentoml**.
- **localstack**.

# Settings
## Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Open your shell configuration file:
Depending on the shell you're using, you'll need to modify a configuration file:

- **Bash**: If you're using Bash, open the ~/.bashrc or ~/.bash_profile file.

- **Zsh**: If you're using Zsh, open the ~/.zshrc file.

- **Fish**: If you're using Fish, open the ~/.config/fish/config.fish file.

For example, in shell option you have to open your shell configuration file (~/.bashrc) and 
add `export PATH="/home/emmuzoo/.local/bin:$PATH"` to your shell configuration file.

```bash
vi ~/.bashrc
...
...
...

export PATH="/home/emmuzoo/.local/bin:$PATH"
```

After editing the file, apply the changes without having to close and reopen the terminal with:

```bash
source ~/.bashrc
```

You can test that everything is set up by executing:

```bash
poetry --version

Poetry (version 2.1.3)
```

### Setting With Poetry

```bash
cd ~/mlops-zoomcamp-2025-capstone-citibike
poetry init
```

 Install dependecies:
```bash
poetry add --group dev $(cat requirements.dev.txt)
```

```bash
poetry add $(cat requirements.txt)

```