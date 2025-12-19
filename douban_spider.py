import requests
from bs4 import BeautifulSoup
import pandas as pd

print("🎬 开始爬取豆瓣电影Top250...")
print("=" * 50)

# 1. 目标网址
url = 'https://movie.douban.com/top250'

# 2. 模拟浏览器访问（很重要！）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 3. 发送请求
response = requests.get(url, headers=headers)
print(f"📡 网页请求状态码: {response.status_code}")

# 4. 检查是否成功
if response.status_code == 200:
    print("✅ 网页获取成功，开始解析数据...")

    # 5. 解析网页
    soup = BeautifulSoup(response.text, 'html.parser')

    # 6. 查找所有电影项目
    movie_list = []

    # 查找每个电影项目
    for item in soup.find_all('div', class_='item'):
        # 获取电影标题
        title_tag = item.find('span', class_='title')
        movie_title = title_tag.text if title_tag else '未知电影'

        # 获取评分
        rating_tag = item.find('span', class_='rating_num')
        movie_rating = rating_tag.text if rating_tag else '0.0'

        # 添加到列表
        movie_list.append([movie_title, movie_rating])

    print(f"📊 共找到 {len(movie_list)} 部电影")

    # 7. 保存到Excel
    df = pd.DataFrame(movie_list, columns=['电影名称', '评分'])
    df.to_excel('豆瓣电影Top250.xlsx', index=False, engine='openpyxl')

    print("✅ 数据保存成功！")
    print("📁 文件已保存为: 豆瓣电影Top250.xlsx")
    print("=" * 50)

    # 8. 显示前10部电影预览
    print("🎥 前10部电影预览:")
    print("-" * 40)
    for i, (title, rating) in enumerate(movie_list[:10], 1):
        print(f"{i:2d}. {title:20} - 评分: {rating}")

else:
    print(f"❌ 请求失败，状态码: {response.status_code}")
    print("💡 提示: 可能是网络问题或需要更新User-Agent")