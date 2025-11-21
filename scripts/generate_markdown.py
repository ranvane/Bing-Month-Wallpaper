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
    Path(path).mkdir(parents=True, exist_ok=True)


def generate_month_page(year, month, items):
    """生成某年某月的壁纸展示页面"""
    # 修改路径格式为：2025-11/2025-11.md
    dir_path = f"{CONTENT_DIR}/{year}-{month}"
    file_path = f"{dir_path}/{year}-{month}.md"
    ensure_dir(dir_path)

    lines = [
        f'# <p align="center">{year}-{month} 壁纸合集</p>',
        f'<p align="center">共收录 {len(items)} 张壁纸</p>',
        "\n",
        "---",
    ]

    # 按日期倒序排列
    sorted_dates = sorted(items.keys(), reverse=True)

    # 逐行生成图片表格，使用 align="center" 实现真正居中
    for i in range(0, len(sorted_dates), images_per_row):
        row_dates = sorted_dates[i:i + images_per_row]

        # 核心：使用 align="center"
        lines.append('<table align="center" style="border-collapse: collapse; text-align:center;"><tr>')

        for date in row_dates:
            item = items[date]
            img_url = item["image_url"]

            lines.append('<td style="padding: 10px;">')
            lines.append(f'<a href="{img_url}" target="_blank">')
            lines.append(f'<img src="{img_url}" alt="{date} {item["title"]}" width="300"/>')
            lines.append('</a><br>')
            lines.append(f'<a href="{img_url}" target="_blank">{date}</a>')
            lines.append(' &nbsp; ')
            lines.append(f'<a href="{img_url}" target="_blank">下载</a>')
            lines.append('</td>')

        # 空列补齐，使表格整齐
        # if len(row_dates) < images_per_row:
        #     for _ in range(images_per_row - len(row_dates)):
        #         lines.append('<td style="padding: 10px;"></td>')

        lines.append('</tr></table>\n')

    # 页脚
    lines.extend([
        "---",
        f'<p align="center">最后更新: {datetime.datetime.now().strftime("%Y-%m-%d")}</p>',
        '<p align="center">数据来源: Microsoft Bing 壁纸</p>',
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
    
    lines = [
        '# <p align="center">📅Bing 壁纸目录</p>\n',
        '> <p align="center">每日更新的精美壁纸，记录时光的印记</p>\n',
        f'<p align="center">共收录 {len(db)} 张壁纸，跨越 {len(year_months)} 年</p>\n',
        "\n",
        "---",
        
    ]
    
    # 添加年份分组
    for year in sorted(year_months.keys(), reverse=True):
        lines.append(f'## <p align="center">{year}</p>\n')
        
        # 对月份进行排序
        months = sorted(year_months[year], reverse=True)
        
        # 按行生成markdown链接
        for i in range(0, len(months), months_per_row):
            row_months = months[i:i + months_per_row]
            
            # 创建链接行 - 修改链接格式为：2025-11/2025-11.md
            link_parts = []
            for month in row_months:
                ym = f"{year}-{month}"
                link_parts.append(f"[{ym}]({ym}/{ym}.md)")
            
            # 使用HTML居中标签包裹链接行，但将markdown链接放在HTML标签外
            lines.append('<center>\n')
            lines.append(' | '.join(link_parts) + '\n')
            lines.append('</center>\n')
        
        lines.append("")  # 添加空行
    
    # 添加页脚
    lines.extend([
        "---\n",
        '<center>\n',
        '*最后更新: ' + datetime.datetime.now().strftime("%Y-%m-%d") + '*\n',
        '*数据来源: Microsoft Bing 壁纸*\n',
        '</center>\n'
    ])
    
    with open(f"{CONTENT_DIR}/index.md", "w", encoding="utf-8") as f:
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

    print("Markdown pages generated.")