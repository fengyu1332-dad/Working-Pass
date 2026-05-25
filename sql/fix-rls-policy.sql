
-- 专业星图 - RLS 策略修复脚本
-- 版本：v1.0 - 修复递归错误
-- 日期：2026-05-21

-- =======================================================
-- 策略说明：
-- 关键修复：避免在 user_profiles 的 RLS 策略中查询 user_profiles 表
-- 解决方案：使用 service_role 密钥，或简化策略
-- =======================================================

-- Step 1: 删除所有现有的 user_profiles RLS 策略
DROP POLICY IF EXISTS "用户只能查看自己的信息" ON user_profiles;
DROP POLICY IF EXISTS "用户可以更新自己的信息" ON user_profiles;
DROP POLICY IF EXISTS "管理员可以查看所有用户" ON user_profiles;
DROP POLICY IF EXISTS "管理员可以更新所有用户" ON user_profiles;

-- Step 2: 创建简化版的 RLS 策略（避免自引用）
-- 方案A：只允许用户查看和更新自己的信息
CREATE POLICY "用户只能查看自己的信息"
ON user_profiles FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "用户可以更新自己的信息"
ON user_profiles FOR UPDATE
USING (auth.uid() = id);

CREATE POLICY "用户可以插入自己的信息"
ON user_profiles FOR INSERT
WITH CHECK (auth.uid() = id);

-- 注意：管理员查询暂时使用 service_role 密钥
-- 或在应用层通过 service_role 密钥来管理

-- =======================================================
-- 验证 RLS 策略
-- =======================================================

DO $$
BEGIN
  -- 验证 user_profiles 表的策略数量
  IF (SELECT COUNT(*) FROM pg_policies WHERE tablename = 'user_profiles') >= 2 THEN
    RAISE NOTICE '✅ user_profiles RLS 策略修复成功！';
  ELSE
    RAISE NOTICE '⚠️ user_profiles RLS 策略可能不完整，请检查';
  END IF;
END $$;

-- =======================================================
-- 测试查询（应该能正常工作）
-- =======================================================

-- 这个查询现在应该不会报错了
-- SELECT * FROM point_packages WHERE is_active = true;

