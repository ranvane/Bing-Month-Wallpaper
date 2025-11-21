import json
import os
import requests
from datetime import datetime, timedelta

DATA_PATH = "data/wallpapers.json"

# Bing API：最近 8 天，idx=0 为今天
API_URL = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&pid=hp"

def fetch_today():
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    data = r.json()

    img = data["images"][0]
    date_str = img["startdate"]  # YYYYMMDD

    date_fmt = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    ohr_url = "https://www.bing.com" + img["url"]

    # 恢复 title 和 copyright 字段
    wallpaper_info = {
        "date": date_fmt,
        "title": img.get("title", ""),
        "copyright": img.get("copyright", ""),
        "image_url": "https://www.bing.com" + img.get("urlbase", "") + "_UHD.jpg"
        # 注意：移除 ohr_url 和 download_url 字段
    }
    return wallpaper_info

def load_db():
    if not os.path.exists(DATA_PATH):
        return {}  # 空字典
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        return data
    else:
        # 自动修复成空 dict
        return {}


def save_db(db):
    # 按日期从近到远排序
    # 使用 sorted 函数对字典按键（日期）进行排序，reverse=True 表示降序
    sorted_items = sorted(db.items(), key=lambda x: x[0], reverse=True)
    sorted_db = dict(sorted_items)
    
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted_db, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    db = load_db()
    today_data = fetch_today()
    db[today_data["date"]] = today_data
    save_db(db)
    print(f"Fetched: {today_data['date']}")
