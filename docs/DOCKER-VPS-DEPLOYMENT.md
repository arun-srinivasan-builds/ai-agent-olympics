# AI Agent Olympics — Docker + VPS Deployment

## Deployment target

The production container runs the Streamlit application on internal port `8501` using Python `3.11`.

The application expects these environment variables:

```text
OPENAI_API_KEY
SERPER_API_KEY
AI_MODEL
EVAL_MODEL
```

Never commit the real `.env` file.

Current public deployment:

```text
https://ai-agent-olympics.srv1965124.hstgr.cloud
```

---

## 1. Local Docker validation

From the project root:

```bat
docker compose build --no-cache
docker compose up -d
docker compose ps
```

Local host mapping:

```text
127.0.0.1:8502 -> container:8501
```

Open:

```text
http://localhost:8502
```

Validate container health:

```bat
curl.exe http://localhost:8502/_stcore/health
```

Expected:

```text
ok
```

Stop the application:

```bat
docker compose down
```

---

## 2. VPS directory standard

Production directory:

```text
/docker/apps/AI-Agent-Olympics
```

---

## 3. Clone from GitHub on the VPS

```bash
cd /docker/apps
git clone https://github.com/arun-srinivasan-builds/ai-agent-olympics.git AI-Agent-Olympics
cd AI-Agent-Olympics
```

For later updates:

```bash
cd /docker/apps/AI-Agent-Olympics
git pull --ff-only origin main
```

---

## 4. Create the production `.env`

Create the file from the safe template:

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Populate the real values directly on the VPS. Do not print the file contents in terminal output, logs, documentation, or chat.

Safe variable-name-only validation:

```bash
awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' .env
```

Expected names:

```text
OPENAI_API_KEY
SERPER_API_KEY
AI_MODEL
EVAL_MODEL
```

---

## 5. VPS Compose layout

The repository keeps two Compose files:

```text
docker-compose.yml       base/local runtime
docker-compose.vps.yml   VPS Traefik routing override
```

The VPS override joins the existing shared Traefik network:

```text
n8n_default
```

Traefik routes HTTPS traffic directly to:

```text
ai-agent-olympics:8501
```

The private VPS troubleshooting route remains:

```text
127.0.0.1:8502 -> container:8501
```

---

## 6. Build and run on the VPS

```bash
docker compose -f docker-compose.yml -f docker-compose.vps.yml build --no-cache
docker compose -f docker-compose.yml -f docker-compose.vps.yml up -d
docker compose -f docker-compose.yml -f docker-compose.vps.yml ps
```

Expected status:

```text
ai-agent-olympics   Up ... (healthy)
```

Validate privately on the VPS:

```bash
curl -s http://127.0.0.1:8502/_stcore/health
```

Expected:

```text
ok
```

---

## 7. Traefik / HTTPS routing

Existing shared reverse proxy:

```text
n8n-traefik-1
```

Shared Docker network:

```text
n8n_default
```

Public hostname:

```text
ai-agent-olympics.srv1965124.hstgr.cloud
```

The VPS override contains the Traefik labels and explicitly sets the Streamlit backend port to `8501`.

Public validation:

```bash
curl -I https://ai-agent-olympics.srv1965124.hstgr.cloud
```

Expected:

```text
HTTP/2 200
```

---

## 8. Production validation checklist

- Dashboard loads without layout regressions.
- Left navigation and approved Olympic UI remain intact.
- All five event pages open correctly.
- Challenge Question remains editable.
- Reset to Benchmark Question restores the official prompt.
- One controlled benchmark event runs successfully.
- One custom question runs successfully.
- `Run All 5 Benchmark Events` executes sequentially.
- Official medal board remains frozen after live runs.
- Latest-run tokens, duration, answer and evals update correctly.
- Container reports `healthy`.
- Public URL returns HTTPS successfully.
- `.env` remains ignored and is never printed or committed.

---

## 9. Release / update procedure

After changes are committed and pushed to `main`:

```bash
cd /docker/apps/AI-Agent-Olympics
git pull --ff-only origin main
docker compose -f docker-compose.yml -f docker-compose.vps.yml build
docker compose -f docker-compose.yml -f docker-compose.vps.yml up -d
docker compose -f docker-compose.yml -f docker-compose.vps.yml ps
```

Health check:

```bash
curl -s http://127.0.0.1:8502/_stcore/health
```

Do not use diagnostic commands that print container environment values or the contents of `.env`.
