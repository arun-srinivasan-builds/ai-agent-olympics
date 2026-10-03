# AI Agent Olympics — Docker + VPS Deployment

## Deployment target

The production container runs the Streamlit application on port `8501` using Python `3.11`.

The application expects these secrets through environment variables:

```text
OPENAI_API_KEY
SERPER_API_KEY
AI_MODEL
EVAL_MODEL
```

Never commit the real `.env` file.

---

## 1. Local Docker validation

From the project root:

```bat
docker compose build --no-cache
docker compose up -d
docker compose ps
```

Open:

```text
http://localhost:8501
```

Validate container health:

```bat
docker inspect ai-agent-olympics --format "{{json .State.Health}}"
```

View logs:

```bat
docker compose logs -f ai-agent-olympics
```

Stop the application:

```bat
docker compose down
```

---

## 2. VPS directory standard

Recommended production directory:

```text
/docker/apps/AI-Agent-Olympics
```

This follows the same enterprise deployment structure used by the other portfolio applications.

---

## 3. Clone from GitHub on the VPS

```bash
cd /docker/apps
git clone <YOUR_GITHUB_REPOSITORY_URL> AI-Agent-Olympics
cd AI-Agent-Olympics
```

For later updates:

```bash
cd /docker/apps/AI-Agent-Olympics
git pull origin main
```

---

## 4. Create the production `.env`

```bash
cp .env.example .env
nano .env
```

Populate:

```text
OPENAI_API_KEY=<production-key>
SERPER_API_KEY=<production-key>
AI_MODEL=gpt-4.1-mini
EVAL_MODEL=gpt-4.1-mini
```

Protect it:

```bash
chmod 600 .env
```

---

## 5. Build and run on the VPS

```bash
docker compose build --no-cache
docker compose up -d
docker compose ps
```

Expected status:

```text
ai-agent-olympics   Up ... (healthy)
```

Validate locally on the VPS:

```bash
curl -I http://127.0.0.1:8501/_stcore/health
```

Expected response:

```text
HTTP/1.1 200 OK
```

---

## 6. Reverse proxy / public URL

Expose the container through the VPS reverse proxy using a dedicated subdomain, for example:

```text
ai-agent-olympics.<your-domain>
```

Proxy target:

```text
http://127.0.0.1:8501
```

Enable HTTPS before sharing the URL publicly.

---

## 7. Production validation checklist

- Dashboard loads without layout regressions.
- Left navigation and approved Olympic UI remain intact.
- All five event pages open correctly.
- One controlled benchmark event runs successfully.
- One custom question runs successfully.
- `Run All 5 Benchmark Events` executes sequentially.
- Official medal board remains frozen after live runs.
- Latest-run tokens, duration, answer and evals update correctly.
- Container reports `healthy`.
- Public URL uses HTTPS.
- `.env` is not committed or exposed.

---

## 8. Release/update procedure

After a code change is validated locally:

```bash
git pull origin main
docker compose build
docker compose up -d
docker compose ps
```

If troubleshooting is needed:

```bash
docker compose logs --tail=200 ai-agent-olympics
```

Rollback to the previous Git commit if required, then rebuild the container.
