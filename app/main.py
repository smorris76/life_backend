from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from git import Repo
from datetime import datetime
import json
import yaml
import os
import subprocess
from app.render_html import render_life_html

def deploy_life_html(source_path: str, target: str):
    key = "/root/.ssh/id_deploy"
    try:
        subprocess.run(
            [
                "scp",
                "-o", "StrictHostKeyChecking=no",
                "-o", "UserKnownHostsFile=/dev/null",
                "-i", key,
                "-q", source_path,
                target
            ],
            check=True
        )
        print(">> HTML deployed successfully.")
    except subprocess.CalledProcessError as e:
        print(">> HTML deployment failed:", e)


app = FastAPI()

FILE_PREFIX = os.getenv("FILE_PREFIX")
REPO_PATH = os.getenv("REPO_PATH", "/repo")
API_TOKEN = os.getenv("API_TOKEN")
SSH_DEST = os.getenv("SSH_DEST")
if not FILE_PREFIX:
    raise RuntimeError("Missing required environment variables: FILE_PREFIX")
elif not REPO_PATH:
    raise RuntimeError("Missing required environment variables: REPO_PATH")
elif not API_TOKEN:
    raise RuntimeError("Missing required environment variables: API_TOKEN")
elif not SSH_DEST:
    raise RuntimeError("Missing required environment variables: SSH_DEST")
else:
    JSON_PATH = os.path.join(REPO_PATH, f"{FILE_PREFIX}.json")
    YAML_PATH = os.path.join(REPO_PATH, f"{FILE_PREFIX}.yaml")
    HTML_PATH = os.path.join(REPO_PATH, f"{FILE_PREFIX}.html")

repo = Repo("/repo")

@app.get("/life")
async def read_life(authorization: str = Header(...)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/life")
async def update_life(request: Request, authorization: str = Header(...)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        wrapper = await request.json()
        # Robust fallback chain
        data = (
            wrapper.get("params", {})
                   .get("life", wrapper.get("params", {}))
                   or wrapper.get("file")
                   or wrapper
        )
        with open(JSON_PATH, "w") as f:
            json.dump(data, f, indent=2)
        with open(YAML_PATH, "w") as y:
            yaml.dump(data, y)
        render_life_html(data, HTML_PATH)
        deploy_life_html(HTML_PATH, SSH_DEST)

        try:
            json_git_path = os.path.relpath(JSON_PATH, repo.working_tree_dir)
            yaml_git_path = os.path.relpath(YAML_PATH, repo.working_tree_dir)
            html_git_path = os.path.relpath(HTML_PATH, repo.working_tree_dir)
            repo.index.add([json_git_path, yaml_git_path, html_git_path])
            #repo.index.add([json_git_path])
            repo.index.commit(f"Update from API at {datetime.now().isoformat()}")
        except Exception as e:
            print(">> Git commit failed:", e)

        return JSONResponse(content={"detail": "Update successful"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
