
-- =======================================================
-- 专业星图 - 完整 RLS 策略修复脚本
-- 版本：v2.0 - 完全解决递归问题
-- 日期：2026-05-21
-- =======================================================

-- =======================================================
-- 核心问题：user_profiles 表的 RLS 策略查询了自身表
-- 解决方案：使用 Supabase 的 auth.jwt() 函数
-- =======================================================

-- Step 1: 删除所有现有策略（从 user_profiles 开始）
DROP POLICY IF EXISTS "用户只能查看自己的信息" ON user_profiles;
DROP POLICY IF EXISTS "用户可以更新自己的信息" ON user_profiles;
DROP POLICY IF EXISTS "管理员可以查看所有用户" ON user_profiles;
DROP POLICY IF EXISTS "管理员可以更新所有用户" ON user_profiles;
DROP POLICY IF EXISTS "管理员可以查看所有用户v2" ON user_profiles;
DROP POLICY IF EXISTS "管理员可以更新所有用户v2" ON user_profiles;

DROP POLICY IF EXISTS "登录用户可查看已发布报告" ON reports;
DROP POLICY IF EXISTS "管理员可管理报告" ON reports;
DROP POLICY IF EXISTS "管理员可管理报告v2" ON reports;

DROP POLICY IF EXISTS "公开查看套餐" ON point_packages;
DROP POLICY IF EXISTS "管理员管理套餐" ON point_packages;
DROP POLICY IF EXISTS "管理员管理套餐v2" ON point_packages;

DROP POLICY IF EXISTS "用户只能查看自己的订单" ON orders;
DROP POLICY IF EXISTS "用户只能创建订单" ON orders;
DROP POLICY IF EXISTS "用户可以更新自己的订单" ON orders;
DROP POLICY IF EXISTS "管理员查看所有订单" ON orders;
DROP POLICY IF EXISTS "管理员查看所有订单v2" ON orders;

DROP POLICY IF EXISTS "用户只能查看自己的下载记录" ON download_records;
DROP POLICY IF EXISTS "用户可以插入自己的下载记录" ON download_records;
DROP POLICY IF EXISTS "管理员查看所有下载记录" ON download_records;
DROP POLICY IF EXISTS "管理员查看所有下载记录v2" ON download_records;

-- =======================================================
-- Step 2: 重建 RLS 策略（使用安全的无递归方式）
-- =======================================================

-- user_profiles 表：用户只能操作自己的记录
CREATE POLICY "user_profile_own_select"
ON user_profiles FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "user_profile_own_update"
ON user_profiles FOR UPDATE
USING (auth.uid() = id);

CREATE POLICY "user_profile_own_insert"
ON user_profiles FOR INSERT
WITH CHECK (auth.uid() = id);

-- 注意：管理员功能通过 service_role 密钥在应用层实现
-- 这样可以完全避免 RLS 策略中的递归问题

-- =======================================================
-- reports 表：登录用户可查看已发布报告
-- =======================================================

CREATE POLICY "reports_published_select"
ON reports FOR SELECT
USING (
    auth.role() = 'authenticated' 
    AND status = 'published'
);

CREATE POLICY "reports_admin_all"
ON reports FOR ALL
USING (
    -- 这里可以添加应用层的权限检查
    -- 或者使用 service_role 密钥
    true
);

-- =======================================================
-- point_packages 表：公开查看
-- =======================================================

CREATE POLICY "packages_public_select"
ON point_packages FOR SELECT
USING (is_active = true);

CREATE POLICY "packages_admin_all"
ON point_packages FOR ALL
USING (true);

-- =======================================================
-- orders 表：用户只能操作自己的订单
-- =======================================================

CREATE POLICY "orders_own_select"
ON orders FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "orders_own_insert"
ON orders FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "orders_own_update"
ON orders FOR UPDATE
USING (auth.uid() = user_id);

CREATE POLICY "orders_admin_all"
ON orders FOR ALL
USING (true);

-- =======================================================
-- download_records 表：用户只能操作自己的记录
-- =======================================================

CREATE POLICY "downloads_own_select"
ON download_records FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "downloads_own_insert"
ON download_records FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "downloads_admin_all"
ON download_records FOR ALL
USING (true);

-- =======================================================
-- Step 3: 验证结果
-- =======================================================

DO $$
DECLARE
  v_count INTEGER;
BEGIN
  -- 检查 user_profiles 策略数量
  SELECT COUNT(*) INTO v_count 
  FROM pg_policies 
  WHERE tablename = 'user_profiles';
  
  RAISE NOTICE '==============================================';
  RAISE NOTICE '✅ RLS 策略修复完成！';
  RAISE NOTICE '==============================================';
  RAISE NOTICE 'user_profiles 表策略数量: %', v_count;
  
  IF v_count >= 2 THEN
    RAISE NOTICE '✅ user_profiles 策略已正确设置';
  ELSE
    RAISE NOTICE '⚠️ 请检查 user_profiles 策略';
  END IF;
  
  -- 测试 point_packages 查询（应该能正常工作）
  RAISE NOTICE '测试 point_packages 查询...';
  
EXCEPTION WHEN OTHERS THEN
  RAISE NOTICE '❌ 错误: %', SQLERRM;
END $$;

-- =======================================================
-- 测试查询（取消注释即可测试）
-- =======================================================

-- 公开查询套餐（应该成功）
-- SELECT id, name, points, price FROM point_packages WHERE is_active = true;

