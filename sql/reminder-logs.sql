-- ============================================================
-- 专业星图 — 召回提醒日志表
-- 防止对同一用户在 7 天内重复发送召回邮件
-- ============================================================

CREATE TABLE IF NOT EXISTS reminder_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  reminded_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_reminder_logs_user_id ON reminder_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_reminder_logs_reminded_at ON reminder_logs(reminded_at);

COMMENT ON TABLE reminder_logs IS '召回邮件发送日志，用于 7 天去重';

-- ============================================================
-- RPC: 查询符合召回条件的用户
-- 返回 7+ 天未登录 + email_follow_up=true + 7 天内未被提醒的用户
-- ============================================================

CREATE OR REPLACE FUNCTION get_remind_targets()
RETURNS TABLE (
  user_id UUID,
  email TEXT,
  days_inactive INTEGER,
  last_sign_in TIMESTAMPTZ
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY
  SELECT
    u.id AS user_id,
    u.email::TEXT,
    EXTRACT(DAY FROM (now() - u.last_sign_in_at))::INTEGER AS days_inactive,
    u.last_sign_in_at
  FROM auth.users u
  JOIN public.assessment_results a ON a.user_id = u.id
  WHERE
    a.email_follow_up = true
    AND u.last_sign_in_at IS NOT NULL
    AND u.last_sign_in_at < now() - INTERVAL '7 days'
    AND NOT EXISTS (
      SELECT 1 FROM public.reminder_logs rl
      WHERE rl.user_id = u.id AND rl.reminded_at > now() - INTERVAL '7 days'
    )
  ORDER BY u.last_sign_in_at ASC;
END;
$$;
