# HYZL_guanwang：华云智联官网 V2.0

本仓库包含华云智联（huayunzhilian.cn）官网改版的全部资料与代码：

- 前期设计调研
- 开发前设计文档
- 素材库
- 网站源码：Nuxt 4 前端 + Spring Boot 4 内容服务
- 部署脚本

**正式部署环境为 Linux**，见下文第 2 节。

## 1. 仓库结构

| 目录 | 内容 |
|---|---|
| [`website/`](./website/README.md) | 官网代码：`apps/web` 前端（Nuxt 4 / Vue 3，SSR）、`apps/api` 内容与业务服务（Spring Boot 4 / Java 21）、`tools/` 内容生成与演示包脚本、`docs/` 架构 / ADR / 测试报告 / 内容待办 |
| [`design_document/`](./design_document/README.md) | 开发前文档 v0.2：现网盘点、内容与布局、素材迁移、K-01…K-07 岗位文档、驱动板、设计 Token |
| [`research/`](./research/README.md) | 国内外 AI 与工业软件头部企业官网设计调研 |
| [`素材库/`](./素材库/) | 现网原图 277 张、页面截图 58 张、官网补录文字、素材索引（网站内容由此生成） |

## 2. Linux 部署

### 2.1 运行架构

```text
用户浏览器 ──HTTPS 443──► Nginx（TLS 终止、静态缓存、gzip）
                            │  反向代理 127.0.0.1:3000
                            ▼
                     hyzl-web  ：Nuxt SSR（Node.js），端口 3000，只监听本机
                            │  /api/v1/* 服务端转发 127.0.0.1:8080
                            ▼
                     hyzl-api  ：Spring Boot（Java），端口 8080，只监听本机
                            │
                            ▼
              PostgreSQL 16（生产推荐）或 内置 H2 文件库（单机 / 演示）
```

对外只开放 80 / 443；3000、8080、5432 端口均不对外。

### 2.2 服务器配置

| 项 | 最低 | 推荐 |
|---|---|---|
| 操作系统 | 64 位 Linux（x86_64 或 ARM64），systemd | Ubuntu 22.04 / 24.04 LTS、Rocky Linux / RHEL 9、Debian 12。国产系统（openEuler、麒麟、统信）满足下表软件版本即可 |
| CPU / 内存 | 2 核 / 2 GB | 2 核 / 4 GB（构建时 Node 与 Maven 峰值约 1.5 GB） |
| 磁盘 | 5 GB 可用 | 20 GB（含依赖缓存、日志、数据库） |
| 网络 | 首次构建需访问 Maven 中央库与 npm 源（可配置国内镜像，见 2.4）；运行时无需外网 | — |

### 2.3 软件环境

| 软件 | 版本要求 | 用途 | 检查命令 | 说明 |
|---|---|---|---|---|
| **JDK** | **21 及以上**（已验证 21、25） | 构建并运行内容服务 | `java -version` | 需要完整 JDK，不能只装 JRE。推荐 Eclipse Temurin 21 或 OpenJDK 21 |
| **Node.js** | **22.22.3+ 或 24.15+**（Nuxt 4.6 官方支持范围） | 构建并运行网站 | `node -v` | 自带 npm 10+。低于该版本脚本会给出警告 |
| **Git** | 2.x | 拉取代码 | `git --version` | — |
| **curl** | 任意 | 健康检查（`hyzl.sh` 使用） | `curl --version` | — |
| **Nginx** | 1.18+ | 反向代理、HTTPS | `nginx -v` | 生产必需；内网演示可省略 |
| PostgreSQL | 16（已验证 16.15） | 生产数据库 | `psql --version` | 可选。不配置时使用内置 H2 文件库（数据在 `website/data/`），适合单机或演示 |
| Python | 3.10+，带 Pillow | 修改素材库后重新生成内容 | `python3 --version` | 可选，只在维护内容时需要 |

**不需要单独安装的：**

- Maven：`apps/api/mvnw` 会自动下载 3.9.11。
- Docker。
- Redis。

### 2.4 安装软件

**Ubuntu 22.04 / 24.04**

```bash
sudo apt update
sudo apt install -y openjdk-21-jdk-headless git curl nginx
# Node.js 24 LTS（NodeSource 源）
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs
# 可选：PostgreSQL 16（24.04 自带 16；22.04 需先添加 PostgreSQL 官方 apt 源）
sudo apt install -y postgresql
```

**Rocky Linux / RHEL 9 及兼容系统**

```bash
sudo dnf install -y java-21-openjdk-devel git curl nginx
curl -fsSL https://rpm.nodesource.com/setup_24.x | sudo bash -
sudo dnf install -y nodejs
# 可选：PostgreSQL 16
sudo dnf module enable -y postgresql:16 && sudo dnf install -y postgresql-server
sudo postgresql-setup --initdb && sudo systemctl enable --now postgresql
```

**Debian 12**：系统源没有 JDK 21，请安装 Eclipse Temurin 21（adoptium.net 的 apt 源）。Node.js 同样用 NodeSource 安装。

**国内网络加速（可选）：**

```bash
npm config set registry https://registry.npmmirror.com
mkdir -p ~/.m2 && cat > ~/.m2/settings.xml <<'EOF'
<settings><mirrors><mirror><id>aliyun</id><mirrorOf>central</mirrorOf>
<url>https://maven.aliyun.com/repository/public</url></mirror></mirrors></settings>
EOF
export MVNW_REPOURL=https://maven.aliyun.com/repository/public   # Maven 本体也从镜像下载
```

### 2.5 快速部署（单机，一条命令）

适合测试服务器和内网演示。使用内置 H2 数据库，进程由脚本后台管理。

```bash
git clone https://github.com/1940553872/HYZL_guanwang.git /opt/hyzl
cd /opt/hyzl/website
./start.sh                  # 首次自动构建（3–6 分钟），之后约 10 秒启动
./hyzl.sh status            # 查看状态；./stop.sh 停止；./hyzl.sh logs api|web 看日志
```

- 启动后访问 http://127.0.0.1:3000。
- 需要让局域网直接访问时，用 `HYZL_HOST=0.0.0.0 ./start.sh` 启动。
- 更多参数见 [website/docs/本地部署说明.md](./website/docs/本地部署说明.md)。

### 2.6 正式部署（systemd + Nginx + PostgreSQL）

**① 创建用户、目录，构建**

```bash
sudo useradd -r -m -d /opt/hyzl -s /bin/bash hyzl
sudo -u hyzl git clone https://github.com/1940553872/HYZL_guanwang.git /opt/hyzl/src
cd /opt/hyzl/src/website
sudo -u hyzl bash -c 'cd apps/api && ./mvnw -q -DskipTests package'   # → apps/api/target/hyzl-api.jar
sudo -u hyzl bash -c 'cd apps/web && npm ci && npm run build'         # → apps/web/.output（构建后自动自检）
sudo mkdir -p /var/lib/hyzl /etc/hyzl && sudo chown hyzl: /var/lib/hyzl
```

**② 数据库（使用 PostgreSQL 时）**

```bash
sudo -u postgres psql -c "CREATE USER hyzl PASSWORD '请替换为强密码'"
sudo -u postgres createdb -O hyzl hyzl
```

首次启动时，表结构由 Flyway 自动创建，网站内容自动导入。

**③ 配置文件 `/etc/hyzl/hyzl.env`**（权限 600，属主 root）

> ⚠️ 代码中内置的密钥是公开的演示值，**正式环境必须全部替换**。

```ini
# 内容服务
PORT=8080
SERVER_ADDRESS=127.0.0.1
HYZL_DATA_DIR=/var/lib/hyzl
HYZL_CORS_ORIGINS=https://www.huayunzhilian.cn
DB_URL=jdbc:postgresql://127.0.0.1:5432/hyzl
DB_USER=hyzl
DB_PASSWORD=请替换为强密码
# 字段加密与去重密钥：openssl rand -base64 16 / openssl rand -hex 32
HYZL_SM4_KEY=请替换
HYZL_HMAC_KEY=请替换
# 线索管理接口令牌（留空则关闭）：openssl rand -hex 24
HYZL_ADMIN_TOKEN=
```

如果不用 PostgreSQL，删掉 `DB_*` 三行即可，系统会使用 `/var/lib/hyzl` 下的 H2 文件库。

**④ systemd 服务**

`/etc/systemd/system/hyzl-api.service`：

```ini
[Unit]
Description=HYZL website content API
After=network.target postgresql.service

[Service]
User=hyzl
EnvironmentFile=/etc/hyzl/hyzl.env
ExecStart=/usr/bin/java -Xms256m -Xmx512m -jar /opt/hyzl/src/website/apps/api/target/hyzl-api.jar
Restart=on-failure
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target
```

`/etc/systemd/system/hyzl-web.service`：

```ini
[Unit]
Description=HYZL website (Nuxt SSR)
After=network.target hyzl-api.service

[Service]
User=hyzl
Environment=NODE_ENV=production PORT=3000 HOST=127.0.0.1
Environment=NUXT_API_BASE=http://127.0.0.1:8080
Environment=NUXT_PUBLIC_SITE_URL=https://www.huayunzhilian.cn
ExecStart=/usr/bin/node /opt/hyzl/src/website/apps/web/.output/server/index.mjs
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload && sudo systemctl enable --now hyzl-api hyzl-web
curl -s http://127.0.0.1:8080/actuator/health   # {"status":"UP"}
curl -s http://127.0.0.1:3000/api/health        # {"status":"ok","web":"UP","api":"UP",...}
```

**⑤ Nginx：`/etc/nginx/conf.d/hyzl.conf`**

证书路径换成你自己的。

```nginx
server {
    listen 80;
    server_name www.huayunzhilian.cn huayunzhilian.cn;
    return 301 https://www.huayunzhilian.cn$request_uri;
}
server {
    listen 443 ssl http2;   # Nginx 1.25.1+ 可改写为 listen 443 ssl; 加 http2 on;
    server_name www.huayunzhilian.cn;
    ssl_certificate     /etc/nginx/cert/huayunzhilian.cn.pem;
    ssl_certificate_key /etc/nginx/cert/huayunzhilian.cn.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    client_max_body_size 1m;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

然后执行 `sudo nginx -t && sudo systemctl reload nginx`。如需 HTTP 跳转到无 `www` 的域名，按实际域名调整 `server_name`。

### 2.7 日常运维

| 操作 | 命令 |
|---|---|
| 查看状态 / 日志 | `systemctl status hyzl-api hyzl-web`；`journalctl -u hyzl-api -f` |
| 更新版本 | `cd /opt/hyzl/src && sudo -u hyzl git pull`，重新执行 2.6 ① 的两条构建命令，再 `sudo systemctl restart hyzl-api hyzl-web` |
| 修改网站内容 | 修改 `素材库/` 后运行 `python3 website/tools/build_content.py`，重新构建并重启。内容服务检测到种子变化会自动重新导入 |
| 查看留资线索 | 在服务器上执行 `curl -H "Authorization: Bearer <HYZL_ADMIN_TOKEN>" http://127.0.0.1:8080/admin/v1/leads`。接口只监听本机，远程请通过 SSH 隧道访问 |
| 备份 | PostgreSQL：`pg_dump hyzl > hyzl-$(date +%F).sql`；H2：停服务后备份 `/var/lib/hyzl/` |
| 接口文档 | http://127.0.0.1:8080/api/v1/docs（本机或 SSH 隧道访问） |
| 运行测试 | `cd website/apps/api && ./mvnw test`；`cd website/apps/web && npm test && npx playwright test`（端到端测试需先启动站点并执行 `npx playwright install chromium`） |

### 2.8 上线前检查清单

- [ ] `/etc/hyzl/hyzl.env` 中的 `HYZL_SM4_KEY`、`HYZL_HMAC_KEY`、数据库密码已替换为新生成的值。
- [ ] `NUXT_PUBLIC_SITE_URL` 与 `HYZL_CORS_ORIGINS` 已改为正式域名，sitemap 与 canonical 才会正确。
- [ ] 防火墙只开放 80 / 443；3000 / 8080 / 5432 仅本机可访问。
- [ ] HTTPS 证书有效，`http://` 已跳转到 `https://`。
- [ ] 已处理 [内容待办](./website/docs/CONTENT_TODO.md) 中的事项：证书有效期、标准编号核实、客户名称授权、广告法用语等。
- [ ] 已配置数据库定时备份。

## 3. 其他文档

- 网站代码说明：[website/README.md](./website/README.md)：页面清单、目录结构、常用命令
- [架构说明](./website/docs/architecture.md)
- [ADR](./website/docs/adr/)
- [测试报告](./website/docs/test-report.md)
- [本地部署说明（含 Windows 与静态演示包）](./website/docs/本地部署说明.md)
- 设计文档：[design_document/README.md](./design_document/README.md)
