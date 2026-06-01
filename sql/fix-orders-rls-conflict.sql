-- ============================================================
-- 专业星图 — 修复 orders 表 RLS 策略冲突
-- 日期：2026-05-31
--
-- 问题：fix-rls-policy-v2.sql 创建的 orders_own_update 策略
--       允许用户任意修改自己的订单（含金额、状态等），
--       与 alipay.sql 的 orders_user_cancel（仅允许取消）
--       共存时后者形同虚设。
--
-- 解决：删除 orders_own_update，保留 orders_user_cancel。
-- ============================================================

DROP POLICY IF EXISTS "orders_own_update" ON orders;

-- 验证：检查 orders 表的所有策略
DO $$
DECLARE
  r RECORD;
BEGIN
  RAISE NOTICE 'orders 表当前策略：';
  FOR r IN SELECT policyname, cmd, qual, with_check
    FROM pg_policies
    WHERE tablename = 'orders'
    ORDER BY policyname
  LOOP
    RAISE NOTICE '  - % (cmd=%, using=%, with_check=%)',
      r.policyname, r.cmd,
      COALESCE(r.qual::text, '(none)'),
      COALESCE(r.with_check::text, '(none)');
  END LOOP;
END $$;
