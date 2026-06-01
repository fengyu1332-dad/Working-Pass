-- ============================================================
-- 专业星图 - 管理操作审计日志
-- 日期: 2026-05-31
-- ============================================================

-- 1. 审计日志表
CREATE TABLE IF NOT EXISTS admin_audit_logs (
  id BIGSERIAL PRIMARY KEY,
  admin_id UUID NOT NULL,
  action VARCHAR(50) NOT NULL,
  resource VARCHAR(50) NOT NULL,
  resource_id VARCHAR(100),
  detail JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_admin_id ON admin_audit_logs(admin_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON admin_audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_created_at ON admin_audit_logs(created_at);

-- 2. RLS: 仅管理员可读写
ALTER TABLE admin_audit_logs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "管理员查看审计日志" ON admin_audit_logs;
CREATE POLICY "管理员查看审计日志" ON admin_audit_logs
  FOR SELECT
  USING (is_admin());

DROP POLICY IF EXISTS "管理员写入审计日志" ON admin_audit_logs;
CREATE POLICY "管理员写入审计日志" ON admin_audit_logs
  FOR INSERT
  WITH CHECK (is_admin());

-- 3. 便捷函数：记录审计日志
CREATE OR REPLACE FUNCTION log_admin_action(
  p_action VARCHAR(50),
  p_resource VARCHAR(50),
  p_resource_id VARCHAR(100) DEFAULT NULL,
  p_detail JSONB DEFAULT NULL
) RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  INSERT INTO public.admin_audit_logs (admin_id, action, resource, resource_id, detail)
  VALUES (auth.uid(), p_action, p_resource, p_resource_id, p_detail);
END;
$$;
