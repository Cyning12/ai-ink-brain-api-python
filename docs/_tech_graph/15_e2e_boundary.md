```mermaid
flowchart TD
  %% 15_e2e_boundary: 人类友好版（≤12 节点）

  FE[Frontend UI<br/>SSE timeline renderer]
  BFF[Next BFF<br/>/api/py/unified/chat/stream<br/>ai-ink-brain/app/api/py/unified/chat/stream/route.ts]
  PY[Python FastAPI<br/>POST /api/py/unified/chat/stream<br/>api/index.py::unified_chat_stream_route]
  SSE[SSE events<br/>event: chain | done<br/>api/unified_chat.py::_sse]
  CONTRACT[契约最小键名<br/>chain:{type,ts,step_id,payload}<br/>done:{ok,mode,run_id,session_id}]

  CONTENT[Content repo<br/>content/]
  ROOT[CONTENT_ROOT 边界<br/>api/ingest_pipeline.py::get_all_markdown_chunks]

  DB[Supabase<br/>tables/RPC 以 manifest 为真值]
  RPC[example: match_documents<br/>supabase/sql/init.sql]

  FE --> BFF --> PY --> SSE --> CONTRACT
  CONTENT --> ROOT --> PY
  PY --> DB --> RPC
```

### 锚点与真值来源

- **后端端点/表/RPC 真值**：`docs/_tech_graph/_manifest.json`
- **SSE 事件集合 + 最小字段键**：`docs/_tech_graph/14_runtime_observability.ai.md`
- **前端 SSE 消费锚点**：`../ai-ink-brain/components/unified-chat/UnifiedChatPageClient.tsx`
- **前端 BFF 透传锚点**：`../ai-ink-brain/app/api/py/unified/chat/stream/route.ts`
