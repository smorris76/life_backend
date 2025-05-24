# Life Controller

This is a Dockerized FastAPI + Caddy application that powers a personal productivity and CRM system. It exposes an authenticated JSON-based API that manages a structured `life.json` file. The system supports hierarchical task management, CRM tracking, and renders human-readable outputs (YAML, HTML). Changes are versioned in Git and can be deployed or visualized elsewhere.

---

## 🔧 Features

- ✅ **REST API** for reading and updating `life.json`
- ✅ **Token-based authentication**
- ✅ **Rate limiting** via `slowapi`
- ✅ **Git integration** for commit history
- ✅ **YAML + HTML renderers** post-update
- ✅ **Caddy reverse proxy** with HTTPS support
- ✅ **Docker Compose** orchestration
- ✅ **GHCR-compatible image structure**

---

## 📦 API Endpoints

### `GET /life`
Returns the current `life.json`.

- **Auth required**: Yes (Bearer token)
- **Rate limit**: 10 requests/min/IP

### `POST /life`
Replaces `life.json`, commits it to Git, and triggers:

- YAML conversion (`life.yaml`)
- HTML rendering (`life.html`)
- Optional SCP deployment to external web server

---

## 📁 File Structure

```
life_backend/
├── app/
│   ├── config.py
│   ├── git_utils.py
│   ├── main.py
│   └── logging-config.yaml
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
├── logging-config.json
├── openapi.json
├── docker-compose.yml
├── Caddyfile
├── README.md
└── env.example
```

---

## 🚀 Running Locally

```bash
docker compose up --build -d
```

The API is served at `http://localhost:8000`, proxied via Caddy.

---

## 🔐 Authentication

All endpoints require a bearer token defined in your `.env` or passed as `API_TOKEN`.

---

## 💾 Versioning & Backup

The backend commits all changes to `life.json`, `life.yaml`, and `life.html` into a mounted Git repo at `/repo`.

---

## 🔮 Future Enhancements

- External health checks
- Weekly review and agenda forecasting
- GHCR GitHub Actions build pipeline

---

## License

MIT — see `LICENSE.md` if present.