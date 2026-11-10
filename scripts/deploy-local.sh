#!/usr/bin/env bash
# 把 Windows 侧构建产物同步到 1Panel 的静态站目录
#
# 用法（在 WSL 里）：
#   bash /mnt/d/WorkBuddy/写作/scripts/deploy-local.sh
#
# 用法（从 Windows 直接调）：
#   ssh walker@127.0.0.1 'bash /mnt/d/WorkBuddy/写作/scripts/deploy-local.sh'
#
# 前提：先在 Windows 上跑过 npm run build，产物在 D:\WorkBuddy\写作\site

set -euo pipefail

SRC="/mnt/d/WorkBuddy/写作/site/"
DEST="/opt/1panel/www/sites/architecture-cost/index"
URL="http://127.0.0.1:8088/"

if [ ! -f "${SRC}index.html" ]; then
  echo "✗ 找不到 ${SRC}index.html —— 先在 Windows 侧执行 npm run build" >&2
  exit 1
fi

sudo mkdir -p "$DEST"
sudo rsync -a --delete "$SRC" "$DEST/"

COUNT=$(sudo find "$DEST" -type f | wc -l)
SIZE=$(sudo du -sh "$DEST" | cut -f1)
echo "✓ 已同步 ${COUNT} 个文件（${SIZE}）→ ${DEST}"

# 静态内容更新不需要 reload，Nginx 每次请求都读磁盘；这里只做一次可达性检查
CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "$URL" || echo "000")
if [ "$CODE" = "200" ]; then
  echo "✓ 站点在线：${URL}"
else
  echo "⚠ 站点返回 ${CODE}，检查容器是否在跑：sudo docker ps | grep openresty" >&2
  exit 1
fi
