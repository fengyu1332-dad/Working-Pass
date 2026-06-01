-- =======================================================
-- 专业星图 - 积分扣减安全函数
-- 版本：v1.0
-- 日期：2026-05-28
-- 说明：将积分扣减逻辑从客户端迁移到数据库层，确保原子性和安全性
-- =======================================================

-- 创建原子化积分消费函数
CREATE OR REPLACE FUNCTION spend_points(p_report_id UUID)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  v_user_id UUID;
  v_balance INTEGER;
  v_report_exists BOOLEAN;
BEGIN
  -- 获取当前认证用户 ID
  v_user_id := auth.uid();

  IF v_user_id IS NULL THEN
    RETURN jsonb_build_object('success', false, 'error', '未登录');
  END IF;

  -- 检查报告是否存在且已发布
  SELECT EXISTS(
    SELECT 1 FROM public.reports WHERE id = p_report_id AND status = 'published'
  ) INTO v_report_exists;

  IF NOT v_report_exists THEN
    RETURN jsonb_build_object('success', false, 'error', '报告不存在或未发布');
  END IF;

  -- 检查是否已解锁（避免重复扣点）
  IF EXISTS(
    SELECT 1 FROM public.download_records
    WHERE user_id = v_user_id AND report_id = p_report_id
  ) THEN
    RETURN jsonb_build_object('success', false, 'error', '已解锁过此报告');
  END IF;

  -- 原子化扣点：使用 UPDATE + RETURNING 确保并发安全
  UPDATE public.user_profiles
  SET points_balance = points_balance - 1,
      updated_at = NOW()
  WHERE id = v_user_id
    AND points_balance >= 1
  RETURNING points_balance INTO v_balance;

  -- 如果 balance 为 NULL，说明点数不足或用户不存在
  IF v_balance IS NULL THEN
    RETURN jsonb_build_object('success', false, 'error', '点数不足，请先充值');
  END IF;

  -- 创建下载记录
  INSERT INTO public.download_records (user_id, report_id, points_spent)
  VALUES (v_user_id, p_report_id, 1);

  -- 增加报告下载计数
  UPDATE public.reports
  SET download_count = download_count + 1,
      updated_at = NOW()
  WHERE id = p_report_id;

  RETURN jsonb_build_object(
    'success', true,
    'new_balance', v_balance,
    'message', '解锁成功'
  );

EXCEPTION
  WHEN OTHERS THEN
    RETURN jsonb_build_object('success', false, 'error', SQLERRM);
END;
$$;
