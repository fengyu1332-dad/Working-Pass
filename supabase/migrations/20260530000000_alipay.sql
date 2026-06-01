-- ============================================================
-- 支付宝电脑网站支付集成 — 数据库变更
-- ============================================================

-- 1. orders 表新增支付宝相关列
ALTER TABLE orders ADD COLUMN IF NOT EXISTS alipay_trade_no VARCHAR(64);
ALTER TABLE orders ADD COLUMN IF NOT EXISTS alipay_order_str TEXT;

CREATE INDEX IF NOT EXISTS idx_orders_alipay_trade_no ON orders(alipay_trade_no);
CREATE INDEX IF NOT EXISTS idx_orders_status_created ON orders(status, created_at);

-- 2. point_packages 新增列（前端已引用但列不存在）
ALTER TABLE point_packages ADD COLUMN IF NOT EXISTS original_price DECIMAL(10, 2);
ALTER TABLE point_packages ADD COLUMN IF NOT EXISTS featured BOOLEAN DEFAULT false;

-- 3. 更新已有套餐数据
UPDATE point_packages SET original_price = 1.99, featured = false WHERE name = '体验套餐' AND original_price IS NULL;
UPDATE point_packages SET original_price = 15.90, featured = false WHERE name = '基础套餐' AND original_price IS NULL;
UPDATE point_packages SET original_price = 24.90, featured = true WHERE name = '推荐套餐' AND original_price IS NULL;
UPDATE point_packages SET original_price = 59.90, featured = false WHERE name = '畅享套餐' AND original_price IS NULL;
UPDATE point_packages SET original_price = 99.90, featured = false WHERE name = '尊享套餐' AND original_price IS NULL;

-- 4. 收紧 orders RLS：用户只能取消自己的待支付订单
DROP POLICY IF EXISTS "用户可以更新自己的订单" ON orders;
DROP POLICY IF EXISTS "orders_user_cancel" ON orders;
DROP POLICY IF EXISTS "orders_own_update" ON orders;

CREATE POLICY "orders_user_cancel" ON orders
  FOR UPDATE
  USING (auth.uid() = user_id AND status = 'pending')
  WITH CHECK (status = 'cancelled');

-- 5. 原子化支付宝入账函数
CREATE OR REPLACE FUNCTION complete_alipay_order(
  p_order_id UUID,
  p_alipay_trade_no VARCHAR(64),
  p_payment_amount DECIMAL(10, 2)
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  v_order public.orders%ROWTYPE;
  v_new_balance INTEGER;
BEGIN
  -- 锁定订单行，防止并发修改
  SELECT * INTO v_order FROM public.orders WHERE id = p_order_id FOR UPDATE;

  IF NOT FOUND THEN
    RETURN jsonb_build_object('success', false, 'error', '订单不存在');
  END IF;

  -- 幂等性：同交易号已处理则直接返回成功
  IF v_order.status = 'paid' AND v_order.alipay_trade_no = p_alipay_trade_no THEN
    RETURN jsonb_build_object('success', true, 'message', '订单已处理', 'already_paid', true);
  END IF;

  -- 安全检查：已支付但交易号不同
  IF v_order.status = 'paid' AND v_order.alipay_trade_no IS NOT NULL AND v_order.alipay_trade_no != p_alipay_trade_no THEN
    RETURN jsonb_build_object('success', false, 'error', '订单已被另一笔支付处理');
  END IF;

  -- 只处理待支付订单
  IF v_order.status != 'pending' THEN
    RETURN jsonb_build_object('success', false, 'error', '订单状态不允许支付，当前状态: ' || v_order.status);
  END IF;

  -- 过期检查
  IF v_order.expires_at IS NOT NULL AND v_order.expires_at < NOW() THEN
    RETURN jsonb_build_object('success', false, 'error', '订单已过期');
  END IF;

  -- 金额一致性校验（0.01 容差）
  IF ABS(v_order.amount - p_payment_amount) > 0.01 THEN
    RETURN jsonb_build_object('success', false, 'error', '支付金额与订单金额不一致');
  END IF;

  -- 更新订单状态
  UPDATE public.orders SET
    status = 'paid',
    payment_method = 'alipay',
    alipay_trade_no = p_alipay_trade_no,
    paid_at = NOW()
  WHERE id = p_order_id;

  -- 原子增量更新用户余额
  UPDATE public.user_profiles
  SET points_balance = points_balance + v_order.points,
      updated_at = NOW()
  WHERE id = v_order.user_id
  RETURNING points_balance INTO v_new_balance;

  RETURN jsonb_build_object(
    'success', true,
    'new_balance', v_new_balance,
    'user_id', v_order.user_id,
    'points', v_order.points
  );
END;
$$;
