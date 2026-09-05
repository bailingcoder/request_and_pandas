# from playwright.sync_api import sync_playwright
# from bs4 import BeautifulSoup
#
# URL = "https://movie.douban.com/subject/1292052/"
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()
#
#     # 页面加载
#     page.goto(URL, timeout=60000)
#     page.wait_for_load_state("networkidle")
#     page.wait_for_selector("h1", timeout=10000)
#
#     html = page.content()
#     print("✅ 成功拿到完整HTML！")
#
#     soup = BeautifulSoup(html, "html.parser")
#
#     # 1. 提取标题
#     title_tag = soup.find("h1")
#     title = title_tag.text.strip() if title_tag else "未找到标题"
#
#     # 2. 提取评分
#     rating_tag = soup.find("strong", class_="rating_num")           #strong 标签, class_属性为rating_num
#     rating = rating_tag.text.strip() if rating_tag else "未找到评分"
#
#     # 3. 新的简介提取方式（适配当前豆瓣结构）
#     # 方式A：通过 class 定位简介区域
#     # 先找父容器
#     related_info_div = soup.find("div", class_="related-info")
#
#     if related_info_div:
#         # 父容器存在，再找子标签
#         intro_tag = related_info_div.find("div", class_="all")
#         if not intro_tag:
#             # 找不到完整简介，就找展开前的短简介
#             intro_tag = related_info_div.find("span", class_="short").find("span", property="v:summary")
#         intro = intro_tag.text.strip() if intro_tag else "未找到简介"
#     else:
#         intro = "未找到简介"
#
#     # 打印结果
#     print("\n📽️ 电影信息：")
#     print(f"电影名：{title}")
#     print(f"评分：{rating}")
#     print(f"简介：{intro[:300]}...")  # 打印前300字
#
#     browser.close()

from playwright.sync_api import sync_playwright

URL = "https://movie.douban.com/subject/1292052/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # 1. 访问页面，等加载完成
    page.goto(URL, timeout=60000)
    page.wait_for_load_state("networkidle",timeout=60000)

    # 2. 直接用Playwright定位所有元素，不用soup
    title = page.locator("h1").inner_text()
    rating = page.locator("strong.rating_num").inner_text()

    # 3. 定位简介区域，先点击"展开全部"
    intro_container = page.locator("div.related-info")
    expand_btn = intro_container.locator("a.a_show_full")

    # 如果按钮存在，就点击它
    if expand_btn.is_visible(timeout=2000):
        expand_btn.click()
        page.wait_for_timeout(500)  # 等简介展开

    # 4. 提取完整简介
    intro = intro_container.locator("span.all").inner_text().strip()

    # 打印结果
    print("📽️ 电影信息：")
    print(f"电影名：{title}")
    print(f"评分：{rating}")
    print(f"简介：{intro}...")

    browser.close()