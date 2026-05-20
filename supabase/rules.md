# Supabase 配置說明文檔

## 目錄
- [項目創建](#項目創建)
- [數據庫初始化](#數據庫初始化)
- [獲取配置信息](#獲取配置信息)
- [配置前端](#配置前端)
- [創建管理員賬號](#創建管理員賬號)

---

## 項目創建

### 1. 訪問 Supabase 官網
打開瀏覽器訪問 [Supabase 官網](https://supabase.com/)

### 2. 註冊/登錄
- 點擊 "Start your project" 按鈕
- 可以使用 GitHub、Google 或郵箱註冊

### 3. 創建新項目
1. 點擊 "New Project" 按鈕
2. 填寫項目信息：
   - **Organization**: 選擇組織或創建新組織
   - **Name**: 輸入項目名稱（如：`zhuanye-xingtu`）
   - **Database Password**: 設置強密碼（建議使用密碼生成器）
   - **Region**: 選擇最近的區域（建議選擇 `Northeast Asia (Tokyo)` 或 `Southeast Asia (Singapore)`）
3. 點擊 "Create new project" 等待項目創建（約2分鐘）

---

## 數據庫初始化

### 1. 打開 SQL Editor
在 Supabase 儀表板左側菜單點擊 **SQL Editor**

### 2. 執行初始化腳本
1. 點擊 **New Query** 按鈕
2. 複製 `/workspace/supabase/init.sql` 文件中的所有內容
3. 粘貼到 SQL Editor 中
4. 點擊 **Run** 按鈕執行

### 3. 驗證初始化結果
執行成功後可以運行以下命令驗證：

```sql
-- 查看錶是否創建成功
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- 查看默認套餐是否插入成功
SELECT * FROM point_packages;

-- 查看錶結構
\d users
\d reports
\d point_packages
\d orders
\d download_records
```

---

## 獲取配置信息

### 1. 進入項目設置
在 Supabase 儀表板左側點擊 **Settings**（齒輪圖標）

### 2. 獲取 API 配置
點擊 **API** 標籤頁，找到以下信息：

- **Project URL**: 類似 `https://xxxxx.supabase.co`
- **anon public**: 類似 `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- **service_role secret**: 類似 `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`（可選，用於後台管理）

### 3. 開啟 Email 登錄（可選）
如果需要 Email 登錄功能：
1. 左側菜單點擊 **Authentication**
2. 點擊 **Providers**
3. 啟用 **Email** 提供商
4. 配置郵箱驗證（可選）

### 4. 開啟 Phone 登錄（可選）
如果需要手機號登錄功能：
1. 左側菜單點擊 **Authentication**
2. 點擊 **Providers**
3. 啟用 **Phone** 提供商
4. 獲取 Twilio 配置（需要在 Twilio 官網申請）

---

## 配置前端

### 1. 創建配置文件
在 `/workspace/js/` 目錄下創建 `supabase-config.js` 文件（如果不存在）

### 2. 填寫配置信息
```javascript
const SUPABASE_URL = '你的Project URL';
const SUPABASE_ANON_KEY = '你的anon public key';

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
```

### 3. 配置示例
```javascript
// js/supabase-config.js
const SUPABASE_URL = 'https://xxxxx.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4eHh4IiwiYXVkIjoic3VwYWJhc2UiLCJpbnN1YiI6ImFkbWluIiwicm9sZSI6ImFub24iLCJpYXQiOjE2MzA1MDAwMDAsImV4cCI6MTkzMjA3NjAwMH0.xxxxxxxx';
```

---

## 創建管理員賬號

### 方法一：通過 Supabase Dashboard

1. 左側菜單點擊 **Authentication**
2. 點擊 **Users**
3. 點擊 **Add user** 按鈕
4. 填寫用戶信息：
   - **Email**: 管理員郵箱
   - **Phone**: 管理員手機號（可選）
   - **Password**: 設置密碼
   - **User metadata**: 可以添加姓名等信息
5. 點擊 **Create user**

### 方法二：通過 SQL

```sql
-- 插入管理員用戶
INSERT INTO users (email, role, points_balance)
VALUES ('admin@example.com', 'admin', 999999)
ON CONFLICT (email) DO UPDATE 
SET role = 'admin', points_balance = 999999;
```

### 方法三：提升現有用戶為管理員

```sql
-- 將指定用戶提升為管理員
UPDATE users 
SET role = 'admin' 
WHERE id = '用戶UUID';
```

---

## 安全建議

### 1. Row Level Security (RLS)
建議為每個表啟用 RLS 策略：

```sql
-- 為 users 表啟用 RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- 創建策略：用戶只能查看和修改自己的數據
CREATE POLICY "Users can view own data"
    ON users FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own data"
    ON users FOR UPDATE
    USING (auth.uid() = id);
```

### 2. 環境變量
在生產環境中，建議使用環境變量而不是硬編碼：

```javascript
// 生產環境
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;
```

### 3. 定期備份
在 Supabase Dashboard 的 **Database** -> **Backups** 中配置自動備份

---

## 故障排除

### 常見問題

#### Q1: SQL 執行失敗怎麼辦？
A: 
- 檢查錯誤信息，可能是錶已存在
- 使用 `DROP TABLE IF EXISTS table_name;` 刪除後重新創建
- 確保在正確的 schema 中執行（默認為 public）

#### Q2: API 連接失敗怎麼辦？
A:
- 檢查 URL 和 Key 是否正確
- 確認項目是否處於活跃狀態
- 檢查網絡連接是否正常

#### Q3: 用戶無法登錄怎麼辦？
A:
- 檢查 Authentication 配置是否正確
- 確認用戶是否已驗證郵箱/手機
- 查看 Users 日誌排查具體錯誤

---

## 技術支持

如有問題，請參考：
- [Supabase 文檔](https://supabase.com/docs)
- [Supabase Discord 社區](https://discord.gg/supabase)
- [GitHub Issues](https://github.com/supabase/supabase/issues)
