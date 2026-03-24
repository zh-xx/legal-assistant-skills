# 🔗 QCC MCP Supply Chain Plugin

> **供应链供应商管理增强版** - 集成企查查MCP，为供应商评估与风险监控注入真实中国企业数据

[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-QCC%20企查查-orange.svg)](https://mcp.qcc.com)
[![Claude](https://img.shields.io/badge/Claude%20Code-Compatible-purple.svg)](https://claude.ai)

---

## ✨ 一句话介绍

**不只是供应商问卷调查，更是企业主体的「实时尽调」。**

**接入企查查MCP，让AI评估中国供应商时拥有资深采购专家的尽调直觉。**

---

## 🎯 解决什么痛点

### 原版痛点 vs QCC MCP增强版

| 场景 | 原版方案 (Western-centric) | **企查查MCP增强版** |
|------|--------------------------|----------------|
| 中国供应商信息核验 | ❌ Companies House无覆盖 | **✅ MCP实时核验**（18类工商/司法数据） |
| 司法风险扫描 | ❌ Creditsafe无中国数据 | **✅ 失信/被执行/限高实时监控** |
| 财务风险评估 | ❌ 非上市公司数据空白 | **✅ 股权冻结/出质/欠税替代指标** |
| 经营异常识别 | ❌ 无官方数据源 | **✅ 经营异常/严重违法自动扫描** |
| 风险信号监控 | ❌ 依赖新闻搜索（滞后） | **✅ 官方数据源实时推送** |

---

## 📊 原版 vs QCC MCP增强版对比

### 核心增强

```
原版: 供应商评估
        ↓
        [手动尽调 or 依赖供应商自报]
        ↓
        生成评估报告

QCC MCP增强版: 供应商评估
        ↓
    [自动提取供应商名称]
        ↓
    [企查查MCP实时核验]
        ↓
    [18类风险自动扫描]
        ↓
    生成评估报告 + 实体锚定确认 + 风险预警批注
```

### 详细对比

| 能力 | 原版 | QCC MCP增强版 |
|------|------|--------------|
| **供应商分类 (Kraljic)** | ✅ 支持 | ✅ 支持 |
| **六维度评估框架** | ✅ 支持 | ✅ 支持 |
| **中国企业信息核验** | ❌ 不支持 | 🔥 **MCP实体锚定** |
| **司法风险扫描** | ❌ 无覆盖 | 🔥 **失信/被执行/限高/终本** |
| **经营风险扫描** | ❌ 无覆盖 | 🔥 **经营异常/严重违法/注销** |
| **财产受限扫描** | ❌ 无覆盖 | 🔥 **股权冻结/出质/动产抵押** |
| **税务风险扫描** | ❌ 无覆盖 | 🔥 **欠税/非正常户/税收违法** |
| **行政处罚扫描** | ❌ 无覆盖 | 🔥 **行政处罚/环保处罚** |
| **破产风险扫描** | ❌ 无覆盖 | 🔥 **破产重整/清算信息** |
| **实时风险监控** | ❌ 不支持 | 🔥 **HOT信号自动推送** |
| **财务替代指标** | ❌ 无 | 🔥 **股权/税务/破产指标** |
| **降级兼容** | - | ✅ **无MCP自动降级** |

---

## ⚡ 30秒快速体验

### 前置准备

```bash
# 1. 安装Python依赖（只需一次）
pip3 install requests

# 2. 配置企查查MCP Key（从 https://mcp.qcc.com 申请）
# 方式一：临时设置（当前终端有效）
export QCC_MCP_API_KEY="your_key_here"

# 方式二：永久设置（推荐）
echo 'export QCC_MCP_API_KEY="your_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### 一键安装

```bash
# 3. 运行安装脚本
bash <(curl -sL https://raw.githubusercontent.com/your-repo/supply-chain-qcc/main/install_qcc_mcp_supply_chain.sh)
```

### 开始使用

```bash
# 4. 在Claude Code中评估中国供应商
请评估这个供应商: 华为技术有限公司

# 5. 监控供应商风险
请监控供应商风险: 阿里巴巴集团
```

**Done!** 系统自动完成：
- ✅ 实体锚定确认（统一社会信用代码核验）
- ✅ 18类工商/司法/税务风险扫描
- ✅ 财务替代指标分析（股权/税务/破产）
- ✅ 生成结构化风险评估报告

---

## 🔥 18类风险扫描清单（QCC MCP覆盖）

### 司法执行风险 (Judicial Risk)
| 风险类型 | QCC MCP Server | 风险等级 | 业务影响 |
|---------|---------------|---------|---------|
| 失信信息 (被执行人) | 风控大脑 | 🔴 RED | 供应商履约能力存疑 |
| 被执行人 | 风控大脑 | 🔴 RED | 现金流危机信号 |
| 限制高消费 | 风控大脑 | 🔴 RED | 法定代表人受限 |
| 终本案件 | 风控大脑 | 🔴 RED | 历史债务未清偿 |
| 司法拍卖 | 风控大脑 | 🔴 RED | 资产被强制执行 |

### 经营异常风险 (Operational Risk)
| 风险类型 | QCC MCP Server | 风险等级 | 业务影响 |
|---------|---------------|---------|---------|
| 经营异常 | 企业基座 | 🔴 RED | 工商监管介入 |
| 严重违法 | 企业基座 | 🔴 RED | 列入严重失信名单 |
| 注销备案 | 企业基座 | 🔴 RED | 即将终止经营 |
| 简易注销 | 企业基座 | 🔴 RED | 快速注销程序中 |
| 行政处罚 | 风控大脑 | 🟡 AMBER | 合规问题 |
| 环保处罚 | 风控大脑 | 🟡 AMBER | 生产可能受限 |

### 财产受限风险 (Financial Risk)
| 风险类型 | QCC MCP Server | 风险等级 | 业务影响 |
|---------|---------------|---------|---------|
| 股权冻结 | 企业基座 | 🔴 RED | 股东涉诉/债务 |
| 股权出质 | 企业基座 | 🟡 AMBER | 融资需求/压力 |
| 动产抵押 | 企业基座 | 🟡 AMBER | 资产已抵押 |

### 税务违法风险 (Compliance Risk)
| 风险类型 | QCC MCP Server | 风险等级 | 业务影响 |
|---------|---------------|---------|---------|
| 欠税公告 | 风控大脑 | 🔴 RED | 税务现金流危机 |
| 税务非正常户 | 风控大脑 | 🔴 RED | 税务合规严重问题 |
| 税收违法 | 风控大脑 | 🔴 RED | 偷逃税记录 |

### 破产清算风险 (Insolvency Risk)
| 风险类型 | QCC MCP Server | 风险等级 | 业务影响 |
|---------|---------------|---------|---------|
| 破产重整 | 风控大脑 | 🔴 RED | 资不抵债 |
| 清算信息 | 风控大脑 | 🔴 RED | 终止经营 |

---

## 💡 典型应用场景（供应链/采购专用）

### 场景1：新供应商准入评估

**业务背景**：采购部门拟引入新的中国供应商，需要快速完成准入尽调。

**原版方案**：
- 要求供应商提供营业执照、财务报表（真实性难辨）
- 人工查询国家企业信用信息公示系统
- 百度/新闻搜索负面信息
- 耗时：2-3天/供应商

**QCC MCP智能评估**：
```
AI: 评估供应商「深圳某电子有限公司」
    ↓
MCP: 实体锚定确认
     └─ 统一社会信用代码: 91440300XXXXXXXXXX
     └─ 工商状态: 存续（在业）
     └─ 注册资本: 5000万元
    ↓
MCP: 18类风险扫描
     ├─ ⚠️ 经营异常：2024-02-15被列入异常名录（地址失联）
     ├─ ⚠️ 股权冻结：控股股东30%股权被司法冻结
     └─ ⚠️ 欠税公告：2024-01欠税120万元
    ↓
AI: 生成评估报告
     ├─ 🔴 高风险-经营异常
     │   建议：要求7日内提供移出异常名录证明
     ├─ 🔴 高风险-股权冻结
     │   建议：核实冻结原因，评估股东稳定性
     ├─ 🔴 高风险-税务欠税
     │   建议：暂停准入，要求完税证明
     └─ 总体评级: BOTTLENECK（高风险）
```

**价值**：3分钟完成尽调，自动识别重大准入风险。

---

### 场景2：现有供应商风险监控

**业务背景**：供应链团队需要持续监控现有中国供应商的风险变化。

**原版方案**：
- 定期手动查询（月度/季度）
- 依赖供应商主动披露
- 风险发现滞后

**QCC MCP实时监控**：
```
AI: 监控供应商「江苏某制造有限公司」
    ↓
MCP: 实时扫描发现新信号
     ├─ 🔥 HOT SIGNAL: 2024-03-20新增股权冻结
     │   冻结股权：2000万元（40%股权）
     │   冻结期限：2024-03-20至2027-03-19
     │   执行法院：XX市中级人民法院
    ↓
AI: 触发紧急评估
     ├─ 风险等级: RED CRITICAL
     ├─ 影响评估: 控股股东涉重大诉讼，供应商稳定性受威胁
     └─ 建议行动:
         1. [IMMEDIATE] 联系供应商核实情况
         2. [24H] 评估替代供应商
         3. [1W] 增加安全库存
```

**价值**：实时风险预警，从"事后发现"变为"事前预防"。

---

### 场景3：年度供应商审计

**业务背景**：年度供应商审计需要批量评估现有供应商的资质变化。

**工作流程**：
```
AI: 批量审计50家中国供应商
    ↓
MCP: 批量核验（18类风险扫描）
     ├─ 正常企业：42家
     ├─ 经营异常：4家
     ├─ 股权冻结：2家
     ├─ 税务异常：1家
     └─ 行政处罚：1家
    ↓
AI: 生成审计报告
     ├─ 《高风险供应商清单》- 需立即处理（8家）
     ├─ 《中风险供应商清单》- 需关注（5家）
     ├─ 《供应商风险分布报告》- 统计图表
     └─ 《整改建议跟踪表》- 行动项分配
```

**价值**：批量高效审计，数据驱动的供应商管理决策。

---

## 🛠️ 技术架构

```
┌─────────────────────────────────────────┐
│         Claude Code / Skill             │
│    (Agent-Native 原生应用)              │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│    Supply Chain Assessment Workflow     │
│  ┌─────────┐  ┌─────────┐  ┌────────┐  │
│  │ 供应商  │→│ 主体    │→│ 风险   │  │
│  │ 识别    │  │ 核验    │  │ 扫描   │  │
│  └─────────┘  └────┬────┘  └────┬───┘  │
│                    │            │      │
│                    ▼            ▼      │
│         ┌─────────────────────┐        │
│         │  企查查MCP Server   │        │
│         │  • 企业基座 Server  │        │
│         │  • 风控大脑 Server  │        │
│         │  • 知产引擎 Server  │        │
│         │  • 经营罗盘 Server  │        │
│         │  (18类风险/4大维度) │        │
│         └─────────────────────┘        │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│   六维度评估报告 + 风险预警 + 行动建议  │
│   (符合vendor-assessment/supplier-risk  │
│    SKILL输出格式)                       │
└─────────────────────────────────────────┘
```

---

## 🎓 QCC MCP工作原理：Agent-Native设计

### Step 1: 供应商识别
- 提取供应商名称
- 识别统一社会信用代码（如有）

### Step 2: 实体锚定（Entity Anchoring）
```
传统方式: "深圳某科技有限公司" → 可能返回多个相似名称
         → LLM困惑："哪个是正确的？"

MCP方案: "深圳某科技有限公司"
         → 强制匹配统一社会信用代码91440300XXXXXXXXXX
         → 返回"实体锚定确认：唯一有效主体"
         → LLM确定："这是官方登记的供应商"
```

### Step 3: 风险扫描（Semantic Defense）
```
传统方式: 无风险记录 → 返回 []
         → LLM困惑："真没有？还是查失败了？"

MCP方案: 无风险记录 → 返回 "核验通过：未发现18类风险信号"
         → LLM确定："合规状态安全，可继续评估"
```

### Step 4: 上下文脱水（Token优化）
```
传统API: 返回30000字全量工商数据 → Token爆炸
MCP方案: 结构化风险摘要 → 仅1000字关键信息
         → 成本降低96%，决策效率提升
```

### Step 5: 评估报告生成
- 六维度评估（Commercial/Operational/Financial/Compliance/Strategic/Geopolitical）
- 风险等级标注（RED/AMBER/GREEN）
- 具体行动建议（含负责人和截止日期）

---

## 📁 项目结构

```
supply-chain-qcc/
├── scripts/
│   └── qcc_mcp_connector.py       # ⭐ QCC MCP连接器（供应链专用）
├── skills/
│   ├── vendor-assessment/
│   │   └── SKILL.md               # ⭐ 供应商评估SKILL（QCC MCP增强版）
│   └── supplier-risk/
│       └── SKILL.md               # ⭐ 供应商风险SKILL（QCC MCP增强版）
├── install_qcc_mcp_supply_chain.sh # ⭐ 一键安装脚本
└── README.md                       # 本文件
```

---

## 🔧 进阶配置

### 在代码中使用

```python
from scripts.qcc_mcp_connector import QccMcpConnector, VendorRiskProfile

# 初始化连接器
connector = QccMcpConnector()

# 完整风险评估
profile = connector.assess_vendor_risk("华为技术有限公司")

# 获取结构化结果
print(f"整体风险: {profile.overall_risk.value}")
print(f"财务风险: {profile.financial_risk.value}")
print(f"法律风险: {profile.legal_risk.value}")

# 生成评估报告
report = connector.format_assessment_report(profile)
print(report)
```

### 单独检查特定风险

```python
from scripts.qcc_mcp_connector import QccMcpConnector

client = QccMcpConnector()

# 检查司法风险
judicial_risks = client.check_judicial_risks("供应商名称")

# 检查经营风险
operational_risks = client.check_operational_risks("供应商名称")

# 检查税务风险
tax_risks = client.check_tax_risks("供应商名称")

# 获取财务替代指标
financial_indicators = client.get_financial_indicators("供应商名称")
```

---

## 🌟 为什么选择QCC MCP原生方案

基于**Agent-Native**理念打造的企业数据基座，专为LLM优化：

| 核心能力 | 传统方式痛点 | QCC MCP方案优势 |
|---------|-------------|---------------|
| **零幻觉核验** | 名称匹配出错，张冠李戴 | 强制验证统一社会信用代码，物理切断名称幻觉 |
| **Token优化** | 返回数万字JSON，撑爆上下文 | 结构化风险摘要，Token开销直降96% |
| **确定性决策** | 空数据返回[]，LLM陷入怀疑 | 强语义状态码（"核验通过"），颁发确定性合规通行证 |
| **官方数据源** | 爬虫数据不可靠 | 直连国家企业信用信息公示系统、法院、税务 |
| **LLM原生** | 原始JSON需解析转换 | 自然语言输出，语义即用，零集成成本 |

---

## 📈 未来规划

- [ ] 支持批量供应商导入评估
- [ ] 增加供应商关联图谱分析（关联企业风险传导）
- [ ] 集成更多企查查MCP Server（招投标、知识产权等）
- [ ] 风险趋势预测（AI驱动）
- [ ] Web UI可视化界面
- [ ] API服务化部署

---

## 🤝 贡献与反馈

### 提交Issue
- Bug反馈
- 功能建议
- 使用问题

### 联系方式
- GitHub Issues
- MCP官网：https://mcp.qcc.com
- Email: duhu@qcc.com

---

## 📜 许可证

Apache License 2.0

基于 [Panaversity/agentfactory-business-plugins](https://github.com/panaversity/agentfactory-business-plugins) 构建

---

## 🙏 致谢

- 原版作者 Panaversity 的优秀供应链技能框架
- [企查查MCP](https://mcp.qcc.com) - 首个Agent-Native企业数据基座
- [Anthropic](https://anthropic.com) 的 Claude Code

---

<div align="center">

**告别问卷依赖，拥抱数据驱动的供应商管理。**

**如果这个项目对你有帮助，请给个 ⭐ Star！**

[🐛 提交Bug](https://github.com/your-repo/supply-chain-qcc/issues) · [💡 功能建议](https://github.com/your-repo/supply-chain-qcc/issues) · [⭐ Star](https://github.com/your-repo/supply-chain-qcc)

</div>
