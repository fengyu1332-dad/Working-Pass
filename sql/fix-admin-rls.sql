-- ============================================================
-- 专业星图 - 收紧管理策略（USING(true) → 仅管理员）
-- 日期：2026-06-01
--
-- 问题：fix-rls-policy-v2.sql 的 *_admin_all 策略用 USING(true)
--       任何已登录用户都能通过 REST API 修改敏感表
-- 解决：创建 is_admin() 安全函数 + 替换策略
-- ============================================================

-- 1. 安全的管理员判断函数（SECURITY DEFINER 避免递归）
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = ''
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.user_profiles
    WHERE id = auth.uid() AND role = 'admin'
  );
$$;

-- 2. 删除旧的宽松策略
DROP POLICY IF EXISTS "reports_admin_all" ON reports;
DROP POLICY IF EXISTS "packages_admin_all" ON point_packages;
DROP POLICY IF EXISTS "orders_admin_all" ON orders;
DROP POLICY IF EXISTS "downloads_admin_all" ON download_records;

-- 3. 重建为仅管理员
CREATE POLICY "reports_admin_all" ON reports FOR ALL
  USING (is_admin());

CREATE POLICY "packages_admin_all" ON point_packages FOR ALL
  USING (is_admin());

CREATE POLICY "orders_admin_all" ON orders FOR ALL
  USING (is_admin());

CREATE POLICY "downloads_admin_all" ON download_records FOR ALL
  USING (is_admin());

-- 4. 验证
DO $$
DECLARE
  r RECORD;
BEGIN
  RAISE NOTICE '管理策略已收紧，当前 reports/orders/packages/downloads 策略：';
  FOR r IN
    SELECT tablename, policyname, cmd
    FROM pg_policies
    WHERE policyname LIKE '%admin%'
    ORDER BY tablename, policyname
  LOOP
    RAISE NOTICE '  % - % - %', r.tablename, r.policyname, r.cmd;
  END LOOP;
END $$;
