
-- 专业星图 - 数据库初始化脚本
-- 版本：v1.0
-- 日期：2026-05-20

-- 创建用户扩展信息表
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    phone VARCHAR(20) UNIQUE,
    points_balance INTEGER DEFAULT 0 CHECK (points_balance &gt;= 0),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin')),
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
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    download_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建点数套餐表
CREATE TABLE IF NOT EXISTS point_packages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    points INTEGER NOT NULL CHECK (points &gt; 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price &gt;= 0),
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
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'cancelled', 'refunded')),
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

-- 启用 Row Level Security
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE point_packages ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE download_records ENABLE ROW LEVEL SECURITY;

-- user_profiles 表的 RLS 策略
CREATE POLICY "用户只能查看自己的信息"
ON user_profiles FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "用户可以更新自己的信息"
ON user_profiles FOR UPDATE
USING (auth.uid() = id);

CREATE POLICY "管理员可以查看所有用户"
ON user_profiles FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

CREATE POLICY "管理员可以更新所有用户"
ON user_profiles FOR UPDATE
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- reports 表的 RLS 策略
CREATE POLICY "登录用户可查看已发布报告"
ON reports FOR SELECT
USING (
    auth.role() = 'authenticated' AND status = 'published'
);

CREATE POLICY "管理员可管理报告"
ON reports FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- point_packages 表的 RLS 策略
CREATE POLICY "公开查看套餐"
ON point_packages FOR SELECT
USING (is_active = true);

CREATE POLICY "管理员管理套餐"
ON point_packages FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- orders 表的 RLS 策略
CREATE POLICY "用户只能查看自己的订单"
ON orders FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "用户只能创建订单"
ON orders FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "用户可以更新自己的订单"
ON orders FOR UPDATE
USING (auth.uid() = user_id);

CREATE POLICY "管理员查看所有订单"
ON orders FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- download_records 表的 RLS 策略
CREATE POLICY "用户只能查看自己的下载记录"
ON download_records FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "用户可以插入自己的下载记录"
ON download_records FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "管理员查看所有下载记录"
ON download_records FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM user_profiles
        WHERE id = auth.uid() AND role = 'admin'
    )
);

-- 创建自动更新 updated_at 的触发器函数
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为所有需要的表添加触发器
CREATE TRIGGER update_user_profiles_modtime
BEFORE UPDATE ON user_profiles
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_reports_modtime
BEFORE UPDATE ON reports
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_packages_modtime
BEFORE UPDATE ON point_packages
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

-- 插入默认点数套餐数据
INSERT INTO point_packages (name, description, points, price, sort_order) VALUES
('体验套餐', '尝试下载1份报告', 1, 1.00, 1),
('基础套餐', '适合普通需求', 10, 9.90, 2),
('推荐套餐', '性价比最高，购买最多', 20, 18.90, 3),
('畅享套餐', '满足深度调研需求', 50, 39.90, 4),
('尊享套餐', '专业调研，长期使用', 100, 69.90, 5)
ON CONFLICT (id) DO NOTHING;
