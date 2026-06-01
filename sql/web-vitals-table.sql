-- ============================================================
-- 专业星图 - Web Vitals 性能监控表
-- 日期: 2026-05-31
-- ============================================================

CREATE TABLE IF NOT EXISTS web_vitals (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(20) NOT NULL,
  value DECIMAL(10, 2) NOT NULL,
  rating VARCHAR(20),
  page VARCHAR(255),
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_web_vitals_name ON web_vitals(name);
CREATE INDEX IF NOT EXISTS idx_web_vitals_created_at ON web_vitals(created_at);

-- RLS: 公开写入（sendBeacon 不携带 auth），仅管理员可读
ALTER TABLE web_vitals ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "公开写入性能数据" ON web_vitals;
CREATE POLICY "公开写入性能数据" ON web_vitals
  FOR INSERT
  WITH CHECK (true);

DROP POLICY IF EXISTS "管理员查看性能数据" ON web_vitals;
CREATE POLICY "管理员查看性能数据" ON web_vitals
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_profiles up
      WHERE up.id = auth.uid() AND up.role = 'admin'
    )
  );
