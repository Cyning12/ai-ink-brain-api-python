# ai-ink-brain-api-python

FastAPI backend for **AI-Ink-Brain** (RAG chat + ingest/sync) designed for deployment on **Vercel Python Runtime**.

## Endpoints

- `POST /api/py/chat`
- `GET /api/py/health`
- `POST /api/py/admin/sync`
- `GET /api/py/admin/sync?jobId=...`
- `POST /api/py/admin/ingest`

## Required Environment Variables

- `SILICONFLOW_API_KEY`
- `SILICONFLOW_BASE_URL` (optional, default `https://api.siliconflow.cn/v1`)
- `SILICONFLOW_EMBEDDING_MODEL` (optional)
- `SILICONFLOW_EMBEDDING_DIMENSIONS` (optional, for Qwen3)
- `SILICONFLOW_CHAT_MODEL` (optional)
- `NEXT_PUBLIC_SUPABASE_URL` (or `SUPABASE_URL`)
- `SUPABASE_SERVICE_ROLE_KEY` (or `SUPABASE_SERVICE_KEY`)
- `SYNC_ADMIN_SECRET` (admin/sync; same value as frontend BFF)
- ~~`NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET`~~ (deprecated · fallback only · to be removed)
- `RAG_MATCH_THRESHOLD` (optional, default `0.3`, set `none` to disable)
- `DEBUG_RAG` / `RAG_DEBUG` (optional)

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # fill in keys; see docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md
```

**Start API** (recommended: `--log-level info` so Intent retry lines like `[intent-retry]` appear in the console; no extra `DEBUG_INTENT_CACHE` needed):

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --log-level info
```

**Dev with auto-reload:**

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload --log-level info
```

**Smoke check:**

```bash
curl -sS http://127.0.0.1:8000/api/py/health
curl -sS http://127.0.0.1:8000/api/py/live
```

**Tests** (same as CI; excludes slow intent eval/benchmark):

```bash
pytest tests -m "not intent_eval and not intent_benchmark"
```

## Notes

- This repo expects Supabase `public.documents` + RPC `match_documents` already created.
- Admin `sync` uses an in-memory job map, suitable for single instance (serverless may not preserve state).
