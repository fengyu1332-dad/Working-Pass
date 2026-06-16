-- ============================================================
-- 专业星图 — 邮件订阅偏好
-- 为测评结果表添加 email_follow_up 字段
-- ============================================================

ALTER TABLE assessment_results
ADD COLUMN IF NOT EXISTS email_follow_up BOOLEAN DEFAULT false;

COMMENT ON COLUMN assessment_results.email_follow_up IS '用户是否同意接收匹配专业相关的邮件通知';
