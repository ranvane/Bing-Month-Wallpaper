# Bing-Month-Wallpaper - Bing壁纸收集站

一个自动收集和展示Microsoft Bing每日壁纸的网站项目，提供美观的浏览体验。

## 项目特点

- 🖼️ 自动收集每日Bing壁纸
- 📅 按年月组织壁纸，方便浏览
- 🎨 美观的网格布局展示
- 📱 响应式设计，支持移动端浏览
- 🔄 自动化更新流程
- ⚡ 静态站点，加载速度快



本项目[Bing-Month-Wallpaper](https://github.com/ranvane/Bing-Month-Wallpaper)是[wallpaper-changer](https://github.com/ranvane/wallpaper-changer)的配套项目。

### 目的：

旨在通过自己部署Bing-Month-Wallpaper，为wallpaper-changer提供安全可靠的壁纸数据api。

### 注意：

本项目数据来自[Bing Daily Wallpaper](https://github.com/zigou23/Bing-Daily-Wallpaper)和[bing-wallpaper-archive](https://github.com/zigou23/Bing-Daily-Wallpaper)项目中，数据经过整理后合并。

ps：

Bing Daily Wallpaper：一个每天自动下载Bing每日壁纸的脚本，支持Windows、Linux、MacOS。
bing-wallpaper-archive：一个保存了Bing2016-2021年的bing每日壁纸的归档网站。
### GitHub Actions + Cloudflare Pages 部署

项目使用GitHub Actions自动生成Markdown格式文档，并通过Cloudflare Pages发布为网站。整个流程如下：

1. **GitHub Actions 工作流程**：
   - 每日自动触发（UTC时间01:00）或手动触发
   - 获取最新的Bing壁纸数据
   - 处理数据并生成Markdown格式文档
   - 将生成的文档推送到指定分支

2. **Cloudflare Pages 自动构建**：
   - 监听GitHub仓库的变更
   - 自动拉取最新的Markdown文档
   - 将Markdown渲染成静态HTML页面
   - 发布到全球CDN网络

#### 部署步骤

1. **准备GitHub仓库**：
   ```bash
   # Fork此项目到您的GitHub账户
   # 克隆到本地进行必要的修改
   git clone https://github.com/yourusername/Bing-Month-Wallpaper.git
   cd Bing-Month-Wallpaper
   ```

2. **配置GitHub Actions**：
   - 确保`.github/workflows/update.yml`文件存在
   - 工作流将自动执行数据获取和Markdown生成
   - 生成的Markdown文件会保存在`content/`目录下

3. **连接Cloudflare Pages**：
   - 登录Cloudflare Dashboard
   - 进入Pages部分，点击"创建项目"
   - 选择"连接到Git"
   - 授权Cloudflare访问您的GitHub账户
   - 选择ttbing仓库
   - 配置构建设置：
     - 构建命令：留空（因为我们已经生成了Markdown）
     - 构建输出目录：`content`
     - 根目录：`/`

4. **配置环境变量（可选）**：
   - 如需自定义构建流程，可在Cloudflare Pages设置中添加环境变量
   - 例如：`NODE_VERSION=18`

5. **部署完成后**：
   - Cloudflare会自动为您的网站分配一个`.pages.dev`域名
   - 您可以在Pages设置中添加自定义域名

#### 工作流程详解

GitHub Actions负责以下步骤：

1. **数据获取**：运行`fetch_bing.py`获取最新的Bing壁纸数据
2. **数据处理**：将获取的数据转换为结构化格式
3. **Markdown生成**：运行`generate_markdown.py`生成美观的Markdown页面
4. **版本控制**：将生成的Markdown文件提交并推送到仓库

Cloudflare Pages负责：

1. **自动构建**：检测到仓库更新后自动触发构建
2. **Markdown渲染**：将Markdown文件转换为HTML页面
3. **资源优化**：自动优化CSS、JavaScript和图片资源
4. **全球分发**：通过Cloudflare的CDN网络全球分发内容

### 手动触发更新

您也可以手动触发更新流程：

1. 进入GitHub项目的Actions页面
2. 选择"Update Bing Wallpaper"工作流
3. 点击"Run workflow"按钮
4. 选择要更新的日期范围
5. 点击"Run workflow"开始更新

## 自定义配置

您可以通过修改以下文件来自定义项目：

- `scripts/fetch_bing.py` - 修改壁纸获取逻辑
- `scripts/generate_markdown.py` - 调整页面生成参数，如每行显示的图片数量
- `.github/workflows/update.yml` - 修改自动更新频率和流程

## 可能遇到的问题：

1、存在workflows：pages-build-deployment
点选仓库Settings –> pages –> Build and deployment ，修改source选项，默认是 Deploy from a branch ，修改为Github Actions，修改完成后，回到Actions界面，删除之前的 pages-build-deployment workflows即可，后面就不会再出现了。
2、工作流运行失败：

```
1265
remote: Permission to xxx/Bing-Month-Wallpaper.git denied to github-actions[bot].
1266
fatal: unable to access 'https://github.com/xxx/Bing-Month-Wallpaper/': The requested URL returned error: 403
1267
Error: Process completed with exit code 128.
```

Actions 权限设置：进入仓库的 Settings -> Actions -> General，在 Workflow permissions 部分，选择 Read and write permissions，这样可以让 GITHUB_TOKEN 有写入权限。


## 致谢

- 感谢Microsoft Bing提供的高质量壁纸
- 感谢GitHub Actions提供的自动化工作流
- 感谢Cloudflare Pages提供的静态网站托管服务