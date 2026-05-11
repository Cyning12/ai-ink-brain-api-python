-- 在已有 public.agent_info 表上追加测试行：gender =「保密」「未填写」
-- 用于 DISTINCT 探针 / 真库与 YAML 漂移验证（YAML 默认仍为 男、女）
-- 用法：Supabase SQL Editor 或 psql 连接 TEXT2SQL_DATABASE_URL 后执行

begin;

delete from public.agent_info where agent_id in (900001, 900002);

insert into public.agent_info (
  agent_id,
  name,
  gender,
  date_of_birth,
  address,
  phone_number,
  email_address,
  certificate_number,
  license_issue_date,
  license_expiration_date,
  commission_structure
) values
  (
    900001,
    '测试代理甲',
    '保密',
    '1990-01-01 00:00:00',
    '测试地址（gender=保密）',
    13800000001,
    'test_confidential@example.com',
    11111111,
    '2020-01-01 00:00:00',
    '2030-01-01 00:00:00',
    '固定佣金'
  ),
  (
    900002,
    '测试代理乙',
    '未填写',
    '1991-02-02 00:00:00',
    '测试地址（gender=未填写）',
    13800000002,
    'test_unfilled@example.com',
    22222222,
    '2020-01-01 00:00:00',
    '2030-01-01 00:00:00',
    '底薪加提成'
  );

commit;
