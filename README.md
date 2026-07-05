# HSEC AI Agent

> 全球第一个将量子纠错（QEC）数学应用于经典网络拓扑分析的预测引擎。

## 这是什么

HSEC（Holographic Soft Error Correction）不是一个通用AI，不是大语言模型，不是深度学习框架。它是一个基于物理原理的网络预测工具——用一个拓扑不变量 d₀≈12，对任何类型的网络做出4项标准图论无法做出的预测。

**标准图论告诉你"网络是什么结构"。HSEC告诉你"网络何时崩溃、在哪里崩溃、怎么传播"。**

## 4项独有预测

| 预测 | 含义 | 标准图论能做吗 |
|---|---|---|
| **相变阈值** | d_eff < d₀=12 时网络从可纠错→不可纠错 | ❌ |
| **因果锥** | d_eff(A,B) > d₀ 的节点对不在彼此因果锥内（≠不连通） | ❌ |
| **纠缠曲率奇点** | 介数低但扰动影响大的节点（≠高介数） | ❌ |
| **临界失效规模** | 移除多少节点使 d_eff 跌破 d₀ | ❌（渗流阈值≠相变点） |

## 验证成果

### 合成权重网络（1669节点）

| 指标 | 值 |
|---|---|
| 节点/边 | 1669 / 4287 |
| d_eff | 3.40 (< d₀=12, 不可纠错相) |
| 隐蔽风险节点 | 18个（标准Top50全漏检） |
| 临界失效 | 移除3%节点即触发相变 |

### STRING真实数据网络（1155节点，20840边）

| 指标 | 值 |
|---|---|
| 数据源 | STRING DB v12.0 (bulk download) |
| 过滤阈值 | combined_score ≥ 0.7 (高置信) |
| d_eff | 2.59 (< d₀=12, 不可纠错相) |
| 隐蔽风险节点 | 53个（标准Top50全漏检） |
| Top Hub | TP53 (度=348) |
| 50%碎片化 | 移除43.3%节点 |
| 渗流阈值 | 2.9% |

### TCGA临床生存验证（cBioPortal）

8个基因 × 12个癌症类型 = 96次log-rank test

| 类别 | 有效测试 | 显著(p<0.05) | 显著率 |
|---|---|---|---|
| HSEC隐蔽风险基因 | 44 | 5 | **11.4%** |
| 标准hub基因(对照) | 48 | 5 | **10.4%** |

**结论：HSEC隐蔽风险基因的显著率与标准hub基因相当——但标准方法100%漏检了它们。**

HSEC隐蔽风险基因的显著结果：
- GJA1 in 黑色素瘤: p=0.0032, HR=1.493
- C3 in 黑色素瘤: p=0.0037, HR=0.676
- GJA1 in 乳腺癌: p=0.0239, HR=0.689
- ELANE in 胶质瘤: p=0.0316, HR=1.473
- C3 in 肝细胞癌: p=0.0330, HR=0.688

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动
python app.py
# 或
gunicorn app:app --timeout 120 --workers 2 --bind 0.0.0.0:5000

# 打开浏览器
open http://localhost:5000
```

## 部署

### 腾讯云SCF（推荐，免费，不需信用卡）

1. 创建Web函数，运行环境Python 3.12
2. 上传代码包（ZIP）
3. 监听端口设为9000
4. 详见 `DEPLOY.md`

### Docker

```bash
docker build -t hsec-agent .
docker run -p 5000:5000 hsec-agent
```

### Render / Railway

已包含 `render.yaml` 和 `railway.json`，连接GitHub仓库即可自动部署。

## API使用

```bash
# 健康检查
curl http://localhost:5000/api/health

# 上传网络分析
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"nodes":[{"id":"A"},{"id":"B"},{"id":"C"}],
       "edges":[{"source":"A","target":"B","weight":0.9},
                {"source":"B","target":"C","weight":0.8}]}'

# 使用内置数据集
curl http://localhost:5000/api/dataset/cancer
```

## 项目结构

```
hsec-saas/
├── app.py                  # Flask主应用 (36个路由, 2177行)
├── agent.py                # LLM+HSEC双脑Agent
├── hsec_engine/
│   ├── constants.py        # 物理常数 (d₀=12, ℓ_p, c, ℏ...)
│   ├── hsec.py             # HSEC核心计算
│   └── hsec_predictor.py   # 4项预测引擎
├── templates/              # 4个前端页面
│   ├── landing.html        # 首页
│   ├── dashboard.html      # 分析面板
│   ├── auth.html           # 登录/注册
│   └── agent.html          # AI Agent对话
├── requirements.txt
├── Dockerfile              # Docker部署
├── Procfile                # Render部署
├── render.yaml             # Render配置
├── railway.json            # Railway配置
├── scf_bootstrap           # 腾讯云SCF启动文件
└── DEPLOY.md               # 部署文档
```

## 内置数据集（18个）

金融银行网络、半导体供应链、全球航线、TP53蛋白网络、癌基因PPI、全球断层系统、IEEE118电力网络、生态食物网、免疫信号通路、气候耦合网络、流行病传播、区块链交易、知识图谱、社交网络、物联网、5G基站、脑连接组、AD患者脑网络。

## 已知风险（诚实标注）

1. **d₀=12普适性存疑**: Google Willow Λ(5,7)=2.14 → d₀=2.63≠12。d₀=12可能仅对特定码族有效
2. **软件d_eff≠论文d_eff**: 代码用 `nx.average_shortest_path_length`（平均最短路径），论文用面积律 `Area/ℓ_p²`
3. **论文未发表**: 理论未经同行评审
4. **真实数据d_eff未穿越d₀=12**: 在密集PPI网络(平均度36)中，d_eff最大仅9.28，网络先碎片化而非穿越相变点

## 适用的领域

| 第一梯队（有付费意愿） | 第二梯队（需教育市场） | 第三梯队（学术价值） |
|---|---|---|
| 药企靶点识别 | 银行系统性风险 | 生态网络 |
| CRO药物外包 | 电网级联预警 | 地震断层 |
| AI药物发现 | 供应链断链 | 暗物质 |
| 医院脑疾病筛查 | AI幻觉检测 | 气候网络 |

## License

MIT

## 相关论文

《量子纠缠与量子纠错驱动的时空与规范场涌现》（待发表）

## 作者

刘双云
