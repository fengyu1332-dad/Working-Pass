-- 网站统计表：累计访问次数 + 累计停留时长
-- 在 Supabase SQL Editor 中执行

CREATE TABLE IF NOT EXISTS site_stats (
  id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  visit_count BIGINT NOT NULL DEFAULT 0,
  total_seconds BIGINT NOT NULL DEFAULT 0
);

INSERT INTO site_stats (id, visit_count, total_seconds)
VALUES (1, 123, 30000)
ON CONFLICT (id) DO NOTHING;

-- 如果需要重置已有数据为初始值，取消注释下行：
-- UPDATE site_stats SET visit_count = 123, total_seconds = 30000 WHERE id = 1;

-- 原子递增访问次数，返回新值
CREATE OR REPLACE FUNCTION increment_visit()
RETURNS BIGINT
LANGUAGE sql
SECURITY DEFINER
AS $$
  UPDATE site_stats SET visit_count = visit_count + 1 WHERE id = 1
  RETURNING visit_count;
$$;

-- 原子累加停留秒数，返回新总值
CREATE OR REPLACE FUNCTION add_site_time(p_seconds BIGINT)
RETURNS BIGINT
LANGUAGE sql
SECURITY DEFINER
AS $$
  UPDATE site_stats SET total_seconds = total_seconds + p_seconds WHERE id = 1
  RETURNING total_seconds;
$$;

-- 一次性获取全部统计
CREATE OR REPLACE FUNCTION get_site_stats()
RETURNS TABLE(visit_count BIGINT, total_seconds BIGINT)
LANGUAGE sql
SECURITY DEFINER
AS $$
  SELECT visit_count, total_seconds FROM site_stats WHERE id = 1;
$$;

-- 允许匿名用户调用
GRANT EXECUTE ON FUNCTION increment_visit() TO anon, authenticated;
GRANT EXECUTE ON FUNCTION add_site_time(BIGINT) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION get_site_stats() TO anon, authenticated;
