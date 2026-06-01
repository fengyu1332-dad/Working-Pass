-- ============================================================
-- 专业星图 - majors 表 RLS 安全策略
-- 日期: 2026-05-31
-- 说明: 限制 majors 表写入权限为管理员，防止匿名写入
-- ============================================================

-- 1. 启用行级安全
ALTER TABLE majors ENABLE ROW LEVEL SECURITY;

-- 2. 公开查看策略（保持现有行为：匿名和登录用户均可查看）
DROP POLICY IF EXISTS "公开查看专业库" ON majors;
CREATE POLICY "公开查看专业库" ON majors
  FOR SELECT
  USING (true);

-- 3. 管理员写入策略（复用 is_admin() 安全函数，避免递归）
DROP POLICY IF EXISTS "管理员管理专业库" ON majors;
CREATE POLICY "管理员管理专业库" ON majors
  FOR ALL
  USING (is_admin())
  WITH CHECK (is_admin());

-- 4. 验证
DO $$
BEGIN
  RAISE NOTICE '✅ majors 表 RLS 安全策略已启用';
  RAISE NOTICE '   - 匿名/登录用户: SELECT (只读)';
  RAISE NOTICE '   - 管理员: ALL (增删改查)';
END $$;
