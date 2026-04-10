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
- `NEXT_PUBLIC_ADMIN_SECRET` (or `CHAT_API_SECRET`)
- `RAG_MATCH_THRESHOLD` (optional, default `0.3`, set `none` to disable)
- `DEBUG_RAG` / `RAG_DEBUG` (optional)

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

## Notes

- This repo expects Supabase `public.documents` + RPC `match_documents` already created.
- Admin `sync` uses an in-memory job map, suitable for single instance (serverless may not preserve state).
