# 本机先 npm run build（见 deploy/web/build-static.sh），再把 dist 打进 Nginx 镜像。
# 不在镜像里装 Node：国内拉 node 镜像常失败，2 核 ECS 也不适合现场编译。
ARG NGINX_IMAGE=nginx:1.27-alpine

FROM ${NGINX_IMAGE}
COPY deploy/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY frontend/dist /usr/share/nginx/html/h5
COPY admin/dist /usr/share/nginx/html/admin
EXPOSE 80 81 443
