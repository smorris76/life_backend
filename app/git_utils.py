import subprocess
from pathlib import Path
from app.config import REPO_PATH, FILE_NAME, GIT_AUTHOR

def run_git_command(args, cwd=REPO_PATH):
    result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()

def get_life_yaml():
    #run_git_command(["pull"])
    yaml_file = Path(REPO_PATH) / FILE_NAME
    return yaml_file.read_text()

def update_life_yaml(content: str):
    yaml_file = Path(REPO_PATH) / FILE_NAME
    yaml_file.write_text(content)
    run_git_command(["add", FILE_NAME])
    run_git_command(["commit", "-m", "Update life.yaml"])
