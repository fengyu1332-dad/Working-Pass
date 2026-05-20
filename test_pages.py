from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("=" * 60)
    print("测试首页 - http://localhost:8000")
    print("=" * 60)
    
    page.goto('http://localhost:8000')
    page.wait_for_load_state('networkidle')
    
    title = page.title()
    print(f"页面标题: {title}")
    
    login_btn = page.locator('text=登录 / 注册')
    if login_btn.count() > 0:
        print("✅ 登录按钮存在")
    else:
        print("❌ 登录按钮不存在")
    
    major_cards = page.locator('.major-card')
    card_count = major_cards.count()
    print(f"专业卡片数量: {card_count}")
    
    if card_count > 0:
        first_card_name = major_cards.first().locator('.major-name').text_content()
        print(f"第一个专业: {first_card_name}")
    
    page.screenshot(path='/tmp/homepage.png', full_page=True)
    print("截图已保存: /tmp/homepage.png")
    
    print("\n" + "=" * 60)
    print("测试登录页 - http://localhost:8000/login.html")
    print("=" * 60)
    
    page.goto('http://localhost:8000/login.html')
    page.wait_for_load_state('networkidle')
    
    print(f"页面标题: {page.title()}")
    
    phone_tab = page.locator('text=手机号登录')
    email_tab = page.locator('text=邮箱登录')
    if phone_tab.count() > 0 and email_tab.count() > 0:
        print("✅ 手机号/邮箱切换标签存在")
    
    page.screenshot(path='/tmp/login.png')
    
    print("\n" + "=" * 60)
    print("测试用户仪表板 - http://localhost:8000/user/dashboard.html")
    print("=" * 60)
    
    page.goto('http://localhost:8000/user/dashboard.html')
    page.wait_for_load_state('networkidle')
    
    print(f"页面标题: {page.title()}")
    
    points_display = page.locator('.points-value')
    if points_display.count() > 0:
        print(f"✅ 点数显示存在: {points_display.text_content()}")
    
    package_cards = page.locator('.package-card')
    print(f"套餐卡片数量: {package_cards.count()}")
    
    page.screenshot(path='/tmp/dashboard.png', full_page=True)
    
    browser.close()
    print("\n测试完成!")
