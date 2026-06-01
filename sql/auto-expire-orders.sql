-- ============================================================
-- 专业星图 - 订单过期自动处理
-- 日期: 2026-05-31
--
-- 1. 创建原子化过期函数
-- 2. 启用 pg_cron 并设置定时任务（每分钟执行一次）
-- ============================================================

-- 1. 原子化过期函数：将过期待支付订单标记为 expired
CREATE OR REPLACE FUNCTION expire_pending_orders()
RETURNS TABLE (oid UUID, uid UUID, cnt INTEGER)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  RETURN QUERY
  WITH expired AS (
    UPDATE public.orders
    SET status = 'expired'
    WHERE status = 'pending'
      AND expires_at IS NOT NULL
      AND expires_at < NOW()
    RETURNING id, user_id
  )
  SELECT
    e.id,
    e.user_id,
    (SELECT count(*) FROM expired)::INTEGER
  FROM expired e;
END;
$$;

-- 2. 启用 pg_cron 扩展（如果尚未启用）
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- 3. 设置定时任务：每分钟执行一次过期清理
SELECT cron.schedule(
  'expire-orders-every-minute',
  '* * * * *',
  'SELECT expire_pending_orders();'
);
