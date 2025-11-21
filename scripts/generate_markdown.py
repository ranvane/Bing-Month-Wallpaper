import json
import os
from pathlib import Path
from collections import defaultdict
import datetime

DB = "data/wallpapers.json"
CONTENT_DIR = "content"

# 每行显示的月份数量（首页）
months_per_row = 6

# 月页面每行显示图片数量
images_per_row = 3


def ensure_dir(path):
    """
    确保目录存在，如果不存在则创建
    
    参数:
        path (str): 需要创建的目录路径
        
    功能:
        - 使用Path对象的mkdir方法创建目录
        - parents=True表示如果父目录不存在也会一并创建
        - exist_ok=True表示如果目录已存在不会抛出异常
        
    使用场景:
        在创建文件前确保目标目录存在，避免因目录不存在而导致的文件创建失败
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def generate_month_page(year, month, items):
    """生成某年某月的壁纸展示页面"""
    # 修改路径格式为：2025-11/2025-11.html
    dir_path = f"{CONTENT_DIR}/{year}-{month}"
    file_path = f"{dir_path}/{year}-{month}.html"
    ensure_dir(dir_path)
    
    # 生成HTML内容
    lines = [
        '<!DOCTYPE html>',
        '<html lang="zh-CN">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'    <title>{year}-{month} 壁纸合集</title>',
        '    <style>',
        '        body { font-family: Arial, sans-serif; margin: 20px; }',
        '        h1, p { text-align: center; }',
        '        table { margin: 0 auto; border-collapse: collapse; }',
        '        td { padding: 10px; text-align: center; }',
        '        img { max-width: 300px; height: auto; }',
        '        .footer { text-align: center; margin-top: 30px; }',
        '    </style>',
        '</head>',
        '<body>',
        f'    <h1>{year}-{month} 壁纸合集</h1>',
        f'    <p>共收录 {len(items)} 张壁纸</p>',
        '    <hr>',
    ]

    # 按日期倒序排列
    sorted_dates = sorted(items.keys(), reverse=True)

    # 逐行生成图片表格
    for i in range(0, len(sorted_dates), images_per_row):
        row_dates = sorted_dates[i:i + images_per_row]

        lines.append('    <table><tr>')

        for date in row_dates:
            item = items[date]
            img_url = item["image_url"]

            lines.append('        <td>')
            lines.append(f'            <a href="{img_url}" target="_blank">')
            lines.append(f'            <img src="{img_url}" alt="{date} {item["title"]}" />')
            lines.append('            </a><br>')
            lines.append(f'            <a href="{img_url}" target="_blank">{date}</a>')
            lines.append(' &nbsp; ')
            lines.append(f'            <a href="{img_url}" target="_blank">下载</a>')
            lines.append('        </td>')

        lines.append('    </tr></table>\n')

    # 页脚
    lines.extend([
        '    <hr>',
        '    <div class="footer">',
        f'        <p>最后更新: {datetime.datetime.now().strftime("%Y-%m-%d")}</p>',
        '        <p>数据来源: Microsoft Bing 壁纸</p>',
        '    </div>',
        '</body>',
        '</html>',
        ""
    ])

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))



def generate_index(all_months, db):
    # 按年份分组月份
    year_months = defaultdict(list)
    for ym in sorted(all_months, reverse=True):
        year, month = ym.split("-")
        year_months[year].append(month)
    
    # 生成HTML内容
    lines = [
        '<!DOCTYPE html>',
        '<html lang="zh-CN">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '    <title>Bing 壁纸目录</title>',
        '    <style>',
        '        body { font-family: Arial, sans-serif; margin: 20px; }',
        '        h1, h2, p { text-align: center; }',
        '        .links { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; }',
        '        .link-item { margin: 5px; }',
        '        .footer { text-align: center; margin-top: 30px; }',
        '    </style>',
        '</head>',
        '<body>',
        '    <h1>📅Bing 壁纸目录</h1>',
        '    <p>每日更新的精美壁纸，记录时光的印记</p>',
        f'    <p>共收录 {len(db)} 张壁纸，跨越 {len(year_months)} 年</p>',
        '    <hr>',
    ]
    
    # 添加年份分组
    for year in sorted(year_months.keys(), reverse=True):
        lines.append(f'    <h2>{year}</h2>')
        lines.append('    <div class="links">')
        
        # 对月份进行排序
        months = sorted(year_months[year], reverse=True)
        
        # 生成月份链接
        for month in months:
            ym = f"{year}-{month}"
            lines.append(f'        <div class="link-item"><a href="{ym}/{ym}.html">{ym}</a></div>')
        
        lines.append('    </div>\n')
    
    # 添加页脚
    lines.extend([
        '    <hr>',
        '    <div class="footer">',
        f'        <p>最后更新: {datetime.datetime.now().strftime("%Y-%m-%d")}</p>',
        '        <p>数据来源: Microsoft Bing 壁纸</p>',
        '    </div>',
        '</body>',
        '</html>',
        ""
    ])
    
    with open(f"{CONTENT_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    with open(DB, "r", encoding="utf-8") as f:
        db = json.load(f)

    months = {}

    # 聚合日期 → 年月
    for date_str, item in db.items():
        ym = date_str[:7]  # YYYY-MM
        months.setdefault(ym, {})
        months[ym][date_str] = item

    # 生成月页面
    for ym, entries in months.items():
        year, month = ym.split("-")
        generate_month_page(year, month, entries)

    # 生成首页
    generate_index(months.keys(), db)

    print("HTML pages generated.")