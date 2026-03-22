# 🔍 Legal Assistant Skills Pro

> **合同审核增强版** - 集成企查查MCP，实现AI驱动的企业风险智能识别

[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-QCC%20企查查-orange.svg)](https://mcp.qcc.com)
[![Claude](https://img.shields.io/badge/Claude%20Code-Compatible-purple.svg)](https://claude.ai)

---

## ✨ 一句话介绍

**在原版合同审核基础上，增加企业工商信息实时核验和18类风险自动排查，让AI不只是"读"合同，更能"懂"风险。**

---

## 🎯 解决什么痛点

| 场景 | 传统方式 | 本方案 |
|------|---------|--------|
| 甲方公司是否存在？ | 人工查询/百度 | **API实时核验** |
| 对方有无失信记录？ | 上企查查逐个查 | **18类风险自动扫描** |
| 合同主体信息错误 | 肉眼比对 | **智能批注提醒** |
| 风险条款识别 | 依赖律师经验 | **结构化风险报告** |

---

## 🚀 30秒快速体验

```bash
# 1. 安装（一键脚本）
bash <(curl -sL https://raw.githubusercontent.com/duhu2000/legal-assistant-skills/main/install_qcc_mcp.sh)

# 2. 配置API Key（从 https://mcp.qcc.com 申请）
export QCC_MCP_API_KEY="your_key_here"

# 3. 在Claude Code中使用
# 请审核这份合同: /path/to/contract.docx
```

**Done!** 系统自动完成：
- ✅ 提取甲方/乙方等合同主体
- ✅ 实时核验企业工商信息
- ✅ 扫描18类经营/司法/税务风险
- ✅ 生成带风险标记的审核版合同

---

## 📊 功能对比：原版 vs 增强版

### 核心增强

```
原版: 合同文本审核 → 生成批注
        ↓
增强版: 合同文本审核
        ↓
    [自动提取合同主体]
        ↓
    [企查查MCP实时核验]
        ↓
    [18类风险自动扫描]
        ↓
    生成批注 + 主体核验批注 + 风险预警批注
```

### 详细对比

| 能力 | 原版 | 本增强版 |
|------|------|---------|
| **合同文本审核** | ✅ 支持 | ✅ 支持 |
| **企业信息核验** | ❌ 不支持 | 🔥 **自动核验** |
| **司法风险扫描** | ❌ 不支持 | 🔥 **失信/被执行/限高** |
| **经营风险扫描** | ❌ 不支持 | 🔥 **异常/违法/注销** |
| **财产风险扫描** | ❌ 不支持 | 🔥 **股权冻结/出质** |
| **税务风险扫描** | ❌ 不支持 | 🔥 **欠税/非正常户** |
| **破产风险扫描** | ❌ 不支持 | 🔥 **破产/清算** |
| **智能风险批注** | ❌ 不支持 | 🔥 **自动生成** |
| **降级兼容** | - | ✅ **无API Key自动降级** |

---

## 🔥 18类风险扫描清单

### ⚠️ 司法执行类（高风险）
- 失信信息（老赖）
- 被执行人
- 限制高消费
- 终本案件
- 司法拍卖

### ⚠️ 经营异常类（中风险）
- 经营异常
- 严重违法
- 注销备案
- 简易注销

### ⚠️ 财产受限类（中风险）
- 股权冻结
- 股权出质
- 动产抵押

### ⚠️ 税务违法类（中风险）
- 税务非正常户
- 欠税公告
- 税收违法

### ⚠️ 环保/行政处罚类
- 环保处罚
- 行政处罚

### ⚠️ 破产清算类（高风险）
- 破产重整
- 清算信息

---

## 💡 典型应用场景

### 场景1：采购合同审核
```
AI: 检测到甲方「XXX科技有限公司」
    ↓
MCP: 核验结果：该企业于2024-03-15被列入经营异常名录
    ↓
批注: 🔴 高风险-经营异常
      建议：要求对方提供情况说明或更换供应商
```

### 场景2：服务合同签署前
```
AI: 检测到乙方「XXX建设集团」
    ↓
MCP: 风险扫描：发现3条失信记录，2条被执行人记录
    ↓
批注: 🔴 高风险-司法执行
      建议：立即终止合作谈判
```

### 场景3：投资尽职调查
```
AI: 扫描目标公司风险
    ↓
MCP: 18类风险全扫描
    ↓
报告: 生成详细风险报告 + 风险矩阵
```

---

## 🛠️ 技术架构

```
┌─────────────────────────────────────────┐
│         Claude Code / Skill             │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      Contract Review Workflow           │
│  ┌─────────┐  ┌─────────┐  ┌────────┐  │
│  │  合同   │→│  主体   │→│  风险  │  │
│  │  解析   │  │  提取   │  │  扫描  │  │
│  └─────────┘  └────┬────┘  └────┬───┘  │
│                    │            │      │
│                    ▼            ▼      │
│            ┌─────────────────────┐     │
│            │  QCC 企查查MCP      │     │
│            │  (4服务/65工具)     │     │
│            └─────────────────────┘     │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      智能批注生成 + DOCX输出            │
└─────────────────────────────────────────┘
```

---

## 📁 项目结构

```
legal-assistant-skills/
├── contract-review/                 # 合同审核核心
│   ├── scripts/
│   │   ├── qcc_mcp_client.py       # ⭐ MCP客户端（新增）
│   │   ├── workflow.py             # ⭐ 集成MCP流程（增强）
│   │   └── ...                     # 其他脚本
│   ├── README_QCC_MCP.md           # MCP详细文档
│   └── SKILL.md                    # 技能定义
├── install_qcc_mcp.sh              # ⭐ 一键安装脚本
└── README.md                       # 本文件
```

---

## 🔧 进阶配置

### 手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/duhu2000/legal-assistant-skills.git

# 2. 复制到Claude技能目录
cp -r legal-assistant-skills/contract-review ~/.claude/skills/

# 3. 设置环境变量
export QCC_MCP_API_KEY="your_api_key"
```

### 在代码中使用

```python
from scripts.workflow import ContractReviewWorkflow

# 基础使用
workflow = ContractReviewWorkflow("合同.docx")

# 启用MCP核验（推荐）
workflow = ContractReviewWorkflow(
    "合同.docx",
    enable_mcp_verification=True
)

# 完整流程
workflow.run_full_workflow(comments, "合同_审核版.docx")
```

### 单独使用MCP客户端

```python
from scripts.qcc_mcp_client import QccMcpClient

client = QccMcpClient()

# 核验企业
info = client.verify_company("企查查科技股份有限公司")

# 风险排查
risks = client.check_company_risk("企查查科技股份有限公司")
```

---

## 🎓 工作原理

### Step 1: 合同解析
- 提取合同文本
- 识别甲方/乙方/买方/卖方等主体

### Step 2: 企业核验（MCP）
- 调用企查查MCP服务
- 返回工商注册信息

### Step 3: 风险扫描（MCP）
- 18类风险并行查询
- 汇总风险等级

### Step 4: 批注生成
- 核验批注：企业信息确认
- 风险批注：风险提示+建议

### Step 5: 文档输出
- 审核版合同（带批注）
- 合同概要
- 风险报告

---

## 🌟 为什么选择这个版本

| 优势 | 说明 |
|------|------|
| **数据权威** | 企查查官方数据，非爬虫 |
| **实时核验** | API实时查询，非缓存数据 |
| **风险全面** | 18类风险，覆盖司法/经营/税务 |
| **零侵入** | 可选启用，不影响原有功能 |
| **易于集成** | 一行代码启用MCP |

---

## 📈 未来规划

- [ ] 支持批量合同处理
- [ ] 增加企业关联图谱分析
- [ ] 集成更多MCP服务（知识产权、招投标等）
- [ ] Web UI可视化界面
- [ ] API服务化部署

---

## 🤝 贡献与反馈

### 提交Issue
- Bug反馈
- 功能建议
- 使用问题

### 提交PR
- Fork本仓库
- 创建feature分支
- 提交PR

### 联系方式
- GitHub Issues
- Email: duhu@qcc.com

---

## 📜 许可证

Apache License 2.0

基于 [zh-xx/legal-assistant-skills](https://github.com/zh-xx/legal-assistant-skills) 构建

---

## 🙏 致谢

- 原版作者 [zh-xx](https://github.com/zh-xx) 的优秀基础
- [企查查](https://www.qcc.com) 提供的企业数据服务
- [Anthropic](https://anthropic.com) 的 Claude Code

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star！**

[🐛 提交Bug](https://github.com/duhu2000/legal-assistant-skills/issues) · [💡 功能建议](https://github.com/duhu2000/legal-assistant-skills/issues) · [⭐ Star](https://github.com/duhu2000/legal-assistant-skills)

</div>
