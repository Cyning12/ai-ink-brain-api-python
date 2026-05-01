-- =============================================================================
-- Text2SQL v1 · Supabase/Postgres 初始化脚本（最小可用样例数据）
-- 用法：Supabase Dashboard → SQL Editor → 粘贴整段执行
--
-- 说明：
-- - 原始数据来源于 docs/text2sql/v1/sql/（Navicat 导出的 MySQL 脚本）
-- - 本脚本已移除 MySQL 方言（SET NAMES/FOREIGN_KEY_CHECKS/ENGINE/CHARSET/AUTO_INCREMENT 等）
-- - 统一采用 snake_case 小写字段名，便于 Text2SQL 生成
-- - 每表仅保留前 10 行样例数据（足够用于 v1 MVP 验证）
-- =============================================================================

begin;

-- ----------------------------
-- agent_info
-- ----------------------------
drop table if exists public.agent_info;
create table public.agent_info (
  agent_id bigint,
  name text,
  gender text,
  date_of_birth timestamp,
  address text,
  phone_number bigint,
  email_address text,
  certificate_number bigint,
  license_issue_date timestamp,
  license_expiration_date timestamp,
  commission_structure text
);

insert into public.agent_info values
  (367916, '张勇', '男', '1989-10-05 00:00:00', '新疆维吾尔自治区重庆县花溪惠州路J座 207678', 13949400870, 'jing61@example.net', 81558231, '2022-12-31 00:00:00', '2029-02-28 00:00:00', '固定佣金'),
  (580213, '马秀芳', '男', '1982-02-20 00:00:00', '福建省帅县双滦白街G座 658028', 15106451363, 'weiwei@example.org', 93288835, '2014-03-14 00:00:00', '2025-10-20 00:00:00', '固定佣金'),
  (882261, '窦刚', '女', '1988-10-29 00:00:00', '黑龙江省太原市海港潜江街G座 509037', 18223208693, 'ming30@example.org', 33159879, '2017-02-09 00:00:00', '2030-10-09 00:00:00', '提成结构'),
  (514922, '牟海燕', '男', '1987-06-17 00:00:00', '澳门特别行政区红霞县金平李路e座 865473', 18255576707, 'yangjin@example.net', 54025983, '2021-01-18 00:00:00', '2026-05-30 00:00:00', '提成结构'),
  (656679, '沈丹', '女', '2000-09-27 00:00:00', '甘肃省邯郸市翔安合山路s座 987931', 18953610446, 'qiang53@example.com', 78805353, '2018-04-14 00:00:00', '2031-06-19 00:00:00', '固定佣金'),
  (786458, '倪慧', '女', '1975-05-22 00:00:00', '江西省玉市闵行李路e座 388162', 18164914593, 'wei28@example.net', 42091510, '2014-07-30 00:00:00', '2029-05-29 00:00:00', '底薪加提成'),
  (284984, '曹玉', '女', '1986-08-20 00:00:00', '山东省桂香县普陀六安街U座 812361', 18275269415, 'ghuang@example.org', 94648855, '2016-10-07 00:00:00', '2030-06-23 00:00:00', '提成结构'),
  (79455, '张雪梅', '女', '1977-02-23 00:00:00', '河南省燕市花溪邯郸路a座 675638', 15344097557, 'huanglei@example.org', 76822635, '2019-12-29 00:00:00', '2032-06-04 00:00:00', '底薪加提成'),
  (397590, '覃淑珍', '女', '1982-03-30 00:00:00', '海南省天津县清浦黄街n座 114765', 15967782184, 'liangguiying@example.net', 61335527, '2017-05-01 00:00:00', '2024-09-23 00:00:00', '固定佣金'),
  (727776, '周倩', '女', '1960-01-03 00:00:00', '陕西省建平县和平惠州路V座 790906', 18206755709, 'jie75@example.org', 73651223, '2023-06-30 00:00:00', '2030-01-11 00:00:00', '固定佣金');

-- ----------------------------
-- beneficiary_info
-- ----------------------------
drop table if exists public.beneficiary_info;
create table public.beneficiary_info (
  beneficiary_id bigint,
  name text,
  gender text,
  date_of_birth date,
  nationality text,
  address text,
  phone_number bigint,
  email_address text
);

insert into public.beneficiary_info values
  (7618, '黄丽', '女', '1956-09-19', '巴西', '江苏省杭州市', 13846043285, 'vlgnlm@icloud.com'),
  (8840, '赵伟', '男', '1958-01-21', '英国', '河南省长沙市', 13291611976, 'fblzap@sohu.com'),
  (4429, '黄红', '男', '1989-09-18', '澳大利亚', '四川省武汉市', 13895404634, 'gjczal@163.com'),
  (6205, '周静', '女', '1957-09-19', '韩国', '河南省武汉市', 13994745844, 'ieijkd@outlook.com'),
  (7749, '刘娜', '男', '1981-03-13', '韩国', '浙江省长沙市', 13304632297, 'qgixnt@icloud.com'),
  (3332, '王伟', '男', '1980-05-24', '中国', '山东省上海市', 13224574518, 'jpxhsu@qq.com'),
  (5477, '杨涛', '女', '1995-08-03', '加拿大', '湖北省深圳市', 13900737696, 'cfjhxp@sohu.com'),
  (4544, '杨芳', '女', '1978-02-28', '韩国', '湖北省深圳市', 13472081396, 'ezxpuo@hotmail.com'),
  (3295, '刘磊', '男', '1957-11-02', '澳大利亚', '浙江省长沙市', 13210050188, 'rpfqoq@gmail.com'),
  (3111, '赵娜', '男', '1970-11-13', '法国', '山东省广州市', 13409026052, 'nurugr@sina.com');

-- ----------------------------
-- claim_info
-- ----------------------------
drop table if exists public.claim_info;
create table public.claim_info (
  claim_number text,
  policy_number text,
  claim_date timestamp,
  claim_type text,
  claim_amount bigint,
  claim_status text,
  claim_description text,
  beneficiary_id text,
  medical_records text,
  accident_report text,
  claim_handler text,
  review_date timestamp,
  payment_method text,
  payment_date timestamp,
  denial_reason text
);

insert into public.claim_info values
  ('CLM4243', 'POL29795', '2018-06-07 00:00:00', '医疗理赔', 55407, '审核中', '意外身故', 'BEN901', 'Medical records', 'Accident report', '张三', '2018-01-03 00:00:00', '支票', '2021-12-21 00:00:00', '资料不完整'),
  ('CLM1073', 'POL51873', '2020-05-11 00:00:00', '医疗理赔', 20026, '审核中', '车祸导致受伤', 'BEN106', 'Medical records', 'Accident report', '王五', '2010-03-07 00:00:00', '支票', '2015-07-28 00:00:00', '保险期限已过'),
  ('CLM3448', 'POL58182', '2015-07-22 00:00:00', '医疗理赔', 42063, '已拒绝', '意外身故', 'BEN154', 'Medical records', 'Accident report', '王五', '2014-07-07 00:00:00', '支票', '2015-01-16 00:00:00', '保险期限已过'),
  ('CLM8863', 'POL57396', '2017-02-05 00:00:00', '意外伤害理赔', 22287, '已批准', '住院治疗费用', 'BEN209', 'Medical records', 'Accident report', '李四', '2020-05-14 00:00:00', '支票', '2020-01-11 00:00:00', '不符合保险条款'),
  ('CLM8311', 'POL32375', '2012-07-28 00:00:00', '意外伤害理赔', 86718, '审核中', '意外身故', 'BEN686', 'Medical records', 'Accident report', '张三', '2011-05-13 00:00:00', '支票', '2010-05-19 00:00:00', '资料不完整'),
  ('CLM4114', 'POL47157', '2013-04-05 00:00:00', '身故理赔', 92884, '已拒绝', '意外身故', 'BEN951', 'Medical records', 'Accident report', '李四', '2017-03-26 00:00:00', '支票', '2013-06-18 00:00:00', '不符合保险条款'),
  ('CLM8636', 'POL15647', '2010-09-23 00:00:00', '意外伤害理赔', 85500, '已拒绝', '车祸导致受伤', 'BEN451', 'Medical records', 'Accident report', '王五', '2015-01-06 00:00:00', '电汇', '2010-06-26 00:00:00', '资料不完整'),
  ('CLM1554', 'POL42378', '2011-10-23 00:00:00', '意外伤害理赔', 51169, '已拒绝', '车祸导致受伤', 'BEN411', 'Medical records', 'Accident report', '李四', '2016-08-21 00:00:00', '直接存款', '2010-08-19 00:00:00', '资料不完整'),
  ('CLM9156', 'POL73748', '2018-03-15 00:00:00', '身故理赔', 93405, '审核中', '车祸导致受伤', 'BEN301', 'Medical records', 'Accident report', '李四', '2014-02-19 00:00:00', '支票', '2015-11-28 00:00:00', '不符合保险条款'),
  ('CLM9150', 'POL28403', '2020-07-23 00:00:00', '身故理赔', 1267, '审核中', '意外身故', 'BEN376', 'Medical records', 'Accident report', '王五', '2014-11-01 00:00:00', '支票', '2011-10-17 00:00:00', '不符合保险条款');

-- ----------------------------
-- customer_info
-- ----------------------------
drop table if exists public.customer_info;
create table public.customer_info (
  customer_id bigint,
  name text,
  gender text,
  date_of_birth date,
  id_number text,
  address text,
  phone_number bigint,
  email_address text,
  marital_status text,
  occupation text,
  health_status text,
  registration_date date,
  customer_type text,
  source_of_customer text,
  customer_status text
);

insert into public.customer_info values
  (609296, '欧颖', '女', '1996-11-05', '421200198010233550', '贵州省惠州市新城南昌街H座 647180', 14708198484, 'fangshen@example.org', '已婚', '企业主', '良好', '2023-10-13', '个人客户', '网站', '潜在客户'),
  (240508, '李辉', '女', '1961-11-22', '350681197909297401', '贵州省波县新城金路n座 737608', 15182875235, 'pchang@example.org', '未婚', '金领', '良好', '2020-08-03', '个人客户', '网站', '停保客户'),
  (590620, '李璐', '男', '1971-08-27', '510723198312100932', '山东省柳县朝阳武汉路e座 476236', 18604878643, 'juan91@example.org', '离异', '蓝领', '良好', '2020-01-08', '团体客户', '网站', '停保客户'),
  (831316, '张玉', '女', '1954-07-27', '440513199010211904', '安徽省岩县华龙上海路F座 293022', 18266615576, 'esun@example.net', '未婚', '金领', '良好', '2019-08-18', '团体客户', '网站', '潜在客户'),
  (798344, '张云', '女', '1995-10-20', '350421200402193942', '浙江省杰县双滦石家庄街k座 725835', 15783496041, 'qiang69@example.net', '已婚', '企业主', '良好', '2021-10-20', '团体客户', '网站', '活跃客户'),
  (321649, '周玉兰', '女', '2000-08-30', '371082197704223319', '上海市大冶市平山杨街B座 223799', 18944485428, 'mingmao@example.net', '已婚', '企业主', '良好', '2023-07-23', '团体客户', '代理人', '停保客户'),
  (421777, '徐波', '男', '2000-11-23', '440783197505188508', '内蒙古自治区兰英市吉区周街K座 323462', 18537535161, 'mingwan@example.org', '已婚', '金领', '良好', '2022-09-27', '个人客户', '网站', '活跃客户'),
  (147577, '季丹丹', '男', '1997-11-03', '469027199707168195', '吉林省浩县沙市王街H座 628857', 18556735783, 'qianglin@example.com', '未婚', '蓝领', '良好', '2019-06-30', '个人客户', '推广', '潜在客户'),
  (58489, '张杰', '女', '1961-03-04', '420105198301213280', '湖北省柳州市璧山石家庄街F座 590911', 13648915552, 'yongwen@example.org', '未婚', '企业主', '良好', '2019-07-16', '个人客户', '代理人', '潜在客户'),
  (58558, '张杰', '男', '1993-11-26', '321084198601216333', '安徽省兰州县平山太原路n座 778254', 13302970653, 'zengna@example.org', '已婚', '白领', '良好', '2018-11-13', '个人客户', '网站', '活跃客户');

-- ----------------------------
-- employee_info
-- ----------------------------
drop table if exists public.employee_info;
create table public.employee_info (
  employee_id bigint,
  name text,
  gender text,
  date_of_birth timestamp,
  address text,
  phone_number text,
  email_address text,
  hire_date timestamp,
  position text,
  department text,
  salary bigint,
  location text,
  supervisor text,
  employee_type text,
  employee_status text
);

insert into public.employee_info values
  (120925, 'Barry Schultz', '女', '1990-05-26 00:00:00', '3127 Sullivan Road, Brianmouth, LA 79417', '(237)764-5678', 'wrightjessica@example.com', '2019-02-04 00:00:00', 'Trade union research officer', '技术部', 18456, 'North Michelleland', 'Keith Williams', '合同工', '离职'),
  (715382, 'Abigail Rodriguez', '女', '1971-10-23 00:00:00', '237 Dawn Highway, South Sandra, SC 65019', '946-527-4527', 'johnsmith@example.net', '2021-12-12 00:00:00', 'Horticulturist, commercial', '技术部', 10622, 'North Cherylland', 'Lauren Gilmore', '合同工', '离职'),
  (414920, 'James Snyder', '女', '1967-04-25 00:00:00', '08061 Foster Brooks Suite 929, Myerston, OK 48787', '(976)557-9437x5333', 'benjamin77@example.net', '2022-12-09 00:00:00', 'Naval architect', '市场部', 11589, 'Staceyfurt', 'Justin Holt', '全职', '在职'),
  (953964, 'Amanda Esparza', '男', '1997-03-17 00:00:00', '284 Raymond Fords Apt. 800, Jasmineville, CO 42885', '+1-635-979-2484x0627', 'whoward@example.com', '2020-08-20 00:00:00', 'Administrator, charities/voluntary organisations', '人力资源部', 10079, 'Port William', 'Jade Buckley', '全职', '在职'),
  (71355, 'Mark Mitchell', '男', '1986-11-20 00:00:00', '41580 Torres Dale, East Markside, IL 23278', '(308)263-9939x092', 'shelleylewis@example.org', '2019-08-14 00:00:00', 'Production manager', '人力资源部', 11933, 'Williamsmouth', 'Tina Blair', '合同工', '离职'),
  (389134, 'Juan Crane', '女', '1960-11-15 00:00:00', '3593 Karen Courts, Patrickshire, PR 68579', '7949057551', 'kochdonna@example.net', '2022-06-06 00:00:00', 'Financial adviser', '技术部', 5510, 'North Robert', 'David Bailey', '合同工', '离职'),
  (762301, 'Jonathan Boyd', '男', '1990-12-13 00:00:00', '090 Berg Hollow Apt. 145, New Derrickview, MI 42098', '(336)918-0398', 'christina93@example.com', '2021-02-26 00:00:00', 'Art gallery manager', '财务部', 9414, 'New Bradley', 'Aaron Small', '全职', '离职'),
  (694521, 'Derek Johnson', '男', '1975-06-20 00:00:00', '832 Carroll Hollow, South Bryanberg, GA 22203', '+1-418-625-0520x2567', 'andreacarroll@example.com', '2020-08-29 00:00:00', 'Engineer, chemical', '销售部', 12179, 'Adamsburgh', 'Victoria Hernandez', '全职', '离职'),
  (523578, 'Phyllis Miller', '男', '1964-06-12 00:00:00', '60471 Michael Courts Apt. 969, Gregorybury, TN 21831', '932-287-4888x174', 'ryandavid@example.net', '2023-05-02 00:00:00', 'Analytical chemist', '人力资源部', 18175, 'East Kennethview', 'Kirk Todd', '合同工', '在职'),
  (835959, 'James Thomas', '女', '1966-01-03 00:00:00', '74915 Turner Flats Suite 761, Colebury, OK 48397', '(617)714-9433x2212', 'megan35@example.org', '2020-11-11 00:00:00', 'Marine scientist', '市场部', 14446, 'East Stephanie', 'Michael Williams', '兼职', '在职');

-- ----------------------------
-- policy_info
-- ----------------------------
drop table if exists public.policy_info;
create table public.policy_info (
  policy_number text,
  customer_id text,
  product_id text,
  policy_status text,
  beneficiary text,
  relationship text,
  policy_start_date timestamp,
  policy_end_date timestamp,
  premium_payment_status text,
  payment_date timestamp,
  payment_method text,
  agent_id text
);

insert into public.policy_info values
  ('POL744698', 'CUST9500', 'PROD802', '终止', '{''姓名'': ''赵六'', ''受益比例'': 80}', '配偶', '2014-08-27 00:00:00', '2019-08-27 00:00:00', '逾期', '2015-08-09 00:00:00', '信用卡', 'AGENT904'),
  ('POL263979', 'CUST9686', 'PROD192', '生效', '{''姓名'': ''李四'', ''受益比例'': 4}', '配偶', '2011-07-22 00:00:00', '2021-07-22 00:00:00', '未支付', '2013-07-20 00:00:00', '信用卡', 'AGENT155'),
  ('POL864724', 'CUST1623', 'PROD921', '暂停', '{''姓名'': ''李四'', ''受益比例'': 90}', '父母', '2013-02-03 00:00:00', '2020-02-03 00:00:00', '逾期', '2016-02-08 00:00:00', '信用卡', 'AGENT758'),
  ('POL863392', 'CUST6842', 'PROD360', '暂停', '{''姓名'': ''李四'', ''受益比例'': 44}', '父母', '2016-10-25 00:00:00', '2025-10-25 00:00:00', '未支付', '2025-10-02 00:00:00', '支票', 'AGENT693'),
  ('POL625994', 'CUST4733', 'PROD560', '终止', '{''姓名'': ''赵六'', ''受益比例'': 37}', '父母', '2011-02-03 00:00:00', '2021-02-03 00:00:00', '未支付', '2012-02-18 00:00:00', '银行转账', 'AGENT504'),
  ('POL755553', 'CUST8694', 'PROD649', '终止', '{''姓名'': ''张三'', ''受益比例'': 61}', '子女', '2015-06-24 00:00:00', '2020-06-24 00:00:00', '未支付', '2020-06-02 00:00:00', '信用卡', 'AGENT203'),
  ('POL184941', 'CUST7781', 'PROD858', '暂停', '{''姓名'': ''赵六'', ''受益比例'': 3}', '子女', '2014-08-17 00:00:00', '2022-08-17 00:00:00', '未支付', '2018-08-16 00:00:00', '支票', 'AGENT645'),
  ('POL347381', 'CUST5206', 'PROD461', '终止', '{''姓名'': ''赵六'', ''受益比例'': 65}', '父母', '2016-05-20 00:00:00', '2022-05-20 00:00:00', '未支付', '2021-05-06 00:00:00', '银行转账', 'AGENT160'),
  ('POL505796', 'CUST2974', 'PROD101', '生效', '{''姓名'': ''李四'', ''受益比例'': 72}', '父母', '2018-01-18 00:00:00', '2020-01-18 00:00:00', '已支付', '2019-01-19 00:00:00', '银行转账', 'AGENT655'),
  ('POL907420', 'CUST4914', 'PROD297', '终止', '{''姓名'': ''赵六'', ''受益比例'': 58}', '子女', '2013-02-10 00:00:00', '2014-02-10 00:00:00', '已支付', '2013-02-08 00:00:00', '银行转账', 'AGENT851');

-- ----------------------------
-- product_info
-- ----------------------------
drop table if exists public.product_info;
create table public.product_info (
  product_id bigint,
  product_name text,
  product_type text,
  coverage_range text,
  coverage_term text,
  premium bigint,
  payment_frequency text,
  product_features text,
  age_limit bigint,
  premium_calculation text,
  claims_process text,
  underwriting_requirements text,
  sales_region text,
  product_status text
);

insert into public.product_info values
  (8410, '医疗保险', '汽车保险', '100万-500万', '5年', 3302, '每月', '免赔额', 38, '按保额计算', '在线申请', '收入证明', '成都', '停售'),
  (6895, '医疗保险', '医疗保险', '10万-50万', '5年', 1721, '每季度', '保额递增', 27, '按年龄计算', '在线申请', '健康问卷', '上海', '停售'),
  (1602, '汽车保险', '寿险', '50万-200万', '3年', 8600, '每年', '免赔额', 27, '按健康状况计算', '在线申请', '健康问卷', '深圳', '可用'),
  (1132, '医疗保险', '意外险', '100万-500万', '1年', 3513, '每季度', '附加服务', 29, '按年龄计算', '邮寄申请', '收入证明', '北京', '停售'),
  (2305, '家庭保险', '汽车保险', '100万-500万', '5年', 9673, '每季度', '免赔额', 48, '按年龄计算', '在线申请', '健康问卷', '成都', '可用'),
  (6527, '意外险', '家庭保险', '50万-200万', '1年', 1144, '每年', '附加服务', 54, '按年龄计算', '在线申请', '健康问卷', '成都', '停售'),
  (1516, '家庭保险', '家庭保险', '50万-200万', '10年', 2281, '每年', '免赔额', 28, '按年龄计算', '在线申请', '健康问卷', '深圳', '停售'),
  (8261, '寿险', '家庭保险', '100万-500万', '5年', 1080, '每年', '附加服务', 31, '按年龄计算', '电话申请', '健康问卷', '成都', '停售'),
  (6638, '寿险', '家庭保险', '100万-500万', '10年', 5302, '每年', '免赔额', 38, '按年龄计算', '电话申请', '收入证明', '上海', '下架'),
  (5756, '医疗保险', '医疗保险', '100万-500万', '5年', 3460, '每年', '保额递增', 18, '按健康状况计算', '邮寄申请', '收入证明', '北京', '停售');

-- ----------------------------
-- crs_orders
-- ----------------------------
drop table if exists public.crs_orders;
create table public.crs_orders (
  order_time timestamp,
  crs_user_id bigint,
  eco_main_order_id text,
  channel text,
  status_code text,
  hotel_code text,
  reserved_roomtype_code text,
  actual_roomtype_code text,
  rate_code text,
  rooms bigint,
  rns bigint,
  adults bigint,
  children bigint,
  no_guests bigint,
  total_revenue double precision,
  city text,
  province text,
  age bigint,
  gender text,
  arrival timestamp,
  departure timestamp,
  event_timestamp bigint,
  eventid text,
  offset_code text,
  productid text
);

insert into public.crs_orders values
  ('2023-02-21 01:44:00', 16258, 'ORD402692', 'TAS', 'checkout', 'NUPEK11', 'D2Q', 'D2Q', 'TABAR', 2, 2, 3, 3, 6, 478.6, '北京市', '北京', 18, 'F', '2023-02-21 01:44:00', '2023-02-23 01:44:00', 1676915040, 'EVT869962', 'OFF22635', 'App'),
  ('2023-03-11 04:38:22', 73100, 'ORD203772', 'TAS', 'checkout', 'ULPEK10', 'D2Q', 'D2Q', 'FLI618G', 2, 4, 4, 2, 6, 838.36, '上海市', '上海', 32, 'M', '2023-03-11 04:38:22', '2023-03-12 04:38:22', 1678480702, 'EVT508794', 'OFF86528', 'App'),
  ('2023-01-08 09:03:54', 66608, 'ORD517695', 'FLI', 'checkout', 'ULPEK10', 'D2Q', 'D2Q', 'FLI618G', 4, 4, 1, 0, 1, 958.13, '北京市', '北京', 49, 'M', '2023-01-08 09:03:54', '2023-01-09 09:03:54', 1673139834, 'EVT675098', 'OFF36718', 'App'),
  ('2023-12-03 02:32:55', 52955, 'ORD612940', 'TAS', 'checkout', 'ULPEK10', 'D2Q', 'D2Q', 'TABAR', 1, 1, 4, 0, 4, 256.91, '厦门市', '福建省', 55, 'M', '2023-12-03 02:32:55', '2023-12-05 02:32:55', 1701541975, 'EVT764058', 'OFF85663', 'WeChat Mini-program'),
  ('2023-09-27 14:14:54', 69732, 'ORD360068', 'TAS', 'checkout', 'NUPEK11', 'D2Q', 'D2Q', 'TABAR', 3, 3, 3, 2, 5, 462.3, '北京市', '北京', 26, 'F', '2023-09-27 14:14:54', '2023-09-29 14:14:54', 1695795294, 'EVT531411', 'OFF72880', 'WeChat Mini-program'),
  ('2023-05-25 22:05:02', 89525, 'ORD496395', 'TAS', 'checkout', 'NUPEK11', 'B2Q', 'B2Q', 'FLI618G', 5, 10, 2, 1, 3, 106.59, '重庆市', '重庆', 42, 'F', '2023-05-25 22:05:02', '2023-05-27 22:05:02', 1685023502, 'EVT596135', 'OFF99330', 'App'),
  ('2023-10-18 12:12:55', 44275, 'ORD891640', 'FLI', 'checkout', 'ULPEK10', 'B2Q', 'B2Q', 'TABAR', 5, 5, 3, 0, 3, 836.92, '北京市', '北京', 19, 'M', '2023-10-18 12:12:55', '2023-10-20 12:12:55', 1697602375, 'EVT277282', 'OFF22047', 'App'),
  ('2023-08-03 11:09:58', 96029, 'ORD166072', 'TAS', 'checkout', 'NUPEK11', 'B2Q', 'B2Q', 'FLI618G', 1, 1, 1, 3, 4, 761.61, '北京市', '北京', 50, 'F', '2023-08-03 11:09:58', '2023-08-04 11:09:58', 1691032198, 'EVT118054', 'OFF56708', 'App'),
  ('2023-05-22 05:33:59', 87818, 'ORD268727', 'TAS', 'checkout', 'NUPEK11', 'B2Q', 'B2Q', 'FLI618G', 3, 6, 4, 1, 5, 607.45, '北京市', '北京', 55, 'M', '2023-05-22 05:33:59', '2023-05-23 05:33:59', 1684704839, 'EVT264762', 'OFF72199', 'WeChat Mini-program'),
  ('2023-02-17 04:07:52', 43495, 'ORD545010', 'FLI', 'checkout', 'NUPEK11', 'D2Q', 'D2Q', 'TABAR', 2, 4, 1, 2, 3, 309.77, '青岛市', '山东省', 18, 'M', '2023-02-17 04:07:52', '2023-02-18 04:07:52', 1676578072, 'EVT952941', 'OFF70458', 'WeChat Mini-program');

-- ----------------------------
-- heros
-- ----------------------------
drop table if exists public.heros;
create table public.heros (
  id integer generated by default as identity primary key,
  name text not null,
  hp_max real,
  hp_growth real,
  hp_start real,
  mp_max real,
  mp_growth real,
  mp_start real,
  attack_max real,
  attack_growth real,
  attack_start real,
  defense_max real,
  defense_growth real,
  defense_start real,
  hp_5s_max real,
  hp_5s_growth real,
  hp_5s_start real,
  mp_5s_max real,
  mp_5s_growth real,
  mp_5s_start real,
  attack_speed_max real,
  attack_range text,
  role_main text,
  role_assist text,
  birthdate date
);

insert into public.heros (
  id, name, hp_max, hp_growth, hp_start, mp_max, mp_growth, mp_start, attack_max, attack_growth, attack_start,
  defense_max, defense_growth, defense_start, hp_5s_max, hp_5s_growth, hp_5s_start, mp_5s_max, mp_5s_growth, mp_5s_start,
  attack_speed_max, attack_range, role_main, role_assist, birthdate
) values
  (10000, '夏侯惇', 7350, 288.8, 3307, 1746, 94, 430, 321, 11.57, 159, 397, 21.14, 101, 98, 3.357, 51, 37, 1.571, 15, 0, '近战', '坦克', '战士', '2016-07-19'),
  (10001, '钟无艳', 7000, 275, 3150, 1760, 95, 430, 318, 11, 164, 409, 22.07, 100, 92, 3.143, 48, 37, 1.571, 15, 0, '近战', '战士', '坦克', '2021-05-01'),
  (10002, '钟', 8341, 329.4, 3450, 100, 0, 100, 301, 10.57, 153, 504, 27.07, 125, 115, 4.143, 57, 5, 0, 5, 0, '近战', '坦克', '辅助', '2012-05-04'),
  (10003, '牛魔', 8476, 352.8, 3537, 1926, 104, 470, 273, 8.357, 156, 394, 20.36, 109, 117, 4.214, 58, 42, 1.786, 17, 0, '近战', '坦克', '辅助', '2015-11-24'),
  (10004, '吕布', 7344, 270, 3564, 0, 0, 0, 343, 12.36, 170, 390, 20.79, 99, 97, 3.071, 54, 0, 0, 0, 0, '近战', '战士', '坦克', '2015-12-22'),
  (10005, '亚瑟', 8050, 316.3, 3622, 0, 0, 0, 346, 13, 164, 400, 21.57, 98, 106, 3.643, 55, 0, 0, 0, 0, '近战', '战士', '坦克', '2021-05-18'),
  (10006, '芈月', 6164, 281.5, 3105, 100, 0, 100, 289, 9.786, 152, 361, 19.5, 88, 77, 2.357, 44, 0, 0, 0, 0, '远程', '法师', '坦克', '2015-12-08'),
  (10007, '程咬金', 8611, 369.6, 3437, 0, 0, 0, 316, 11.07, 161, 504, 27.07, 125, 119, 4.429, 57, 0, 0, 0, 0, '近战', '坦克', '战士', '2021-05-18'),
  (10008, '廉颇', 9328, 412.1, 3558, 1708, 92, 420, 286, 8.786, null, 514, 27.29, 132, 128, 4.929, 59, 36, 1.5, 15, 0, '近战', '坦克', null, '2021-05-18'),
  (10009, '东皇太一', 7669, 319.1, 3201, 1926, 104, 470, 286, 8.786, 163, 360, 18.64, 99, 106, 3.786, 53, 42, 1.786, 17, 0, '近战', '坦克', null, '2017-03-30');

commit;

