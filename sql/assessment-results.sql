-- ============================================================
-- 专业适配测评 — 结果保存表
-- 每人只保留最新一份测评结果 (UNIQUE user_id)
-- ============================================================

CREATE TABLE IF NOT EXISTS assessment_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL UNIQUE REFERENCES user_profiles(id) ON DELETE CASCADE,
  answers JSONB NOT NULL,
  results JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_assessment_results_user ON assessment_results(user_id);

-- RLS
ALTER TABLE assessment_results ENABLE ROW LEVEL SECURITY;

-- 用户只能管理自己的结果
CREATE POLICY "Users can select own results" ON assessment_results
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own results" ON assessment_results
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own results" ON assessment_results
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own results" ON assessment_results
  FOR DELETE USING (auth.uid() = user_id);
