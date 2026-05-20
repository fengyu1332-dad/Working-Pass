
-- 专业星图 - 数据库初始化脚本（简化版）
-- 版本：v1.2
-- 日期：2026-05-20

-- ==========================================
-- Step 1: 创建表（使用 CREATE TABLE IF NOT EXISTS）
-- ==========================================

-- 创建用户扩展信息表
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    phone VARCHAR(20) UNIQUE,
    points_balance INTEGER DEFAULT 0,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建报告表
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    major_code VARCHAR(10) NOT NULL UNIQUE,
    major_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    preview_content TEXT,
    full_content TEXT,
    status VARCHAR(20) DEFAULT 'draft',
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建点数套餐表
CREATE TABLE IF NOT EXISTS point_packages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    points INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建订单表
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES user_profiles(id),
    package_id INTEGER NOT NULL REFERENCES point_packages(id),
    amount DECIMAL(10, 2) NOT NULL,
    points INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(20) DEFAULT 'mock',
    paid_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

-- 创建下载记录表
CREATE TABLE IF NOT EXISTS download_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES user_profiles(id),
    report_id UUID NOT NULL REFERENCES reports(id),
    points_spent INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- Step 2: 启用 Row Level Security (RLS)
-- ==========================================

ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE point_packages ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE download_records ENABLE ROW LEVEL SECURITY;

-- ==========================================
-- Step 3: 创建 RLS 策略（安全的方式创建）
-- ==========================================

-- user_profiles 表的 RLS 策略
DROP POLICY IF EXISTS "用户只能查看自己的信息" ON user_profiles;
CREATE POLICY "用户只能查看自己的信息"
ON user_profiles FOR SELECT
USING (auth.uid() = id);

DROP POLICY IF EXISTS "用户可以更新自己的信息" ON user_profiles;
CREATE POLICY "用户可以更新自己的信息"
ON user_profiles FOR UPDATE
USING (auth.uid() = id);

DROP POLICY IF EXISTS "管理员可以查看所有用户" ON user_profiles;
CREATE POLICY "管理员可以查看所有用户"
ON user_profiles FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

DROP POLICY IF EXISTS "管理员可以更新所有用户" ON user_profiles;
CREATE POLICY "管理员可以更新所有用户"
ON user_profiles FOR UPDATE
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- reports 表的 RLS 策略
DROP POLICY IF EXISTS "登录用户可查看已发布报告" ON reports;
CREATE POLICY "登录用户可查看已发布报告"
ON reports FOR SELECT
USING (
    auth.role() = 'authenticated' AND status = 'published'
);

DROP POLICY IF EXISTS "管理员可管理报告" ON reports;
CREATE POLICY "管理员可管理报告"
ON reports FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- point_packages 表的 RLS 策略
DROP POLICY IF EXISTS "公开查看套餐" ON point_packages;
CREATE POLICY "公开查看套餐"
ON point_packages FOR SELECT
USING (is_active = true);

DROP POLICY IF EXISTS "管理员管理套餐" ON point_packages;
CREATE POLICY "管理员管理套餐"
ON point_packages FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- orders 表的 RLS 策略
DROP POLICY IF EXISTS "用户只能查看自己的订单" ON orders;
CREATE POLICY "用户只能查看自己的订单"
ON orders FOR SELECT
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "用户只能创建订单" ON orders;
CREATE POLICY "用户只能创建订单"
ON orders FOR INSERT
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "用户可以更新自己的订单" ON orders;
CREATE POLICY "用户可以更新自己的订单"
ON orders FOR UPDATE
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "管理员查看所有订单" ON orders;
CREATE POLICY "管理员查看所有订单"
ON orders FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- download_records 表的 RLS 策略
DROP POLICY IF EXISTS "用户只能查看自己的下载记录" ON download_records;
CREATE POLICY "用户只能查看自己的下载记录"
ON download_records FOR SELECT
USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "用户可以插入自己的下载记录" ON download_records;
CREATE POLICY "用户可以插入自己的下载记录"
ON download_records FOR INSERT
WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "管理员查看所有下载记录" ON download_records;
CREATE POLICY "管理员查看所有下载记录"
ON download_records FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- ==========================================
-- Step 4: 创建触发器函数
-- ==========================================

CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- Step 5: 添加触发器（安全方式，先检查是否存在）
-- ==========================================

-- user_profiles 表触发器
DROP TRIGGER IF EXISTS update_user_profiles_modtime ON user_profiles;
CREATE TRIGGER update_user_profiles_modtime
BEFORE UPDATE ON user_profiles
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

-- reports 表触发器
DROP TRIGGER IF EXISTS update_reports_modtime ON reports;
CREATE TRIGGER update_reports_modtime
BEFORE UPDATE ON reports
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

-- point_packages 表触发器
DROP TRIGGER IF EXISTS update_packages_modtime ON point_packages;
CREATE TRIGGER update_packages_modtime
BEFORE UPDATE ON point_packages
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

-- ==========================================
-- Step 6: 插入默认点数套餐数据
-- ==========================================

-- 安全插入，如果已存在则跳过
INSERT INTO point_packages (name, description, points, price, sort_order)
SELECT * FROM (
    VALUES
    ('体验套餐', '尝试下载1份报告', 1, 1.00, 1),
    ('基础套餐', '适合普通需求', 10, 9.90, 2),
    ('推荐套餐', '性价比最高，购买最多', 20, 18.90, 3),
    ('畅享套餐', '满足深度调研需求', 50, 39.90, 4),
    ('尊享套餐', '专业调研，长期使用', 100, 69.90, 5)
) AS tmp(name, description, points, price, sort_order)
WHERE NOT EXISTS (
    SELECT 1 FROM point_packages WHERE name = tmp.name
);

