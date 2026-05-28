-- =======================================================
-- 专业星图 - majors 表字段补充
-- 日期：2026-05-27
-- 说明：添加管理后台需要的字段，补齐数据库与前端/管理端的字段差异
-- =======================================================

-- 添加学位字段
ALTER TABLE majors ADD COLUMN IF NOT EXISTS degree VARCHAR(20);

-- 添加学制字段（年）
ALTER TABLE majors ADD COLUMN IF NOT EXISTS duration INTEGER;

-- 添加就业方向字段（JSONB 数组）
ALTER TABLE majors ADD COLUMN IF NOT EXISTS career_directions JSONB;

-- 为 RLS 策略添加 majors 表的管理员策略（如果还不存在）
-- 注意：当前 majors 表可能没有 RLS 或已有公开访问策略
-- 如果需要限制写入权限，请取消以下注释：

-- ALTER TABLE majors ENABLE ROW LEVEL SECURITY;
-- DROP POLICY IF EXISTS "管理员可管理专业库" ON majors;
-- CREATE POLICY "管理员可管理专业库" ON majors FOR ALL USING (
--   EXISTS (SELECT 1 FROM user_profiles up WHERE up.id = auth.uid() AND up.role = 'admin')
-- );
-- DROP POLICY IF EXISTS "公开查看专业库" ON majors;
-- CREATE POLICY "公开查看专业库" ON majors FOR SELECT USING (true);

DO $$
BEGIN
  RAISE NOTICE '✅ majors 表字段补充完成！';
  RAISE NOTICE '新增字段: degree (VARCHAR), duration (INTEGER), career_directions (JSONB)';
END $$;
