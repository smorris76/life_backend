# Life Backend

This is a Dockerized FastAPI application that serves as the backend for a
personal productivity and CRM system. It reads and writes a YAML-based data
file (`life.yaml`) versioned using Git, enabling structured, secure tracking
of tasks, projects, and customer interactions.

---

## 🔧 Features

- ✅ **REST API** for reading and updating `life.yaml`
- ✅ **Token-based authentication** for secure access
- ✅ **Rate limiting** with `slowapi` to protect against abuse
- ✅ **Git integration** for version history, rollback, and auditability
- ✅ **Dockerized** for portability and maintainability
- ✅ **Local repo mount** for easy access and off-host backup
- ✅ **Safe directory and committer identity configuration** handled at startup

---

## 📦 API Endpoints

### `GET /life`

Returns the current version of `life.yaml`.

- **Auth required**: Yes (Bearer token)
- **Rate limit**: 10 requests per minute per IP

### `POST /life`

Overwrites `life.yaml` with new content, commits the change to Git.

- **Auth required**: Yes (Bearer token)
- **Rate limit**: 5 requests per minute per IP

---

## 🚀 Quickstart

### 1. Build the image

```bash
docker build -t life-backend .
```

### 2. Create a `.env` file

```env
REPO_PATH=/repo
FILE_NAME=life.yaml
GIT_USER=Shawn Morris
GIT_EMAIL=shawn@smorris.com
API_TOKEN=your-secret-token
```

### 3. Run the container

```bash
docker run -d \
  --name life-api \
  --env-file ~/.life-data.env \
  -v $HOME/life-data:/repo \
  -p 8000:8000 \
  --restart unless-stopped \
  life-backend
```

---

## 🔐 Authentication

Use a Bearer token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer <your-token>" http://localhost:8000/life
```

---

## ⚙️ Environment Variables

| Variable        | Description                              |
|-----------------|------------------------------------------|
| `REPO_PATH`     | Path to the mounted Git repo             |
| `FILE_NAME`     | YAML file name (e.g. `life.yaml`)        |
| `GIT_USER`      | Git commit user.name                     |
| `GIT_EMAIL`     | Git commit user.email                    |
| `API_TOKEN`     | Bearer token for API access              |

---

## 🛠 Internals

- `entrypoint.sh`: Configures Git (safe.directory, identity) and starts Uvicorn
- `main.py`: Defines the FastAPI app and routes
- `git_utils.py`: Handles Git interactions (add, commit)
- Rate limits are applied via `slowapi` using IP-based rules

---

## 🧩 Future Ideas

- OpenAPI schema for GPT integration
- Optional HTTPS + reverse proxy via Caddy
- Read-only web viewer for `life.yaml`

---

## 📄 License

This project is intended for private or personal use. Contact the author if
you'd like to adapt it for broader distribution.
