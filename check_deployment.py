#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署前最终检查脚本
"""
import os
import json
from datetime import datetime

def check_files():
    """检查关键文件是否存在"""
    print("=" * 70)
    print("文件检查")
    print("=" * 70)

    critical_files = [
        "index.html",
        "majors.html",
        "login.html",
        "register.html",
        "js/auth.js",
        "js/payments.js",
        "js/reports.js",
        "css/common.css",
        "user/dashboard.html",
        "user/reports.html",
        "user/orders.html",
        "user/purchase.html",
        "admin/users.html",
        "admin/reports.html",
    ]

    all_ok = True
    for f in critical_files:
        if os.path.exists(f):
            print(f"✅ {f}")
        else:
            print(f"❌ {f}")
            all_ok = False

    return all_ok

def check_reports():
    """检查深度报告"""
    print("\n" + "=" * 70)
    print("深度报告检查")
    print("=" * 70)

    reports_dir = "data/reports"
    if not os.path.exists(reports_dir):
        print("❌ data/reports 目录不存在")
        return False

    files = os.listdir(reports_dir)
    html_files = [f for f in files if f.endswith(".html") and f != "index.html"]
    pdf_files = [f for f in files if f.endswith(".pdf")]
    txt_files = [f for f in files if f.endswith(".txt")]

    print(f"✅ HTML报告: {len(html_files)} 个")
    print(f"✅ PDF报告: {len(pdf_files)} 个")
    print(f"✅ TXT报告: {len(txt_files)} 个")
    print(f"✅ 索引页面: {'index.html' in files}")

    if len(html_files) >= 15:
        return True
    else:
        print("⚠️ 警告: HTML报告少于15个")
        return False

def check_git_status():
    """检查Git状态"""
    print("\n" + "=" * 70)
    print("Git状态检查")
    print("=" * 70)

    try:
        import subprocess
        status = subprocess.check_output(["git", "status", "--porcelain"], text=True)
        if status.strip() == "":
            print("✅ 工作树干净，所有更改已提交")
            return True
        else:
            print("⚠️ 有未提交的更改:")
            print(status)
            return False
    except Exception as e:
        print(f"❌ Git检查失败: {e}")
        return False

def check_local_server():
    """检查本地服务器"""
    print("\n" + "=" * 70)
    print("本地服务器检查")
    print("=" * 70)

    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:3456/")
        response = urllib.request.urlopen(req, timeout=5)
        if response.status == 200:
            print(f"✅ 本地服务器运行中 (端口3456, HTTP {response.status})")
            print("   访问地址: http://localhost:3456")
            return True
        else:
            print(f"❌ 本地服务器响应异常 (HTTP {response.status})")
            return False
    except Exception as e:
        print(f"❌ 本地服务器未运行或无法访问: {e}")
        print("   请运行: python3 -m http.server 3456")
        return False

def generate_summary():
    """生成部署总结"""
    print("\n" + "=" * 70)
    print("部署准备总结")
    print("=" * 70)
    print()

    print("📦 项目名称: 专业星图")
    print("📅 准备时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🌐 部署方案: GitHub Pages + Supabase")
    print()

    print("✅ 已完成:")
    print("  - 611个专业数据导入")
    print("  - 15个专业深度分析报告")
    print("  - 用户认证系统")
    print("  - 支付点数系统")
    print("  - 管理后台")
    print("  - 响应式设计")
    print()

    print("🚀 下一步:")
    print("  1. 配置GitHub仓库")
    print("  2. 启用GitHub Pages")
    print("  3. 部署上线")
    print("  4. 线上测试验证")
    print()

def main():
    print("\n" + "=" * 70)
    print("专业星图 - 部署前最终检查")
    print("=" * 70)
    print()

    checks = [
        ("关键文件", check_files()),
        ("深度报告", check_reports()),
        ("Git状态", check_git_status()),
        ("本地服务器", check_local_server()),
    ]

    print()
    print("=" * 70)
    print("检查结果汇总")
    print("=" * 70)
    print()

    passed = 0
    for name, result in checks:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
        if result:
            passed += 1

    print()
    if passed == len(checks):
        print("🎉 所有检查通过！可以开始部署。")
    else:
        print(f"⚠️ {passed}/{len(checks)} 通过，请解决失败项后再部署。")

    generate_summary()

if __name__ == '__main__':
    main()
