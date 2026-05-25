#!/bin/bash
# 服务器保活脚本
# 自动检测并重启停止的服务器

PORT=3456
LOG_FILE="/workspace/server.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 启动服务器保活脚本..." | tee -a $LOG_FILE

while true; do
    # 检查端口是否被占用
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 服务器运行正常 (端口:$PORT)" | tee -a $LOG_FILE
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 服务器已停止，重新启动..." | tee -a $LOG_FILE
        
        # 先释放端口
        kill -9 $(lsof -ti:$PORT) 2>/dev/null || true
        sleep 1
        
        # 启动服务器
        cd /workspace && python3 -m http.server $PORT > /dev/null 2>&1 &
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 服务器已重启" | tee -a $LOG_FILE
    fi
    
    # 每30秒检查一次
    sleep 30
done
