# 🔗 QCC MCP Supply Chain Plugin

> **企查查MCP供应链供应商管理插件** - 为中国供应商评估提供实时企业数据支持

[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-QCC%20企查查-orange.svg)](https://mcp.qcc.com)
[![Claude](https://img.shields.io/badge/Claude%20Code-Compatible-purple.svg)](https://claude.ai)

---

## 📋 目录

- [功能概述](#功能概述)
- [快速开始](#快速开始)
- [安装指南](#安装指南)
- [使用方法](#使用方法)
- [9维度评估模型](#9维度评估模型)
- [18类风险清单](#18类风险清单)
- [配置说明](#配置说明)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)

---

## 功能概述

### 解决什么问题？

传统供应商评估对中国企业存在**数据盲区**：
- ❌ Companies House 无中国数据
- ❌ Creditsafe 无中国覆盖
- ❌ 手动查询耗时2-3天
- ❌ 非上市公司财务不可见

### 我们的方案

集成 **企查查MCP**，为中国供应商提供：
- ✅ **实体锚定** - 统一社会信用代码验证
- ✅ **18类风险** - 司法/经营/税务/破产全覆盖
- ✅ **9维度评估** - 基础4维 + 供应链特有3维
- ✅ **实时数据** - 官方数据源直连
- ✅ **3秒评估** - 自动化风险扫描

---

## 快速开始

### 3分钟快速体验

```bash
# 1. 一键安装
bash <(curl -sL https://raw.githubusercontent.com/your-repo/supply-chain-qcc/main/install_qcc_mcp_supply_chain.sh)

# 2. 配置API Key（从 https://mcp.qcc.com 申请）
export QCC_MCP_API_KEY="your_api_key_here"

# 3. 开始评估
/vendor-assessment-qcc 华为技术有限公司
```

---

## 安装指南

### 系统要求

- **操作系统**: macOS / Linux / Windows (WSL)
- **Python**: 3.9+
- **Claude Code**: 最新版本
- **网络**: 可访问 https://mcp.qcc.com

### 详细安装步骤

#### 步骤1: 安装Python依赖

```bash
pip3 install requests
```

#### 步骤2: 申请企查查MCP Key

1. 访问 [企查查MCP官网](https://mcp.qcc.com)
2. 注册企业账号
3. 申请MCP服务授权
4. 获取API Key

#### 步骤3: 配置环境变量

**临时配置（当前终端）:**
```bash
export QCC_MCP_API_KEY="your_api_key_here"
```

**永久配置（推荐）:**
```bash
# macOS
export QCC_MCP_API_KEY="your_api_key_here"

# Linux
export QCC_MCP_API_KEY="your_api_key_here"
```

#### 步骤4: 安装插件

```bash
git clone https://github.com/your-repo/supply-chain-qcc.git
cd supply-chain-qcc
bash install_qcc_mcp_supply_chain.sh
```

---

## 使用方法

### 在Claude Code中使用

#### 供应商评估

```
# 基础评估
/vendor-assessment-qcc 供应商名称

# 示例
/vendor-assessment-qcc 华为技术有限公司
/vendor-assessment-qcc 阿里巴巴集团
```

#### 风险监控

```
# 实时监控
/supplier-risk-qcc 供应商名称

# 示例
/supplier-risk-qcc 深圳某电子有限公司
```

### 在Python代码中使用

```python
from scripts.qcc_mcp_connector import QccMcpConnector

# 初始化连接器
connector = QccMcpConnector()

# 完整评估（9维度）
profile = connector.assess_vendor_risk("供应商名称")

# 查看评估结果
print(f"整体风险: {profile.overall_risk}")
print(f"产能资质风险: {profile.capacity_risk}")      # 供应链特有
print(f"组织稳定性风险: {profile.stability_risk}")   # 供应链特有
print(f"业务健康度风险: {profile.business_health_risk}")  # 供应链特有
```

---

## 9维度评估模型

### 基础4维度（与法务共享）

| 维度 | 说明 | 数据来源 |
|------|------|---------|
| 财务风险 | 股权冻结/欠税/破产 | QCC MCP Enterprise/Risk |
| 经营风险 | 经营异常/严重违法 | QCC MCP Enterprise |
| 合规风险 | 环保处罚/行政处罚 | QCC MCP Risk |
| 法律风险 | 失信/被执行/限高 | QCC MCP Risk |

### 供应链特有3维度 ⭐

| 维度 | 说明 | 数据来源 | 关键指标 |
|------|------|---------|---------|
| **产能资质风险** | 生产许可、质量认证 | QCC MCP Operation | ISO认证、生产许可证、排污许可 |
| **组织稳定性风险** | 股权变更、单点风险 | QCC MCP Enterprise | 分支机构数、股权变更次数 |
| **业务健康度风险** | 信用评级、招投标 | QCC MCP Operation | 官方信用评级、招投标活跃度 |

---

## 18类风险清单

### 🔴 CRITICAL（立即供应中断）

| 风险类型 | 供应链影响 | 响应时间 |
|---------|-----------|---------|
| 破产重整 | 供应关系终止 | < 4小时 |
| 失信信息 | 信用崩溃 | < 4小时 |
| 被执行人 | 现金流危机 | < 24小时 |
| 环保处罚(停产) | 生产被迫停止 | < 24小时 |
| 经营异常 | 监管介入 | < 48小时 |

### 🔴 HIGH（供应不稳定）

| 风险类型 | 供应链影响 | 响应时间 |
|---------|-----------|---------|
| 严重违法 | 可能吊销执照 | < 48小时 |
| 注销备案 | 主动终止经营 | < 48小时 |
| 股权冻结 | 控制权不稳定 | < 48小时 |

### 🟡 MEDIUM（财务/合规风险）

股权出质、欠税、税务异常、终本案件等

### 🔵 LOW（一般合规风险）

一般行政处罚

---

## 配置说明

### 必需配置

```bash
# 企查查MCP API Key
export QCC_MCP_API_KEY="your_api_key_here"
```

### 可选配置

```bash
# 风险阈值（根据企业标准调整）
export QCC_OTD_THRESHOLD="90"          # OTD阈值
export QCC_QUALITY_THRESHOLD="2"       # 质量拒收阈值
export QCC_CREDIT_RATING_THRESHOLD="B" # 信用评级阈值
```

### 验证配置

```bash
python3 -c "
from scripts.qcc_mcp_connector import QccMcpConnector
c = QccMcpConnector()
print('✅ MCP配置成功' if c.api_key else '❌ MCP未配置')
"
```

---

## 常见问题

### Q: 没有QCC MCP Key可以使用吗？

**A:** 可以，但功能受限。没有Key时：
- ❌ 无法查询中国企业风险数据
- ✅ 仍可使用基础评估框架
- ✅ 可手动输入数据进行评估

### Q: 支持非中国企业吗？

**A:** 支持，但数据来源不同：
- 中国企业 → QCC MCP（推荐）
- 海外企业 → 原版Skill（Companies House等）

### Q: 数据更新频率？

**A:**
- 司法执行：实时
- 经营异常：每日
- 信用评级：每月
- 建议评估频率：Strategic季度/Tactical半年/Commodity年度

### Q: 如何申请QCC MCP Key？

**A:**
1. 访问 https://mcp.qcc.com
2. 企业注册认证
3. 申请MCP服务
4. 获取API Key
5. 设置环境变量

### Q: 数据安全吗？

**A:**
- 所有数据来自企查查官方
- 传输使用HTTPS加密
- 仅存储在本地环境变量
- 不上传至第三方

---

## 贡献指南

### 提交Issue

- Bug反馈
- 功能建议
- 文档改进

### 提交PR

1. Fork本仓库
2. 创建feature分支
3. 提交修改
4. 创建Pull Request

### 代码规范

- Python代码遵循PEP 8
- SKILL文档使用Markdown
- 新增功能需包含测试用例

---

## 项目结构

```
supply-chain-qcc/
├── README.md                           # 本文件
├── LICENSE                             # Apache 2.0
├── install_qcc_mcp_supply_chain.sh     # 一键安装脚本
├── example.py                          # 使用示例
│
├── skills/
│   ├── vendor-assessment/
│   │   └── SKILL.md                    # 供应商评估Skill
│   └── supplier-risk/
│       └── SKILL.md                    # 风险监控Skill
│
├── scripts/
│   └── qcc_mcp_connector.py            # QCC MCP连接器
│
└── docs/
    ├── CHANGES.md                      # 变更日志
    ├── OPTIMIZATION_SUMMARY.md         # 优化总结
    ├── SUPPLY_CHAIN_RISKS.md           # 风险设计原理
    └── QUICK_REFERENCE.md              # 快速参考
```

---

## 相关链接

- [企查查MCP官网](https://mcp.qcc.com)
- [Claude Code文档](https://docs.anthropic.com/en/docs/claude-code)
- [原版Supply Chain Plugin](https://github.com/panaversity/agentfactory-business-plugins)

---

## 许可证

Apache License 2.0

基于 [Panaversity/agentfactory-business-plugins](https://github.com/panaversity/agentfactory-business-plugins) 构建

---

## 致谢

- 原版作者 Panaversity 的优秀供应链技能框架
- [企查查MCP](https://mcp.qcc.com) - Agent-Native企业数据基座
- [Anthropic](https://anthropic.com) 的 Claude Code

---

<div align="center">

**让供应商评估从"数据盲区"走向"全面透视"** 🔍

如果这个项目对您有帮助，请 ⭐ Star 支持！

[提交Issue](https://github.com/your-repo/supply-chain-qcc/issues) · [贡献代码](https://github.com/your-repo/supply-chain-qcc/pulls)

</div>
