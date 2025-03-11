import json

def count_items_in_json(json_file_path):
    """
    该函数用于统计JSON文件中的项数。

    参数:
    json_file_path (str): JSON文件的路径。

    返回:
    int: JSON文件中的项数。
    """
    try:
        # 打开JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            # 加载JSON数据
            data = json.load(file)
            # 如果数据是列表，返回列表的长度
            if isinstance(data, list):
                return len(data)
            else:
                print("JSON数据不是一个列表。")
                return 0
    except FileNotFoundError:
        print(f"文件 {json_file_path} 未找到。")
        return 0
    except json.JSONDecodeError:
        print(f"无法解析 {json_file_path} 中的JSON数据。")
        return 0

# 示例调用
json_file_path = '/home/ranvane/WorkSpace/Bing-Month-Wallpaper/bing/bing_en-GB.json'
item_count = count_items_in_json(json_file_path)
print(f"JSON文件中的项数: {item_count}")
