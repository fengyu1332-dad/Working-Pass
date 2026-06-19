-- ============================================================
-- 专业星图 - 推荐奖励系统数据库迁移
-- 日期: 2026-06-19
-- ============================================================

-- 1. user_profiles 增加 referred_by 列
ALTER TABLE user_profiles
  ADD COLUMN IF NOT EXISTS referred_by UUID REFERENCES auth.users(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_user_profiles_referred_by ON user_profiles(referred_by);

-- 2. 推荐奖励记录表
CREATE TABLE IF NOT EXISTS referral_rewards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    referrer_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    referred_user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    points_awarded INTEGER NOT NULL DEFAULT 3,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(referrer_id, referred_user_id)
);

CREATE INDEX IF NOT EXISTS idx_referral_rewards_referrer ON referral_rewards(referrer_id);
CREATE INDEX IF NOT EXISTS idx_referral_rewards_referred ON referral_rewards(referred_user_id);

-- 3. 原子化增加点数函数（防负余额）
CREATE OR REPLACE FUNCTION add_points(p_user_id UUID, p_points INTEGER)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  v_result JSONB;
BEGIN
  UPDATE user_profiles
    SET points_balance = points_balance + p_points,
        updated_at = NOW()
    WHERE id = p_user_id;

  IF NOT FOUND THEN
    RETURN jsonb_build_object('success', false, 'error', '用户不存在');
  END IF;

  RETURN jsonb_build_object('success', true);
END;
$$;

-- 4. 为 referral_rewards 表启用 RLS
ALTER TABLE referral_rewards ENABLE ROW LEVEL SECURITY;

-- 允许认证用户插入
DROP POLICY IF EXISTS "Allow insert for authenticated users" ON referral_rewards;
CREATE POLICY "Allow insert for authenticated users" ON referral_rewards
  FOR INSERT TO authenticated
  WITH CHECK (referrer_id = auth.uid());

-- 允许认证用户查询自己的推荐记录
DROP POLICY IF EXISTS "Allow select own records" ON referral_rewards;
CREATE POLICY "Allow select own records" ON referral_rewards
  FOR SELECT TO authenticated
  USING (referrer_id = auth.uid() OR referred_user_id = auth.uid());
