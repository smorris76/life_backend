#!/bin/bash
set -e  # Exit on error

# Ensure the repo is trusted by Git (avoid 'dubious ownership' errors)
git config --global --add safe.directory "${REPO_PATH}"
git config --global user.name "${GIT_USER}"
git config --global user.email "${GIT_EMAIL}"

# Optionally: pull latest changes on startup
#cd "${REPO_PATH}"
#git pull || echo "Warning: could not pull from repo"

# Start the API
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "${PORT}" \
    --log-config /app/logging-config.json
