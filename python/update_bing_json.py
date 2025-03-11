import json
import logging
import os
from typing import Dict, List
from json_utils import count_items_in_json_variable
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-5s | %(filename)s | %(funcName)s | %(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 获取项目基础目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取Bing壁纸数据目录
bing_dir = os.path.join(base_dir, "bing")

# 支持的语言列表（ROW为通用地区）
LANGS = ['ROW', 'en-US', 'en-CA', 'en-GB', 'en-IN', 'es-ES',
         'fr-FR', 'fr-CA', 'it-IT', 'ja-JP', 'pt-BR', 'de-DE', 'zh-CN']
LANGS = ['ROW']


def fetch_bing_data(lang: str, days: int = 1) -> List[Dict]:
    """
    获取指定天数的Bing壁纸数据
    参数:
        lang: 语言代码
        days: 获取天数（默认当天）
    返回:
        包含壁纸信息的字典列表
    """
    # 计算API参数（idx=0表示当天，n=days表示获取天数）
    api_url = f"https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n={days}&mkt={lang}"

    # 添加浏览器级User-Agent避免被拒绝
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    try:
        logging.info(f"fetch_bing_data:获取{lang}  {days}天数据:")
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()  # 触发HTTP错误异常
        # 数据清洗和格式标准化
        return [{
            "fullstartdate": img.get("fullstartdate"),
            "date": img.get("startdate"),
            "url": f'https://www.bing.com{img.get("url")}',
            "urlbase": f'https://www.bing.com{img.get("urlbase")}',
            "copyright": img.get("copyright"),
            "copyrightKeyword": img.get("copyrightLink").split("=")[-1] if img.get("copyrightLink") else "",
            "hsh": img.get("hsh") or img.get("urlbase", "").split("_")[-1],  # 兼容两种不同API版本
            "description": img.get("desc" if lang.startswith("zh") else "copyright")
        } for img in response.json()['images']]
    except Exception as e:
        logging.error(f"获取{lang}数据失败: {str(e)}")
        return []


def merge_images(existing: List[Dict], new: List[Dict], key_fields: List[str] = ['fullstartdate']) -> List[Dict]:
    """
    合并新旧壁纸数据（避免重复）
    参数:
        existing: 现有数据列表
        new: 新获取的数据列表
        key_fields: 用于判重的字段列表
    返回:
        合并后的新数据列表（按日期倒序）
    """
    # 使用集合快速查找已存在的键值组合
    existing_keys = {tuple(img[key] for key in key_fields if key in img) for img in existing}

    # 添加新数据中不重复的条目
    for img in new:
        new_key = tuple(img.get(key) for key in key_fields)
        if new_key not in existing_keys:
            existing.append(img)
            existing_keys.add(new_key)

    # 按日期倒序排列（最新在前）
    return sorted(existing,
                  key=lambda x: x.get('startdate', '00000000'),
                  reverse=True)


def save_monthly_data(lang: str, data: List[Dict]):
    """
    按年月分类保存数据到对应文件夹
    参数:
        lang: 语言代码
        data: 合并后的完整数据列表
    """
    for img in data:
        # 解析日期（格式示例：202402030700 -> 2024-02）
        date_str = img.get('fullstartdate', '')
        if len(date_str) >= 6:
            year_month = f"{date_str[:4]}-{date_str[4:6]}"

            # 创建年月文件夹
            dir_path = os.path.join(bing_dir, year_month)
            os.makedirs(dir_path, exist_ok=True)

            # 构建文件路径
            file_path = os.path.join(bing_dir, f"bing_{lang}.json")

            # 读取已有数据（如果存在）
            existing = []
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing = json.load(f)

            # 合并数据并保存

            merged = merge_images(existing, [img], key_fields=['hsh', 'copyrightKeyword'])
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(merged, f, ensure_ascii=False, indent=4)


def update_lang_data(lang: str, days: int = 1):
    """
    更新指定语言的完整数据
    参数:
        lang: 语言代码
        days：要获取的最近天数的数据，默认1天
    """
    # 根目录文件路径
    root_file = os.path.join(bing_dir, f"bing_{lang}.json")

    # 读取已有数据
    existing_data = []
    if os.path.exists(root_file):
        try:
            with open(root_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"解析 {root_file} 时发生JSON解码错误: {e}")
            return


    # 获取最新数据时传入days参数
    logging.info(f"获取 {lang} 的{days}天最新数据")
    new_data = fetch_bing_data(lang, days)
    if not new_data:
        return

    # 合并数据

    merged_data = merge_images(existing_data, new_data)
    # logging.info(f"合并 {existing_data} 的 {len(new_data)} 数据完成")

    logging.info(
        f"\n原有 {count_items_in_json_variable(existing_data)}条数据，新获得 {count_items_in_json_variable(new_data)}条数据,合并后 {count_items_in_json_variable(merged_data)}条数据")
    # 保存根文件
    # logging.info(f"保存合并 {lang} 的 {days} 天数据到{root_file}")
    try:
        with open(root_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"保存 {root_file} 时发生错误: {e}")
        return

    # 按年月分类保存
    save_monthly_data(lang, merged_data)
    logging.info(f"{lang} 数据更新完成")


if __name__ == "__main__":
    for lang in LANGS:
        update_lang_data(lang, 7)
    logging.info("所有语言数据更新完成")
