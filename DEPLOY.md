# HSEC SaaS 部署指南（零成本）

## 方案1：腾讯云SCF（推荐，免费，不需信用卡）

### 前置条件
- 腾讯云账号（身份证实名即可，不需要信用卡）
- 免费额度：前3个月每月40万次请求 + 100万GBs资源

### 步骤

1. **上传代码到GitHub**
   - 创建私有仓库 `hsec-saas`
   - 上传所有文件

2. **创建SCF函数**
   - 腾讯云控制台 → 云函数SCF → 新建
   - 函数类型：Web函数
   - 运行环境：Python 3.12
   - 内存：512MB（免费额度内）
   - 监听端口：9000（SCF要求）
   - 代码上传方式：ZIP包上传 或 GitHub拉取

3. **配置启动文件**
   - 确保 `scf_bootstrap` 文件存在且可执行
   - SCF会自动执行该文件启动应用

4. **生成访问域名**
   - SCF → 触发器 → API网关
   - 生成默认域名（三级域名，不需备案）
   - 访问格式：`https://{function-id}.{region}.tencentscf.com/`

5. **上线！**

### 注意事项
- Web函数监听端口必须为9000
- `scf_bootstrap` 必须有可执行权限（`chmod +x scf_bootstrap`）
- 免费额度够小型应用运行3个月
- 自定义域名需要备案，默认域名不需要

---

## 方案2：Docker部署（任何云平台）

```bash
# 构建镜像
docker build -t hsec-agent .

# 运行容器
docker run -d -p 5000:5000 --name hsec hsec-agent

# 打开浏览器
open http://localhost:5000
```

可部署到任何支持Docker的平台：阿里云ECS、华为云CCE、AWS ECS等。

---

## 方案3：Render部署（海外，需要信用卡）

> ⚠️ Render需要Visa/Mastercard信用卡验证，中国银联卡不支持

1. 注册GitHub账号
2. 上传代码到GitHub仓库
3. 去 render.com 用GitHub登录
4. New → Web Service → 连接GitHub仓库
5. 设置：
   - Environment: Python 3
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --timeout 120 --workers 2`
6. 免费域名：`https://hsec-agent.onrender.com`

---

## 方案4：本地运行（最快）

```bash
cd hsec_saas
pip install -r requirements.txt
python3 app.py
```
打开浏览器访问 `http://localhost:5000`

---

## API快速验证

部署后用以下命令验证：

```bash
# 健康检查
curl https://你的域名/api/health

# 上传网络分析
curl -X POST https://你的域名/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"nodes":[{"id":"A"},{"id":"B"},{"id":"C"}],
       "edges":[{"source":"A","target":"B","weight":0.9},
                {"source":"B","target":"C","weight":0.8}]}'

# 使用内置数据集
curl https://你的域名/api/dataset/cancer
```

---

## 接入支付（赚钱）

### 免认证收款（最快）
- 闲鱼挂服务链接，客户付款后手动开通
- 知识星球收年费
- 爱发电（afdian.com）收赞助

### 正式支付
- 微信支付：需个体工商户或公司
- 支付宝当面付：个人可开通

---

## 接单渠道

| 平台 | 定价 | 怎么做 |
|---|---|---|
| 闲鱼 | 500-2000元/单 | 挂"网络拓扑分析服务" |
| 淘宝 | 500-2000元/单 | 开个人店铺 |
| 猪八戒网 | 1000-5000元/单 | 挂数据分析服务 |
| Upwork | $100-500/单 | 面向海外客户 |
| Fiverr | $50-200/单 | 挂gig |

---

## 文件结构

```
hsec-saas/
├── app.py              # Flask主应用 (36路由)
├── agent.py            # LLM+HSEC双脑Agent
├── requirements.txt    # Python依赖
├── Dockerfile          # Docker部署
├── Procfile            # Render部署
├── render.yaml         # Render配置
├── railway.json        # Railway配置
├── scf_bootstrap       # 腾讯云SCF启动文件
├── hsec_engine/        # HSEC核心物理引擎
│   ├── constants.py    # d₀=12等物理常数
│   ├── hsec.py         # 全息软纠错计算
│   └── hsec_predictor.py  # 4项预测引擎
├── templates/
│   ├── landing.html    # 着陆页
│   ├── auth.html       # 登录/注册页
│   ├── dashboard.html  # 控制台仪表板
│   └── agent.html      # 对话式Agent界面
└── data/               # SQLite数据库（自动创建）
```
