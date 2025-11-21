import json
import os

def convert_date_format(date_str):
    """将YYYYMMDD格式转换为YYYY-MM-DD格式"""
    year = date_str[:4]
    month = date_str[4:6]
    day = date_str[6:8]
    return f"{year}-{month}-{day}"

def main():
    # 读取data.json
    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 转换为wallpapers.json格式
    wallpapers = {}
    
    for item in data:
        # 转换日期格式
        date = convert_date_format(item["startdate"])
        
        # 构建图片URL
        image_url = f"https://www.bing.com{item['urlbase']}_UHD.jpg"
        
        # 添加到wallpapers字典
        wallpapers[date] = {
            "date": date,
            "title": item["title"],
            "copyright": item["copyright"],
            "image_url": image_url
        }
    
    # 按日期降序排列（从最新到最旧）
    sorted_wallpapers = dict(sorted(wallpapers.items(), key=lambda x: x[0], reverse=True))
    
    # 写入wallpapers.json
    with open("data/wallpapers.json", "w", encoding="utf-8") as f:
        json.dump(sorted_wallpapers, f, ensure_ascii=False, indent=2)
    
    print(f"转换完成，共处理 {len(sorted_wallpapers)} 条记录")

if __name__ == "__main__":
    main()