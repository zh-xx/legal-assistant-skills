# 🔍 Legal Assistant Skills Pro

> **合同审核增强版** - 集成企查查MCP，为AI合同审核注入真实商业世界的确定性

[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-QCC%20企查查-orange.svg)](https://mcp.qcc.com)
[![Claude](https://img.shields.io/badge/Claude%20Code-Compatible-purple.svg)](https://claude.ai)

---

## ✨ 一句话介绍

**不只是合同文本审核，更是企业主体的「实时尽调」。**
**接入企查查MCP，让AI审核合同时拥有资深合规专家的商业直觉。**

---

## 🎯 解决什么痛点

| 场景 | 传统方式 | **MCP原生方案** |
|------|---------|----------------|
| 甲方公司是否存在？ | 人工查询/百度/爬虫 | **MCP实时核验**（实体强锚定，零幻觉） |
| 对方有无失信记录？ | 上企查查逐个查 | **18类风险自动扫描**（语义即用） |
| 合同主体信息错误 | 肉眼比对 | **智能批注提醒**（确定性决策） |
| 风险条款识别 | 依赖律师经验 | **结构化风险报告**（合规可审计） |
| Token消耗爆炸 | 万字冗余数据 | **上下文脱水**（节省96%成本） |

---

## 🚀 为什么是MCP，而不是API？

### ❌ 传统API方案的问题

```
传统API调用：
├─ 返回数万字JSON → Token瞬间爆炸
├─ 空数据返回[] → LLM陷入"无数据or查询失败"的自我怀疑
├─ 名称相似企业 → 张冠李戴致命错误（如错认乐视网）
└─ 结果：AI不敢下定论，人工复核成本高
```

### ✅ 企查查MCP方案的优势

基于**Agent-Native**理念打造的企业数据基座：

| 核心能力 | 说明 |
|---------|------|
| **🛡️ 实体强锚定** | 内置"二段式核验"协议，强制验证统一社会信用代码，物理层面切断名称幻觉 |
| **🗜️ 极致上下文管理** | 参数下推+智能摘要，Token开销直降96%，阻断千字级废话流 |
| **🚦 强语义负向防御** | 空数据转化为强语义状态码（如"核验通过"），为AI颁发确定的"合规通行证" |
| **🔒 合规可审计** | 所有核验留痕，满足法务审计要求 |

---

## ⚡ 30秒快速体验

### 前置准备

```bash
# 1. 安装Python依赖（只需一次）
pip3 install requests

# 2. 配置MCP Key（从 https://mcp.qcc.com 申请）
# 方式一：临时设置（当前终端有效）
export QCC_MCP_API_KEY="your_key_here"

# 方式二：永久设置（推荐）
# 添加到shell配置文件，这样无论从哪启动Claude Code都能读取到
echo 'export QCC_MCP_API_KEY="your_key_here"' >> ~/.zshrc
source ~/.zshrc
# 如果是Bash用户，请使用 ~/.bashrc
```

**注意**：如果使用方式一（临时设置），必须在同一终端窗口中启动Claude Code，否则环境变量不会生效。强烈建议使用方式二（永久设置）。

### 一键安装

```bash
# 3. 运行安装脚本
bash <(curl -sL https://raw.githubusercontent.com/duhu2000/legal-assistant-skills/main/install_qcc_mcp.sh)
```

### 开始使用

```bash
# 4. 在Claude Code中
# 请审核这份合同: /path/to/contract.docx
```

**Done!** 系统自动完成：
- ✅ 提取甲方/乙方等合同主体
- ✅ MCP实时核验企业工商信息
- ✅ 18类经营/司法/税务风险扫描
- ✅ 生成带风险标记的审核版合同

---

## 📊 功能对比：原版 vs MCP增强版

### 核心增强

```
原版: 合同文本审核 → 生成批注
        ↓
MCP增强版: 合同文本审核
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

| 能力 | 原版 | MCP增强版 |
|------|------|----------|
| **合同文本审核** | ✅ 支持 | ✅ 支持 |
| **企业信息核验** | ❌ 不支持 | 🔥 **MCP实时核验** |
| **司法风险扫描** | ❌ 不支持 | 🔥 **失信/被执行/限高** |
| **经营风险扫描** | ❌ 不支持 | 🔥 **异常/违法/注销** |
| **财产风险扫描** | ❌ 不支持 | 🔥 **股权冻结/出质** |
| **税务风险扫描** | ❌ 不支持 | 🔥 **欠税/非正常户** |
| **破产风险扫描** | ❌ 不支持 | 🔥 **破产/清算** |
| **智能风险批注** | ❌ 不支持 | 🔥 **自动生成** |
| **降级兼容** | - | ✅ **无MCP Key自动降级** |

---

## 🔥 18类风险扫描清单（MCP四大Server覆盖）

### ⚠️ 司法执行类（风控大脑Server）
- 失信信息（老赖）
- 被执行人
- 限制高消费
- 终本案件
- 司法拍卖

### ⚠️ 经营异常类（企业基座Server）
- 经营异常
- 严重违法
- 注销备案
- 简易注销

### ⚠️ 财产受限类（企业基座Server）
- 股权冻结
- 股权出质
- 动产抵押

### ⚠️ 税务违法类（企业基座Server）
- 税务非正常户
- 欠税公告
- 税收违法

### ⚠️ 环保/行政处罚类（风控大脑Server）
- 环保处罚
- 行政处罚

### ⚠️ 破产清算类（风控大脑Server）
- 破产重整
- 清算信息

---

## 💡 典型应用场景

### 场景1：采购合同审核
```
AI: 检测到甲方「XXX科技有限公司」
    ↓
MCP: 核验结果：该企业于2024-03-15被列入经营异常名录
     （实体锚定：统一社会信用代码9132***********确认无误）
    ↓
批注: 🔴 高风险-经营异常
      建议：要求对方提供情况说明或更换供应商
```

### 场景2：服务合同签署前
```
AI: 检测到乙方「XXX建设集团」
    ↓
MCP: 风险扫描：发现3条失信记录，2条被执行人记录
     （语义确认：确定性的"存在风险"状态，非空数据）
    ↓
批注: 🔴 高风险-司法执行
      建议：立即终止合作谈判
```

### 场景3：投资尽职调查
```
AI: 扫描目标公司风险
    ↓
MCP: 18类风险全扫描（脱水后仅返回关键摘要）
    ↓
报告: 生成详细风险报告 + 风险矩阵 + 影响路径图
```

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
│      Contract Review Workflow           │
│  ┌─────────┐  ┌─────────┐  ┌────────┐  │
│  │  合同   │→│  主体   │→│  风险  │  │
│  │  解析   │  │  提取   │  │  扫描  │  │
│  └─────────┘  └────┬────┘  └────┬───┘  │
│                    │            │      │
│                    ▼            ▼      │
│         ┌─────────────────────┐        │
│         │  企查查 MCP Server  │        │
│         │  • 企业基座 Server  │        │
│         │  • 风控大脑 Server  │        │
│         │  • 知产引擎 Server  │        │
│         │  • 经营罗盘 Server  │        │
│         │  (65个工具/4大维度) │        │
│         └─────────────────────┘        │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│   智能批注生成 + 合同概要 + DOCX输出    │
└─────────────────────────────────────────┘
```

---

## 🎓 MCP工作原理：Agent-Native设计

### Step 1: 合同解析
- 提取合同文本
- 识别甲方/乙方/买方/卖方等主体

### Step 2: 企业核验（MCP实体锚定）
```
传统API: "华为技术有限公司" → 可能返回多个相似名称
MCP方案: "华为技术有限公司"
         → 强制匹配统一社会信用代码914403001038138210
         → 返回"实体锚定确认：唯一有效主体"
```

### Step 3: 风险扫描（MCP语义防御）
```
传统API: 无失信记录 → 返回 []
         → LLM困惑："真没有？还是查失败了？"
MCP方案: 无失信记录 → 返回 "核验通过：未发现失信信息"
         → LLM确定："合规状态安全，可继续执行"
```

### Step 4: 上下文脱水（MCP Token优化）
```
传统API: 返回30000字全量数据 → Token爆炸
MCP方案: 智能摘要+按需索取 → 仅1000字关键信息
         → 成本降低96%，决策效率提升
```

### Step 5: 批注生成
- 核验批注：企业信息确认（含实体锚定标识）
- 风险批注：风险提示+法律建议
- 审计留痕：所有核验可追溯

---

## 📁 项目结构

```
legal-assistant-skills/
├── contract-review/                 # 合同审核核心
│   ├── scripts/
│   │   ├── qcc_mcp_client.py       # ⭐ MCP客户端（Agent-Native）
│   │   ├── workflow.py             # ⭐ MCP集成流程
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
export QCC_MCP_API_KEY="your_mcp_key"
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

# 核验企业（带实体锚定）
info = client.verify_company("企查查科技股份有限公司")

# 风险排查（语义化结果）
risks = client.check_company_risk("企查查科技股份有限公司")
```

---

## 🌟 为什么选择MCP原生方案

| 优势 | 传统API | 企查查MCP |
|------|---------|----------|
| **数据权威** | 企查查官方数据 | ✅ 企查查官方数据 |
| **实体锚定** | ❌ 名称匹配易出错 | ✅ **统一社会信用代码强制验证** |
| **语义即用** | ❌ 原始JSON需解析 | ✅ **LLM友好的自然语言输出** |
| **零幻觉** | ❌ 张冠李戴风险 | ✅ **二段式核验协议** |
| **Token成本** | ❌ 万字冗余数据 | ✅ **脱水后降低96%** |
| **确定性决策** | ❌ 空数据无法判断 | ✅ **强语义状态码** |
| **合规审计** | ❌ 无留痕 | ✅ **全链路可追溯** |

---

## 📈 未来规划

- [ ] 支持批量合同处理
- [ ] 增加企业关联图谱分析（MCP股权穿透）
- [ ] 集成更多MCP Server（知识产权、招投标等）
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

基于 [zh-xx/legal-assistant-skills](https://github.com/zh-xx/legal-assistant-skills) 构建

---

## 🙏 致谢

- 原版作者 [zh-xx](https://github.com/zh-xx) 的优秀基础
- [企查查MCP](https://mcp.qcc.com) - 首个Agent-Native企业数据基座
- [Anthropic](https://anthropic.com) 的 Claude Code

---

<div align="center">

**告别JSON搬运工，拥抱Agent原生时代。**

**如果这个项目对你有帮助，请给个 ⭐ Star！**

[🐛 提交Bug](https://github.com/duhu2000/legal-assistant-skills/issues) · [💡 功能建议](https://github.com/duhu2000/legal-assistant-skills/issues) · [⭐ Star](https://github.com/duhu2000/legal-assistant-skills)

</div>
