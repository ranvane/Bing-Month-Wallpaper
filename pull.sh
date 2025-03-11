echo  "设置Git代理"
# 设置http、https::
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy https://127.0.0.1:7897
# 设置socks:
git config --global http.proxy 'socks5://127.0.0.1:7897'
git config --global https.proxy 'socks5://127.0.0.1:7897'


echo  "git pull origin main"
git pull origin main

## 取消代理
echo  "取消Git代理"
git config --global --unset http.proxy
git config --global --unset https.proxy
echo "按任意键继续..."
read -n 1 -s
echo
