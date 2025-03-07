from pathlib import Path
from datetime import datetime
import json
from collections import defaultdict
from typing import List, Dict
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-5s | %(filename)s | %(funcName)s:%(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# 支持的语言列表（ROW为通用地区）
LANGS = [
    'ROW', 'en-US', 'en-CA', 'en-GB', 'en-IN', 'es-ES',
    'fr-FR', 'fr-CA', 'it-IT', 'ja-JP', 'pt-BR', 'de-DE', 'zh-CN'
]


def process_bing_json(file_path: Path, copy_index: bool = False) -> None:
    """处理单个Bing壁纸JSON文件，按年月分类存储"""
    # 异常处理：读取JSON文件（文件不存在/格式错误时捕获异常）
    try:
        data = json.loads(file_path.read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.info(f"Error reading {file_path}: {e}")
        return

    # 获取文件名（不含扩展名）
    base_name = file_path.stem

    # 使用 defaultdict 自动初始化空列表，简化数据分组
    sorted_data = defaultdict(list)

    # 遍历数据项，按年月分组
    for item in data:
        if 'fullstartdate' in item:
            try:
                # 解析日期并格式化为YYYY-MM
                date = datetime.strptime(item['fullstartdate'], '%Y%m%d%H%M')
                sorted_data[date.strftime('%Y-%m')].append(item)
            except ValueError as e:
                logging.info(f"Invalid date format in {file_path}: {e}")

    # 写入分组后的文件
    for year_month, items in sorted_data.items():
        # 创建年月目录（自动创建父目录）
        output_dir = file_path.parent / year_month
        output_dir.mkdir(parents=True, exist_ok=True)

        # 写入语言专属文件（如 bing_zh-CN.json）
        lang_file = output_dir / f"{base_name}.json"
        lang_file.write_text(json.dumps(items, ensure_ascii=False, indent=4))

        # 选择性写入当月索引文件（如 2023-10.json）
        if copy_index:
            index_file = output_dir / f"{year_month}.json"
            index_file.write_text(json.dumps(items, ensure_ascii=False, indent=4))

        logging.info(f"Created: {lang_file}")


def year_month_langs(lang: str = 'zh-CN') -> None:
    """
    处理指定语言的JSON文件
    将所有的json文件生成:"年月文件夹/bing_地区.json"的文件
    """
    # 获取项目根目录（python文件夹的父级）
    base_dir = Path(__file__).parent.parent

    # 构建Bing数据目录路径
    bing_dir = base_dir / "bing"

    # 遍历所有支持的语言
    for lang_code in LANGS:
        # 构建完整的JSON文件路径
        json_file = bing_dir / f"bing_{lang_code}.json"

        # 检查文件是否存在
        if not json_file.exists():
            logging.info(f"File not found: {json_file.name}")
            continue  # 跳过不存在的文件

        # 处理当前语言文件
        logging.info(f"Processing: {json_file.name}")
        # 调用处理函数，仅当当前语言等于目标语言时创建索引文件
        process_bing_json(json_file, copy_index=(lang_code == lang))


if __name__ == "__main__":
    year_month_langs()
