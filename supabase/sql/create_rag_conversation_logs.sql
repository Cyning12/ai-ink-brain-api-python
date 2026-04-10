-- 用于 Supabase (PostgreSQL) 创建 RAG 全链路调试日志表
-- 执行位置：Supabase Dashboard → SQL Editor

create extension if not exists "pgcrypto";

create table if not exists public.rag_conversation_logs (
  id uuid primary key default gen_random_uuid(),
  session_id varchar not null,
  query text not null,
  rewritten_query text,
  retrieved_context jsonb,
  response text,
  metadata jsonb,
  created_at timestamptz not null default now()
);

create index if not exists rag_conversation_logs_session_id_idx
  on public.rag_conversation_logs (session_id);

create index if not exists rag_conversation_logs_created_at_idx
  on public.rag_conversation_logs (created_at desc);

