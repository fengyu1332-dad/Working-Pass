# ============================================================
# 专业星图 - Docker 部署
# 多阶段构建：Vite 构建 → Nginx 服务
# ============================================================

# ---- 阶段 1: 构建 ----
FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --production=false

COPY . .
RUN npm run build

# ---- 阶段 2: 生产运行 ----
FROM nginx:1.27-alpine

# 复制自定义 nginx 配置
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:80/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
