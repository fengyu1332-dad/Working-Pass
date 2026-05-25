#!/usr/bin/env python3
"""
专业星图 AI Agent 系统 - 环境设置脚本
帮助用户快速配置开发环境
"""

import os
import sys
import subprocess
from pathlib import Path


def print_step(step: str, message: str):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"步骤 {step}: {message}")
    print('='*60)


def check_python_version():
    """检查Python版本"""
    print_step("1", "检查Python版本")
    
    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python版本过低，需要Python 3.8或更高版本")
        return False
    
    print("✅ Python版本符合要求")
    return True


def check_git():
    """检查Git是否安装"""
    print_step("2", "检查Git")
    
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        print(f"✅ Git已安装: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ Git未安装")
        print("请从 https://git-scm.com 下载安装")
        return False


def create_virtual_environment():
    """创建虚拟环境"""
    print_step("3", "创建虚拟环境")
    
    venv_path = Path('.venv')
    
    if venv_path.exists():
        print("✅ 虚拟环境已存在")
        return True
    
    try:
        print("正在创建虚拟环境...")
        subprocess.run([sys.executable, '-m', 'venv', '.venv'], check=True)
        print("✅ 虚拟环境创建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 虚拟环境创建失败: {e}")
        return False


def install_dependencies():
    """安装依赖"""
    print_step("4", "安装Python依赖")
    
    # 获取虚拟环境中的pip
    if os.name == 'nt':  # Windows
        pip = '.venv\\Scripts\\pip'
        python = '.venv\\Scripts\\python'
    else:  # Unix/Linux/Mac
        pip = '.venv/bin/pip'
        python = '.venv/bin/python'
    
    try:
        print("正在安装依赖（可能需要几分钟）...")
        
        # 升级pip
        subprocess.run([python, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        
        # 安装requirements.txt中的依赖
        result = subprocess.run(
            [pip, 'install', '-r', 'requirements.txt'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 依赖安装成功")
            return True
        else:
            print(f"❌ 依赖安装失败:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 依赖安装失败: {e}")
        return False


def setup_environment_file():
    """创建环境变量文件"""
    print_step("5", "配置环境变量")
    
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env文件已存在")
        return True
    
    # 创建.env文件模板
    env_template = """# LLM API 配置 (选择其中一个)

# OpenAI (推荐)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Anthropic Claude (备选)
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# ANTHROPIC_MODEL=claude-3-opus

# 百度文心一言 (国内用户)
# BAIDU_API_KEY=your_baidu_api_key_here
# BAIDU_API_SECRET=your_baidu_api_secret_here

# Supabase 数据库配置
SUPABASE_URL=https://djteatwxjlnbjylynvjh.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# 系统配置
ENVIRONMENT=development
LOG_LEVEL=INFO
"""
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_template)
        
        print("✅ .env文件创建成功")
        print("⚠️  请编辑.env文件，填入您的API密钥")
        return True
        
    except Exception as e:
        print(f"❌ .env文件创建失败: {e}")
        return False


def verify_installation():
    """验证安装"""
    print_step("6", "验证安装")
    
    # 获取虚拟环境中的python
    if os.name == 'nt':  # Windows
        python = '.venv\\Scripts\\python'
    else:  # Unix/Linux/Mac
        python = '.venv/bin/python'
    
    try:
        # 测试导入关键库
        test_imports = [
            'requests',
            'openai',
            'anthropic',
            'pydantic',
            'loguru'
        ]
        
        for module in test_imports:
            result = subprocess.run(
                [python, '-c', f'import {module}'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"  ✅ {module}")
            else:
                print(f"  ❌ {module}")
                return False
        
        print("\n✅ 所有依赖验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False


def main():
    """主函数"""
    print("\n" + "="*60)
    print("专业星图 AI Agent 系统 - 环境设置")
    print("="*60)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查Git
    check_git()
    
    # 创建虚拟环境
    if not create_virtual_environment():
        sys.exit(1)
    
    # 安装依赖
    if not install_dependencies():
        sys.exit(1)
    
    # 配置环境变量
    if not setup_environment_file():
        sys.exit(1)
    
    # 验证安装
    if not verify_installation():
        sys.exit(1)
    
    # 完成
    print("\n" + "="*60)
    print("🎉 环境设置完成！")
    print("="*60)
    
    print("\n下一步操作:")
    print("1. 编辑 .env 文件，填入您的API密钥")
    print("2. 运行演示程序: python ai_agent_demo.py")
    print("3. 查看文档: cat README_AI_AGENT.md")
    
    print("\n常用命令:")
    if os.name == 'nt':  # Windows
        print("  激活虚拟环境: .venv\\Scripts\\activate")
        print("  运行程序: .venv\\Scripts\\python your_script.py")
    else:  # Unix/Linux/Mac
        print("  激活虚拟环境: source .venv/bin/activate")
        print("  运行程序: .venv/bin/python your_script.py")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
