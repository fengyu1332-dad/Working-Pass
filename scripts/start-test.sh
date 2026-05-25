#!/bin/bash
# 专业星图系统 - 快速测试启动脚本
# 作者: Claude AI
# 日期: 2026-05-23

echo "========================================"
echo "  专业星图 - 系统测试启动器"
echo "========================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查当前目录
if [ ! -f "verify_system.js" ]; then
    echo -e "${RED}❌ 请在项目根目录运行此脚本${NC}"
    echo "当前目录: $(pwd)"
    exit 1
fi

# 显示菜单
echo -e "${BLUE}请选择要执行的操作:${NC}"
echo ""
echo "1️⃣  运行系统验证（快速检查）"
echo "2️⃣  启动本地服务器（用于前端测试）"
echo "3️⃣  导入报告数据到数据库"
echo "4️⃣  上传PDF文件到Storage"
echo "5️⃣  运行所有Python依赖检查"
echo "6️⃣  查看测试指南文档"
echo "7️⃣  查看部署指南"
echo "8️⃣  退出"
echo ""

read -p "请输入选项 (1-8): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}🚀 正在运行系统验证...${NC}"
        echo ""
        if command -v node &> /dev/null; then
            node verify_system.js
        else
            echo -e "${RED}❌ Node.js 未安装${NC}"
            echo "请先安装 Node.js: https://nodejs.org/"
        fi
        ;;
    
    2)
        echo ""
        echo -e "${GREEN}🚀 正在启动本地服务器...${NC}"
        echo -e "${YELLOW}服务器将在 http://localhost:8000 启动${NC}"
        echo -e "${YELLOW}打开浏览器访问:${NC}"
        echo "   - 主页: http://localhost:8000/index.html"
        echo "   - 测试工具: http://localhost:8000/test-tool.html"
        echo "   - 用户报告: http://localhost:8000/user/reports.html"
        echo ""
        echo -e "${YELLOW}按 Ctrl+C 停止服务器${NC}"
        echo ""
        
        # 检查Python
        if command -v python3 &> /dev/null; then
            python3 -m http.server 8000
        elif command -v python &> /dev/null; then
            python -m http.server 8000
        else
            echo -e "${RED}❌ Python 未安装${NC}"
            echo "请先安装 Python 或使用其他方式启动服务器"
        fi
        ;;
    
    3)
        echo ""
        echo -e "${GREEN}🚀 正在导入报告数据...${NC}"
        echo ""
        if command -v node &> /dev/null; then
            node import_reports_to_db.js
        else
            echo -e "${RED}❌ Node.js 未安装${NC}"
        fi
        ;;
    
    4)
        echo ""
        echo -e "${GREEN}🚀 正在上传PDF文件...${NC}"
        echo ""
        if command -v node &> /dev/null; then
            # 检查是否安装了依赖
            if [ ! -d "node_modules" ]; then
                echo "正在安装依赖..."
                npm install @supabase/supabase-js
            fi
            node upload_reports_to_storage.js
        else
            echo -e "${RED}❌ Node.js 未安装${NC}"
        fi
        ;;
    
    5)
        echo ""
        echo -e "${GREEN}🚀 正在检查Python依赖...${NC}"
        echo ""
        if command -v python3 &> /dev/null; then
            if [ -f "scripts/test_system.py" ]; then
                python3 scripts/test_system.py
            else
                echo -e "${RED}❌ 测试脚本不存在${NC}"
            fi
        else
            echo -e "${RED}❌ Python3 未安装${NC}"
        fi
        ;;
    
    6)
        echo ""
        echo -e "${GREEN}📖 正在打开测试指南...${NC}"
        echo ""
        if command -v cat &> /dev/null; then
            cat TEST_GUIDE.md
        else
            echo -e "${YELLOW}请直接查看文件: TEST_GUIDE.md${NC}"
        fi
        ;;
    
    7)
        echo ""
        echo -e "${GREEN}📖 正在打开部署指南...${NC}"
        echo ""
        if command -v cat &> /dev/null; then
            cat DEPLOYMENT_GUIDE.md
        else
            echo -e "${YELLOW}请直接查看文件: DEPLOYMENT_GUIDE.md${NC}"
        fi
        ;;
    
    8)
        echo ""
        echo -e "${GREEN}👋 再见！${NC}"
        exit 0
        ;;
    
    *)
        echo -e "${RED}❌ 无效选项${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ 操作完成${NC}"
echo ""
echo "其他有用的命令："
echo "  - 查看项目结构: ls -la"
echo "  - 查看README: cat README.md"
echo "  - 查看所有测试文件: ls -la *.md"
echo ""
