# Bing-Month-Wallpaper

本项目[Bing-Month-Wallpaper](https://github.com/ranvane/Bing-Month-Wallpaper)是[wallpaper-changer](https://github.com/ranvane/wallpaper-changer)的配套项目。

### 目的：

旨在通过自己部署Bing-Month-Wallpaper，为wallpaper-changer提供安全可靠的壁纸数据api。

### 注意：

本项目数据来自[Bing Daily Wallpaper](https://github.com/zigou23/Bing-Daily-Wallpaper)和[bing-wallpaper-archive](https://github.com/zigou23/Bing-Daily-Wallpaper)项目中，数据经过整理后合并。

ps：

Bing Daily Wallpaper：一个每天自动下载Bing每日壁纸的脚本，支持Windows、Linux、MacOS。
bing-wallpaper-archive：一个保存了Bing2016-2021年的bing每日壁纸的归档网站。

### 部署

1、github actions 部署
    工作流会自动部署，访问地址：地址：`用户名.github.io/Bing-Month-Wallpaper`

2、cloudflare pages部署

最好绑定自定义域名，将设置中将`根目录`设置为`/bing`即可。


### 可能遇到的问题：

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


