import json, os

# 获取项目基础目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取Bing壁纸数据目录
bing_dir = os.path.join(base_dir, "bing")


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
                return len(data), data
            else:
                print("JSON数据不是一个列表。")
                return 0
    except FileNotFoundError:
        print(f"文件 {json_file_path} 未找到。")
        return 0
    except json.JSONDecodeError:
        print(f"无法解析 {json_file_path} 中的JSON数据。")
        return 0


def count_items_in_json_variable(json_variable):
    """
    该函数用于统计JSON变量中的项数。

    参数:
    json_variable (list): JSON变量，应为列表类型。

    返回:
    int: JSON变量中的项数。
    """
    if isinstance(json_variable, list):
        return len(json_variable)
    else:
        print("JSON变量不是一个列表。")
        return 0


def process_bing_json(bing_dir):
    """
    该函数用于处理bing文件夹下的所有JSON文件。
    参数:
    bing_dir (str): bing文件夹的路径。
    """
    # 遍历bing文件夹下的所有文件
    for filename in os.listdir(bing_dir):
        if filename.startswith('bing_') and filename.endswith('.json'):
            file_path = os.path.join(bing_dir, filename)
            try:
                # 读取JSON文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 按hsh去重
                unique_data = []
                hsh_set = set()
                for item in data:
                    hsh = item.get('hsh')
                    if hsh and hsh not in hsh_set:
                        unique_data.append(item)
                        hsh_set.add(hsh)

                # 按fullstartdate降序排列
                sorted_data = sorted(unique_data, key=lambda x: x.get('fullstartdate', '000000000000'), reverse=True)

                # 保存回原文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(sorted_data, f, ensure_ascii=False, indent=4)

                print(f"已处理 {filename}")
            except Exception as e:
                print(f"处理 {filename} 时出错: {e}")


if __name__ == '__main__':
    # # 示例调用
    # json_file_path = '/home/ranvane/WorkSpace/Bing-Month-Wallpaper/bing/bing_en-GB.json'
    # item_count ,data= count_items_in_json(json_file_path)
    # print(f"JSON文件中的项数: {item_count}")
    #
    # # 示例JSON变量
    # example_json_variable = [{"key": "value"}, {"key2": "value2"}]
    # variable_item_count = count_items_in_json_variable(data)
    # print(f"JSON变量中的项数: {variable_item_count}")

    process_bing_json(bing_dir)
