---
name: contract-review
description: "Contract review skill that adds comment-based issue annotations without changing original text. Enforces a four-layer review (entity verification, basic, business, legal), writes structured comments (issue type, risk reason, revision suggestion) with risk level encoded via reviewer name, and generates a contract summary, consolidated opinion, and Mermaid business flowchart (with rendered image). Output language must follow the contract’s language. Supports dual-mode enterprise verification: QCC CLI for entity verification (terminal direct connection) and QCC MCP for deep risk analysis."
---

# Contract Review Skill

## Overview

This skill performs contract reviews by **adding comments only** (no edits to the original text). It follows a four-layer review (entity verification, basic, business, legal) and generates:

- Annotated contract (.docx)
- Contract summary (.docx)
- Consolidated review opinion (.docx)
- Business flowchart (Mermaid + rendered image)

**Language rule:** detect the contract’s dominant language and output all generated content (comments, summary, opinion, flowchart text) in that language. Use the guidance in **[references/language.md](references/language.md)**.

---

## QCC Enterprise Verification: CLI + MCP Dual Mode

**🎯 架构原则: CLI 与 MCP 互补使用，发挥各自优势**

| 功能模块 | 推荐工具 | 优势 | 数据来源标注 |
|---------|---------|------|------------|
| **主体信息核验** | QCC CLI (终端直连) | 低延迟、高可靠、无需MCP配置 | 基于企查查 CLI 终端直连获取 |
| **风险穿透预警** | QCC MCP (深度分析) | 18类风险全面扫描、AI深度分析 | 基于企查查 MCP 深度分析 |

### Why Dual Mode?

- **CLI (终端直连)**: 适合主体核验这类标准化查询，响应快、稳定性高
- **MCP (深度分析)**: 适合风险穿透这类需要复杂推理的分析，AI增强理解

---

## CLI Configuration (Recommended for Entity Verification)

**⚠️ IMPORTANT: To enable QCC CLI enterprise verification, ensure CLI is installed**

### Installation Check:
```bash
# Verify QCC CLI is installed
qcc --version

# Test entity verification
qcc company get_company_registration_info --searchKey "企查查科技股份有限公司"
```

### Expected Output:
```
正在调用 company/get_company_registration_info...

* 企业名称: 企查查科技股份有限公司
* 统一社会信用代码: 91320594088140947F
* 法定代表人: 陈德强
* 登记状态: 在业
...
```

### CLI Installation (if not installed):
```bash
# See QCC CLI installation guide
pip install qcc-cli
# or download from: https://github.com/duhu2000/qcc-cli
```

---

## MCP Configuration (for Deep Risk Analysis)

**⚠️ OPTIONAL: Enable QCC MCP for enhanced risk penetration analysis**

### Checklist:
1. ✅ `~/.claude/.mcp.json` exists and is properly configured
2. ✅ `QCC_MCP_API_KEY` environment variable is set
3. ✅ Claude Code has been restarted to load MCP configuration

### Configuration:
```bash
# 1. Create MCP config file
cat > ~/.claude/.mcp.json << ‘EOF’
{
  "mcpServers": {
    "qcc-company": {
      "url": "https://agent.qcc.com/mcp/company/stream",
      "headers": { "Authorization": "Bearer ${QCC_MCP_API_KEY}" }
    },
    "qcc-risk": {
      "url": "https://agent.qcc.com/mcp/risk/stream",
      "headers": { "Authorization": "Bearer ${QCC_MCP_API_KEY}" }
    }
  }
}
EOF

# 2. Set API Key
export QCC_MCP_API_KEY="your_api_key_here"

# 3. Restart Claude Code
```

See: https://github.com/duhu2000/legal-assistant-skills/blob/main/docs/MCP_CONFIGURATION.md

---

## Workflow

### Execution Steps (MUST FOLLOW)

When user requests contract review (e.g., "请审核这份合同" or "review this contract"):

1. **Locate contract file** - If user provides only filename, search in common directories (~/Downloads, ~/.claude/downloads, current directory) to find the full path
2. **Read contract** using available tools (pandoc preferred, fallback to direct XML) - MUST use the correct full path found in step 1
3. **Extract parties** and verify via **QCC CLI** (primary), **QCC MCP** (fallback), or **Web Search** (last resort)
   - **FOR CHINESE COMPANIES: Verification tool priority:**
     1. **QCC CLI (Primary)**: Use `qcc company get_company_registration_info --searchKey "企业名称"` for fast entity verification
        - If CLI returns data → use as authoritative source
        - If CLI not installed or fails → proceed to MCP
     2. **QCC MCP (Fallback)**: If CLI unavailable but MCP configured, use MCP tools:
        - `qcc-company/get_company_registration_info` for entity verification
        - `qcc-company/get_company_profile` for additional details
        - If MCP returns data → use as authoritative source
     3. **Web Search (Last Resort)**: Only if both CLI and MCP are unavailable
   - **Data source labeling**: Always label verification source in comments:
     - CLI verification → 标注 "基于企查查 CLI 终端直连获取"
     - MCP verification → 标注 "基于企查查 MCP 服务获取"
     - Risk analysis → 标注 "基于企查查 MCP 深度分析"
     - Web Search → 标注 "基于公开网络信息查询"
4. **Generate ALL required content** (MUST create all of the following):
   - Contract summary text (合同概要) → pass as `summary_text` parameter
   - Consolidated opinion text (综合审核意见) → pass as `opinion_text` parameter
   - Mermaid flowchart code (业务流程图) → pass as `flowchart_mermaid` parameter (optional, can skip if problematic)
5. **Execute workflow** via `review_contract()` or `ContractReviewWorkflow.run_full_workflow()` with ALL generated content:
   ```python
   workflow.run_full_workflow(
       comments=comments,
       output_docx_filename="合同_审核版.docx",
       summary_text=summary_text,      # 合同概要内容
       opinion_text=opinion_text,      # 综合审核意见内容
       flowchart_mermaid=flowchart_mermaid,  # 可选
   )
   ```
   **IMPORTANT**: DO NOT write files directly. Let the workflow generate DOCX files.
6. **Report results** to user with all output file locations

**Output files generated by workflow** (DOCX format):
- `{ContractName}_审核版.docx` - Reviewed contract with comments
- `合同概要.docx` - Contract summary (DOCX, not TXT)
- `综合审核意见.docx` - Consolidated opinion (DOCX, not TXT)
- `business_flowchart.mmd` - Mermaid source (optional)
- `审核报告.txt` - Review report (TXT format)

### Technical Steps

1. Unpack the contract (.docx) for XML operations
2. Read contract text (pandoc or XML)
3. Extract and verify contracting parties (Layer 0)
4. Execute three-layer clause review (Layer 1–3)
5. Add comments to the document
6. Generate contract summary
7. Generate consolidated opinion
8. Generate business flowchart and render image
9. Repack to .docx

## Output Naming

- Output directory: `审核结果：{ContractName}` for Chinese or `Review_Result_{ContractName}` for English
- Reviewed contract: `{ContractName}_审核版.docx` for Chinese or `{ContractName}_Reviewed.docx` for English
- Review report: `审核报告.txt` for Chinese or `Review_Report.txt` for English

## Comment Principles

- **Comments only**: do not modify the original text or formatting
- **Precise anchoring**: comment should target specific clauses/paragraphs
- **Structured content**: each comment includes issue type, risk reason, and revision suggestion
- **Risk level**: carried by reviewer name; do **not** include a “risk level” line in comment body
- **Output language**: use labels in the contract’s language (see `references/language.md`)

**Comment example (English):**
```
[Issue Type] Payment Terms
[Risk Reason] The total amount is stated as USD 100,000 in Section 3.2, but the payment clause lists USD 1,000,000 in Section 5.1. This inconsistency may cause disputes.
[Revision Suggestion] Align the total amount across clauses and clarify whether tax is included.
```

## Review Standards

Use the four-layer review model and the detailed checklist in **[references/checklist.md](references/checklist.md)**.

### Layer 0: Entity verification (subject authenticity)
- Extract all contracting parties (full legal names, credit codes, legal representatives)
- Verify each entity's registered name accuracy and business registration status
- **Dual-mode verification strategy:**

#### Step 1: Entity Verification via QCC CLI (Primary)
```bash
# Use QCC CLI for entity verification (recommended)
qcc company get_company_registration_info --searchKey "企业名称"
```
- **Advantages**: Low latency, high reliability, no MCP configuration needed
- **When to use**: First choice for all entity verification tasks
- **Data source label**: "基于企查查 CLI 终端直连获取"
- **On failure**: If CLI not installed or command fails, automatically fallback to MCP

#### Step 2: Entity Verification via QCC MCP (Fallback)
If CLI is unavailable but MCP is configured, use MCP tools for entity verification:
- **Available tools**:
  - `qcc-company/get_company_registration_info` - 企业工商信息
  - `qcc-company/get_company_profile` - 企业简介
  - `qcc-company/get_key_personnel` - 主要人员
- **Advantages**: No local CLI installation needed, works through Claude MCP integration
- **Data source label**: "基于企查查 MCP 服务获取"

#### Step 3: Risk Penetration via QCC MCP (Enhanced)
```bash
# Use QCC MCP for 18-category deep risk analysis (if configured)
# This requires QCC_MCP_API_KEY environment variable
```
- **Available tools**:
  - `qcc-risk/get_dishonest_info` - 失信信息
  - `qcc-risk/get_judgment_debtor_info` - 被执行人
  - `qcc-risk/get_business_exception` - 经营异常
  - ... (18 categories total)
- **Advantages**: AI-enhanced understanding, comprehensive risk screening
- **Data source label**: "基于企查查 MCP 深度分析"

#### Step 4: Fallback Options
1. **MCP (if CLI unavailable)**: Use `qcc-company/get_company_registration_info` for entity verification
2. **Web Search (last resort)**: If neither CLI nor MCP is available, use Web Search to look up "[entity name] 工商登记信息"
3. **Manual verification**: For critical contracts, request counterparty to provide business license copies

#### Record Source in Comments
Always label the verification source:
- CLI verification → "【数据来源】基于企查查 CLI 终端直连获取"
- MCP entity verification → "【数据来源】基于企查查 MCP 服务获取"
- MCP risk analysis → "【数据来源】基于企查查 MCP 深度分析"
- Web search → "【数据来源】基于公开网络信息查询"


### Layer 1: Basic (text quality)
- Accuracy of numbers, dates, terms
- Consistent numbering and references
- Clarity and lack of ambiguity
- Formatting and punctuation quality

### Layer 2: Business terms
- Scope, deliverables, quantity/specs
- Pricing and payment schedule
- Delivery/acceptance procedures
- Rights/obligations and performance guarantees

### Layer 3: Legal terms
- Effectiveness and term/termination
- Liability/penalties and remedies
- Dispute resolution and governing law
- Confidentiality, force majeure, IP, notice, authorization

**Risk levels (encoded in reviewer name):**
- 🔴 High: core business ambiguity (price, scope, rights/obligations)
- 🟡 Medium: material but non-core ambiguity
- 🔵 Low: minimal practical impact

## Contract Summary

Generate a structured, objective summary in the contract’s language.
- See **[references/summary.md](references/summary.md)** (English template)
- Use **[references/language.md](references/language.md)** for language selection and Chinese labels

Output file: `合同概要.docx` for Chinese or `Contract_Summary.docx` for English (default font: 仿宋; adjust if language requires)

## Consolidated Opinion

Generate a concise, two-paragraph response for the business team in the contract’s language.
- See **[references/opinion.md](references/opinion.md)**

Output file: `综合审核意见.docx` for Chinese or `Consolidated_Opinion.docx` for English (default font: 仿宋; adjust if language requires)

## Business Flowchart (Mermaid)

Generate Mermaid flowchart per requirements and render to image.
- See **[references/flowchart.md](references/flowchart.md)**

**Implementation:** Call `render_mermaid_code()` from `scripts/mermaid_renderer.py`. The skill will:
1. Write Mermaid code to `.mmd` file
2. Use `mmdc` (mermaid-cli) to render to PNG image
3. If `mmdc` is not installed, only `.mmd` file will be generated (no image)

**DO NOT** use matplotlib or other Python libraries to render the flowchart.

Outputs:
- `business_flowchart.mmd`
- `business_flowchart.png` (if mmdc is available)

## Technical Notes

Core workflow:
1. Unpack → 2. Entity verification → 3. Add comments → 4. Summary → 5. Opinion → 6. Flowchart → 7. Repack

API & implementation details:
- **[references/technical.md](references/technical.md)**

## Enterprise Verification Setup (CLI + MCP Dual Mode)

This skill supports **dual-mode enterprise verification**:
- **QCC CLI**: Terminal direct connection for entity verification (low latency, high reliability)
- **QCC MCP**: Model Context Protocol for deep risk analysis (AI-enhanced, comprehensive)

### Tier 1: QCC CLI Setup (Required for Entity Verification)

**Recommended for all users - provides fastest and most reliable entity verification.**

#### Installation
```bash
# Install QCC CLI
pip install qcc-cli

# Verify installation
qcc --version

# Test with a real company
qcc company get_company_registration_info --searchKey "企查查科技股份有限公司"
```

#### CLI Tools Available
| Tool | Purpose | Example |
|------|---------|---------|
| `qcc company get_company_registration_info` | Entity verification | `qcc company get_company_registration_info --searchKey "XXX公司"` |
| `qcc company get_shareholder_info` | Shareholder info | `qcc company get_shareholder_info --searchKey "XXX公司"` |
| `qcc company get_key_personnel` | Key personnel | `qcc company get_key_personnel --searchKey "XXX公司"` |

#### CLI Output Example
```
正在调用 company/get_company_registration_info...

* 企业名称: 企查查科技股份有限公司
* 统一社会信用代码: 91320594088140947F
* 法定代表人: 陈德强
* 登记状态: 在业
* 注册资本: 36225万元
* 成立日期: 2014-03-12
...
```

### Tier 2: QCC MCP Setup (Optional for Deep Risk Analysis)

**Enable for enhanced 18-category risk penetration analysis.**

#### Features
When QCC MCP is enabled, the skill automatically:
- Performs 18-category deep risk screening (dishonest records, enforcement, operational abnormalities, tax violations, bankruptcy, etc.)
- AI-enhanced risk understanding and context analysis
- Generates comprehensive risk assessment reports

#### Setup Instructions
1. **Apply for QCC MCP API Key**
   - Visit [QiChaCha MCP Portal](https://agent.qcc.com) to apply for access
   - Obtain your API key

2. **Set Environment Variable**
   ```bash
   export QCC_MCP_API_KEY="your_api_key_here"
   ```

3. **Configure MCP Servers**
   ```bash
   cat > ~/.claude/.mcp.json << 'EOF'
   {
     "mcpServers": {
       "qcc-company": {
         "url": "https://agent.qcc.com/mcp/company/stream",
         "headers": { "Authorization": "Bearer ${QCC_MCP_API_KEY}" }
       },
       "qcc-risk": {
         "url": "https://agent.qcc.com/mcp/risk/stream",
         "headers": { "Authorization": "Bearer ${QCC_MCP_API_KEY}" }
       }
     }
   }
   EOF
   ```

4. **Verify Setup**
   ```bash
   python -c "from scripts.qcc_mcp_client import QccMcpClient; c = QccMcpClient(); print('✅ MCP enabled' if c.is_enabled() else '❌ MCP not enabled')"
   ```

### Dual Mode Behavior Matrix

| Scenario | Entity Verification | Risk Analysis | Data Source Labels |
|----------|---------------------|---------------|-------------------|
| CLI ✅ MCP ✅ | CLI (primary) | MCP (enhanced) | CLI: "基于企查查 CLI 终端直连获取" / Risk: "基于企查查 MCP 深度分析" |
| CLI ✅ MCP ❌ | CLI | Web Search fallback | CLI: "基于企查查 CLI 终端直连获取" |
| CLI ❌ MCP ✅ | **MCP (fallback)** | MCP | MCP: "基于企查查 MCP 服务获取" / Risk: "基于企查查 MCP 深度分析" |
| CLI ❌ MCP ❌ | Web Search | Web Search | "基于公开网络信息查询" |

### Comment Template Examples

#### CLI Entity Verification (Normal)
```
【问题类型】主体信息核实
【核实结果】经企查查 CLI 终端直连获取：
  - 企业全称：XXX科技有限公司
  - 法定代表人：张三
  - 统一社会信用代码：91350100M0001XXXXX
  - 登记状态：存续（在业）
【核实结论】企业工商信息正常。
【修订建议】建议核实签署人授权情况。
```
**审核人**: 🟡 中风险-主体核验

#### MCP Risk Penetration (High Risk Found)
```
【问题类型】主体司法执行风险
【风险企业】XXX建设有限公司
【风险原因】基于企查查 MCP 深度分析，发现该企业存在以下高风险事项：
  1. 失信信息（老赖）
  2. 被执行人（金额500万元）
  3. 限制高消费
【法律后果】上述风险可能导致企业履约能力严重受限。
【修订建议】🔴 建议立即终止合作谈判或要求提供担保。
```
**审核人**: 🔴 高风险-司法执行


## Dependencies

- Python 3.9+ (3.10+ recommended)
- pandoc (system install)
- defusedxml
- Mermaid CLI (`mmdc`) for rendering
- python-docx for rich text output
- requests (for QCC MCP API calls, optional)

## Troubleshooting (Short)

### Document Issues
- **Comments missing in Word**: run `doc.verify_comments()` and re-save
- **find_paragraph fails**: shorten search text; confirm actual paragraph text
- **Mermaid render fails**: ensure `mmdc` installed; use Chrome path or Puppeteer config

### CLI Issues
- **QCC CLI not found**: Verify installation with `qcc --version`; reinstall with `pip install qcc-cli`
- **CLI command fails**: Check network connectivity; verify API key permissions
- **CLI output empty**: Company name may need exact match; try with full legal name

### MCP Issues
- **QCC MCP not working**: verify `QCC_MCP_API_KEY` is set; check network connectivity to https://agent.qcc.com
- **MCP tools not loading**: Restart Claude Code after configuring `.mcp.json`

## Examples

See **[references/examples.md](references/examples.md)** for a full workflow example.

## Important Rules

1. Never alter original contract text
2. Entity verification (Layer 0) must complete before clause review (Layers 1–3)
3. Review all four layers, do not skip items
4. Ensure risk level is accurate and consistent
5. Keep comments precise, professional, and actionable
6. Flowchart must come strictly from the contract text
7. Summary is objective only; no risk analysis
8. Opinion only reflects findings already identified

## License

SPDX-License-Identifier: Apache-2.0

Copyright (c) 2026 JiCheng

Licensed under the Apache License, Version 2.0. See repository root `LICENSE`.
