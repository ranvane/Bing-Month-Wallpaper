import json
import logging
import os
import re
from string import Template
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-5s | %(filename)s | %(funcName)s | %(lineno)d | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 获取项目基础目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取Bing壁纸数据目录
bing_dir = os.path.join(base_dir, "bing")


# 封装文件读取函数
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logging.info(f"Error: File {file_path} not found.")
        return None
    except Exception as e:
        logging.info(f"Error reading {file_path}: {e}")
        return None


# 封装文件写入函数
def write_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"File {file_path} written successfully.")
    except Exception as e:
        logging.info(f"Error writing {file_path}: {e}")


def generate_md_file(json_file_path, template_path, output_file_path):
    """
    根据JSON文件和模板生成Markdown文件

    主要处理流程：
    1. 读取并校验输入文件
    2. 构建图片展示表格
    3. 填充模板内容
    4. 输出最终Markdown文件
    """
    # 打印处理日志头
    # logging.info('*****************************************')
    # logging.info(f"Processing: {json_file_path}")
    # logging.info(f"Template: {template_path}")
    # logging.info(f"Output: {output_file_path}")
    # logging.info('-----------------------------------------')

    # 读取JSON数据（包含错误处理）
    json_content = read_file(json_file_path)
    if json_content is None:
        return
    data = json.loads(json_content)  # 反序列化JSON内容

    # 加载Markdown模板
    template_content = read_file(template_path)
    if template_content is None:
        return
    template = Template(template_content)  # 创建字符串模板

    # 获取全站归档目录链接
    archive_table = get_year_month_links(bing_dir)

    # 构建图片表格内容
    table_rows = []
    current_row = []
    for item in data:
        # 生成不同分辨率的图片URL：
        # _1920x1080.jpg 为全高清版本
        # _UHD.jpg 为4K超清版本
        url = f"{item.get('urlbase', '')}_1920x1080.jpg"
        url_4k = f"{item.get('urlbase', '')}_UHD.jpg"

        # 提取日期字段（格式示例：20240305）
        date = item.get('date', '')

        # 创建Markdown单元格（图片显示 + 日期 + 4K下载链接）
        cell = f"![]({url}) {date} [download 4k]({url_4k})"
        current_row.append(cell)

        # 每满3个单元格生成表格行
        if len(current_row) == 3:
            row = f"| {current_row[0]} | {current_row[1]} | {current_row[2]} |"
            table_rows.append(row)
            current_row = []  # 重置行缓存

    # 补全最后未满3个的单元格
    if current_row:
        while len(current_row) < 3:
            current_row.append('')  # 空单元格占位
        row = f"| {current_row[0]} | {current_row[1]} | {current_row[2]} |"
        table_rows.append(row)

    # 从输出路径中提取年月信息（如从 "bing/2023-10/2023-10.md" 中提取 "2023-10"）
    year_month = os.path.basename(os.path.dirname(output_file_path))

    # 模板变量替换：
    # year_month - 当前年月标识
    # image_table - 图片表格内容
    # archive_table - 全站归档目录
    md_content = template.safe_substitute(
        year_month=year_month,
        image_table='\n'.join(table_rows),
        archive_table=archive_table
    )

    # 写入生成结果
    write_file(output_file_path, md_content)


def process_year_month_folder(folder_path, template_path):
    """
    处理指定的年月文件夹，为其中的JSON文件生成对应的Markdown文件

    参数:
    folder_path (str): 年月文件夹的路径
    template_path (str): Markdown模板文件的路径
    """
    # 获取年月标识（如"2023-10"）
    year_month = os.path.basename(folder_path)

    # 遍历文件夹内所有文件
    for filename in os.listdir(folder_path):
        # 仅处理JSON格式文件
        if filename.endswith('.json'):
            json_file_path = os.path.join(folder_path, filename)

            # 生成对应Markdown文件名规则：
            # 1. 当月总览文件（如2023-10.json -> 2023-10.md）
            # 2. 语言文件（如bing_zh-CN.json -> 2023-10_bing_zh-CN.md）
            if filename == f"{year_month}.json":
                md_file_name = f"{year_month}.md"
            elif filename.startswith('bing'):
                # 去除.json扩展名后拼接年月
                md_file_name = f"{year_month}_{filename[:-5]}.md"
            else:
                continue  # 跳过非标准命名文件

            # 构建完整输出路径
            md_file_path = os.path.join(folder_path, md_file_name)

            # 调用核心生成函数（参数顺序：输入文件，模板文件，输出文件）
            generate_md_file(json_file_path, template_path, md_file_path)


def process_index_template_folder():
    """
    处理Bing根目录下的所有年月文件夹

    功能流程：
    1. 定位索引模板文件
    2. 筛选符合YYYY-MM格式的年月文件夹
    3. 为每个有效文件夹生成Markdown文件
    """
    # 定位模板文件路径（bing/index_template.md）
    index_template_path = os.path.join(bing_dir, "index_template.md")

    # 模板文件存在性校验
    if not os.path.exists(index_template_path):
        logging.info(f"Error: Template file {index_template_path} not found.")
        return

    # 创建正则匹配器（匹配YYYY-MM格式的文件夹名）
    year_month_pattern = re.compile(r'\d{4}-\d{2}')  # 例：2023-10

    # 遍历Bing根目录下的所有条目
    for item in os.listdir(bing_dir):
        item_path = os.path.join(bing_dir, item)

        # 双重验证：1. 是目录 2. 名称符合年月格式
        if os.path.isdir(item_path) and year_month_pattern.match(item):
            # 调用年月文件夹处理流程（参数：文件夹路径，模板路径）
            process_year_month_folder(item_path, index_template_path)


def get_year_month_links(bing_dir, nums=10):
    """
    生成按年月分组的Markdown超链接表格

    参数:
    bing_dir (str): 包含年月文件夹的根目录
    nums (int): 控制每行显示链接数量（默认10个/行）
    """
    # 筛选并排序年月文件夹（格式：YYYY-MM）
    year_month_folders = sorted(
        [f for f in os.listdir(bing_dir)
         if os.path.isdir(os.path.join(bing_dir, f)) and re.match(r'\d{4}-\d{2}', f)],
        reverse=True  # 按时间倒序排列（最新在前）
    )

    links = []
    for i, folder in enumerate(year_month_folders, 1):
        # 检查目标md文件是否存在（如2023-10/2023-10.md）
        md_file = os.path.join(bing_dir, folder, f"{folder}.md")
        if os.path.exists(md_file):
            # 生成相对路径链接（格式：[2023-10](../2023-10/2023-10.md)）
            # relative_path = os.path.relpath(md_file, start=os.path.dirname(bing_dir))
            # 生成相对路径链接，设置起始路径为bing_dir
            relative_path = os.path.relpath(md_file, start=bing_dir)
            logging.info(f"Relative Path: {relative_path}")
            links.append(f"[{folder}](/{relative_path})")


            # 每满nums个链接插入换行（生成表格换行符）
            if i % nums == 0:
                links.append("\n")  # Markdown表格换行

    # 将列表转换为管道分隔的字符串
    return "|" + "|".join(links)


def generate_index_md(nums=10):
    """
    生成静态网站的首页，即Bing壁纸归档索引文件

    功能流程：
    1. 在bing目录下创建index.md
    2. 组合归档链接表格和标题内容
    3. 将内容写入目标文件

    参数:
    nums (int): 控制表格每行显示的链接数量（默认10个）
    """
    # 构建索引文件绝对路径（bing/index.md）
    index_file_path = os.path.join(bing_dir, "index.md")

    # 组合文件内容：标题 + 链接表格
    content = "# Bing Wallpaper Archive\n\n" + get_year_month_links(bing_dir, nums)

    # 调用通用文件写入函数（复用工程中的write_file实现）
    write_file(index_file_path, content)


if __name__ == "__main__":
    process_index_template_folder()
    generate_index_md()
