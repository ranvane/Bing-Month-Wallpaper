from update_bing_json import fetch_bing_data
import json

a = fetch_bing_data('ROW', 7)
# 使用 json.dumps 格式化输出，indent=4 表示缩进 4 个空格，ensure_ascii=False 确保非 ASCII 字符能正确显示
formatted_json = json.dumps(a, indent=4, ensure_ascii=False)
print(formatted_json)