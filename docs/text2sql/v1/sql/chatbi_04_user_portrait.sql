-- =============================================================================
-- 文件：chatbi_04_user_portrait.sql
-- 用途：ChatBI V3 · **L2 终端用户**可经 Text2SQL **唯一推荐写表**——用户肖像/长久习惯（非核心业务用户宽表）
-- 执行位置：Supabase Dashboard → SQL Editor → 整段粘贴执行
-- 依赖：无；建议在 `chatbi_01`～`chatbi_03` 之后执行（无 FK 依赖，仅任务单约定顺序）
--
-- 产品语义（与 OpenItems §1.3.1、§1.4 对齐）：
-- - **L2 禁止 INSERT**；仅允许 **UPDATE** 除 `user_id` 外的列（首期仅 `long_term_prompt`）。
-- - `user_id`：主键 / 归属键，**L2 不得 UPDATE 本列**（由闸门 + 列白名单 enforce）。
-- - 后续新增可改列：须同步 **可改列白名单**（实现自定，可为 policy JSON 扩展）。
-- - L2 **禁止跨表 / JOIN**：由 AST 后闸 enforce，不单靠本 DDL。
-- =============================================================================

begin;

-- drop table if exists public.chatbi_user_portrait cascade;

create table if not exists public.chatbi_user_portrait (
  user_id text primary key,

  -- 长久 Prompt / 用户习惯摘要等（非「用户通讯录类」PII 宽表）
  long_term_prompt text not null default '',

  updated_at timestamptz not null default now()
);

comment on table public.chatbi_user_portrait is 'L2：肖像与长久习惯；写仅限 UPDATE 非 user_id 列；禁止 INSERT 见 OpenItems §1.4';
comment on column public.chatbi_user_portrait.user_id is '归属主键；L2 UPDATE 不可触碰';
comment on column public.chatbi_user_portrait.long_term_prompt is '长久 Prompt / 习惯等；首期 L2 可改列之一';

create index if not exists chatbi_user_portrait_updated_at_idx
  on public.chatbi_user_portrait (updated_at desc);

commit;
