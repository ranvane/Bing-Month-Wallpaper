import os

from generate_month_json_data import year_month_langs
from generate_yearly_md import process_index_template_folder, generate_index_md
from update_bing_json import update_lang_data

# 判断是否在 GitHub Workflows 中运行
is_github_workflow = os.getenv('GITHUB_ACTIONS')
# 支持的语言列表（ROW为通用地区）
# LANGS = ['ROW', 'en-US', 'en-CA', 'en-GB', 'en-IN', 'es-ES',
#          'fr-FR', 'fr-CA', 'it-IT', 'ja-JP', 'pt-BR', 'de-DE', 'zh-CN']
LANGS = ['en-US', 'zh-CN']
if is_github_workflow:
    print("Running in GitHub Workflows")
    # 更新所有的地区的最近days天的bing桌面数据
    days = 7
    for lang in LANGS:
        update_lang_data(lang, days)

else:
    print("Running locally")
    days = 7
    for lang in LANGS:
        update_lang_data(lang, days)


year_month_langs()  # 将所有的json文件生成:"年月文件夹/bing_地区.json"的文件
process_index_template_folder()  # 将所有的"年月文件夹/bing_地区.json"的文件生成"年月文件夹/年月.md"的文件
generate_index_md()  # 将所有的"年月文件夹/年月.md"的文件生成"bing/index.md"的文件
