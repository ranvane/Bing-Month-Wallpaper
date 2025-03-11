from pathlib import Path
from datetime import datetime
import json
from collections import defaultdict
import logging
import shutil


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


def process_bing_json(file_path: Path, copy_lang:str) -> None:
    """
    处理单个Bing壁纸JSON文件，按年月分类存储

    :param file_path: 要处理的JSON文件的路径
    :param copy_lang: 是否复制索引文件的标志，默认为zh-CN
    处理流程：
    遍历按年月分组的数据。
    为每个年月创建一个目录，目录名为 YYYY-MM，如果父目录不存在则自动创建。
    生成语言专属文件的路径，文件名格式为 {base_name}.json。
    将分组后的数据以JSON格式写入文件，使用 ensure_ascii=False 确保非ASCII字符正确显示，indent=4 使JSON文件具有良好的可读性。
    记录创建的文件信息
    """
    # 异常处理：读取JSON文件（文件不存在/格式错误时捕获异常）
    try:
        # 以UTF-8编码读取文件内容，并将其解析为JSON格式
        data = json.loads(file_path.read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # 若读取文件或解析JSON时出现错误，记录日志并返回
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
                # 将 'fullstartdate' 字段的值解析为datetime对象
                date = datetime.strptime(item['fullstartdate'], '%Y%m%d%H%M')
                # 按年月分组，将数据项添加到对应的年月列表中
                sorted_data[date.strftime('%Y-%m')].append(item)
            except ValueError as e:
                # 若日期格式无效，记录日志
                logging.info(f"Invalid date format in {file_path}: {e}")

    # 写入分组后的文件
    for year_month, items in sorted_data.items():
        # 创建年月目录（自动创建父目录）
        output_dir = file_path.parent / year_month
        # 创建年月目录，若父目录不存在则自动创建
        output_dir.mkdir(parents=True, exist_ok=True)

        # 写入语言专属文件（如 bing_zh-CN.json）
        lang_file = output_dir / f"{base_name}.json"
        # 将分组后的数据写入语言专属文件
        lang_file.write_text(json.dumps(items, ensure_ascii=False, indent=4))

        # 记录创建的文件信息
        logging.info(f"Created: {lang_file}")

def create_monthly_index_files(copy_lang: str = 'zh-CN') -> None:
    """
    处理流程：
    首先遍历 bing 目录下的所有年月文件夹。
    对于每个年月文件夹，查找是否存在命名符合 copy_lang 的 JSON 文件。
    如果没有找到符合 copy_lang 的文件，则查找命名为 bing_en-US.json 的文件。
    若找到匹配的文件，则将其复制为当月索引文件。
    """
    base_dir = Path(__file__).parent.parent
    bing_dir = base_dir / "bing"

    for year_month_folder in bing_dir.iterdir():
        if year_month_folder.is_dir() and year_month_folder.name.count('-') == 1 and len(year_month_folder.name.split('-')[0]) == 4 and len(year_month_folder.name.split('-')[1]) == 2:
            match_files = list(year_month_folder.glob(f"bing_{copy_lang}.json"))
            if not match_files:
                # 如果没有符合 copy_lang 的文件，使用 en-US
                match_files = list(year_month_folder.glob("bing_en-US.json"))
            for json_file in match_files:
                index_file = year_month_folder / f"{year_month_folder.name}.json"
                shutil.copy2(json_file, index_file)
                logging.info(f"Created index file: {index_file}")

def year_month_langs(copy_lang: str = 'zh-CN') -> None:
    """
    处理指定语言的JSON文件
    将所有的json文件生成:"年月文件夹/bing_地区.json"的文件
    :param copy_lang: 复制为当月索引文件（如 2023-10.json）的语言代码，默认为 'zh-CN'

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
        process_bing_json(json_file,copy_lang)

    create_monthly_index_files(copy_lang)


if __name__ == "__main__":
    year_month_langs()
