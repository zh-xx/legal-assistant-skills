---
name: contract-review
description: "Contract review skill that adds comment-based issue annotations without changing original text. Enforces a four-layer review (entity verification, basic, business, legal), writes structured comments (issue type, risk reason, revision suggestion) with risk level encoded via reviewer name, and generates a contract summary, consolidated opinion, and Mermaid business flowchart (with rendered image). Output language must follow the contract’s language."
---

# Contract Review Skill

## Overview

This skill performs contract reviews by **adding comments only** (no edits to the original text). It follows a four-layer review (entity verification, basic, business, legal) and generates:

- Annotated contract (.docx)
- Contract summary (.docx)
- Consolidated review opinion (.docx)
- Business flowchart (Mermaid + rendered image)

**Language rule:** detect the contract’s dominant language and output all generated content (comments, summary, opinion, flowchart text) in that language. Use the guidance in **[references/language.md](references/language.md)**.

## Workflow

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
- **Verification tool priority:**
  1. **Enterprise Verification via QCC MCP (Recommended):** If `QCC_MCP_API_KEY` environment variable is set, use the QiChaCha MCP service for automated enterprise verification and risk assessment. See [Enterprise Verification Setup](#enterprise-verification-setup) below.
  2. **Fallback MCP tools:** If no QCC API key but other MCP tools for business registration lookup are available (e.g., enterprise info query, company lookup, 企业查询, 工商查询), use them to query each party's name or Unified Social Credit Code.
  3. **Web Search fallback:** If no MCP tool is available, use Web Search to look up "[entity name] 工商登记信息" or "[entity name] business registration".
  4. Record the verification source (QCC MCP / MCP tool / Web Search) in the comment.


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

Outputs:
- `business_flowchart.mmd`
- `business_flowchart.png`

## Technical Notes

Core workflow:
1. Unpack → 2. Entity verification → 3. Add comments → 4. Summary → 5. Opinion → 6. Flowchart → 7. Repack

API & implementation details:
- **[references/technical.md](references/technical.md)**

## Enterprise Verification Setup (QCC MCP Integration)

This skill supports **QCC 企查查 MCP (Model Context Protocol)** service for automated enterprise verification and risk assessment.

### Features

When QCC MCP is enabled, the skill automatically:
- Verifies enterprise registration information (name, legal representative, credit code, status)
- Performs 18-category risk screening (dishonest records, enforcement, operational abnormalities, tax violations, bankruptcy, etc.)
- Generates structured review comments with risk levels

### Setup Instructions

1. **Apply for QCC MCP API Key**
   - Visit [QiChaCha MCP Portal](https://mcp.qcc.com) to apply for access
   - Obtain your API key

2. **Set Environment Variable**
   ```bash
   export QCC_MCP_API_KEY="your_api_key_here"
   ```

3. **Verify Setup**
   ```bash
   python -c "from scripts.qcc_mcp_client import QccMcpClient; c = QccMcpClient(); print('✅ MCP enabled' if c.is_enabled() else '❌ MCP not enabled')"
   ```

### Fallback Behavior

- **If QCC_MCP_API_KEY is set:** Use QiChaCha MCP for enterprise verification and risk screening
- **If QCC_MCP_API_KEY is not set:** Fall back to Web Search for enterprise verification (original behavior)


## Dependencies

- Python 3.9+ (3.10+ recommended)
- pandoc (system install)
- defusedxml
- Mermaid CLI (`mmdc`) for rendering
- python-docx for rich text output
- requests (for QCC MCP API calls, optional)

## Troubleshooting (Short)

- **Comments missing in Word**: run `doc.verify_comments()` and re-save
- **find_paragraph fails**: shorten search text; confirm actual paragraph text
- **Mermaid render fails**: ensure `mmdc` installed; use Chrome path or Puppeteer config
- **QCC MCP not working**: verify `QCC_MCP_API_KEY` is set; check network connectivity to https://mcp.qcc.com

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
