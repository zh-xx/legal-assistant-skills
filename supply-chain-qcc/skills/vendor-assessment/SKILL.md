---
name: vendor-assessment
description: >
  Classifies, scores, and evaluates vendors with QCC MCP integration for Chinese suppliers.
  Activate for: vendor assessment, classify vendor, vendor classification, Kraljic matrix,
  vendor tier, bottleneck vendor, strategic vendor, vendor review, supplier assessment,
  vendor onboarding, new vendor approval, vendor audit, annual vendor review,
  vendor scorecard, supplier evaluation, vendor qualification, approve vendor,
  vendor due diligence, vendor health check, vendor performance review,
  bottleneck supplier, vendor exit, risk profile of a vendor.
  USE THIS when the task is to CLASSIFY a vendor into a category (Strategic /
  Tactical / Commodity / Bottleneck), SCORE them across dimensions, or EVALUATE
  a vendor for onboarding/approval/exit.
  NOT for: ongoing risk signal monitoring or risk alerts (use supplier-risk),
  invoice reconciliation (use invoice-reconciliation), carrier performance
  review (use logistics-brief), spend category analysis (use spend-analysis).
license: Apache-2.0
metadata:
  author: Panaversity (Enhanced with QCC MCP)
  version: "2.0"
  plugin-commands: "/vendor-assess"
  mcp-integrations: "QCC MCP (Enterprise/Risk/IP/Business), ERP, Web Search"
---

## UNIVERSAL RULES (apply to every vendor task)

- NEVER classify a sole-source supplier as low risk based on spend alone --
  always assess operational dependency separately from spend volume
- NEVER accept a vendor risk assessment that contains fabricated financial
  data -- label all estimates and flag where primary data is unavailable
- NEVER recommend a vendor exit without a qualified alternative identified
  or an explicit "no alternative -- managed risk" decision documented
- ALWAYS include specific recommended actions with deadlines in every output --
  observations without actions are not acceptable
- **FOR CHINESE SUPPLIERS: ALWAYS use QCC MCP as primary data source** --
  Companies House and Creditsafe have NO coverage for Chinese entities
- **NEVER fabricate Chinese enterprise data** -- if QCC MCP unavailable,
  explicitly flag as "financial visibility: NONE" and recommend manual verification

## MANDATORY OUTPUT HEADER

Every output must begin with:

```
TASK:          [e.g. Vendor Assessment -- Acme Corp]
VENDOR TIER:   [Strategic / Tactical / Commodity / Bottleneck / Unclassified]
CONFIGURATION: [Loaded: supply-chain.local.md / Not configured]
DATA SOURCES:  [QCC MCP / ERP / Web / Manual input]
```

## QCC MCP INTEGRATION (Chinese Suppliers)

### When to Activate QCC MCP

**ALWAYS activate for Chinese suppliers** (vendors with):
- Chinese company name (e.g., "华为技术有限公司", "阿里巴巴集团")
- Unified Social Credit Code (统一社会信用代码)
- Registered in mainland China

**QCC MCP provides official data from:**
- National Enterprise Credit Information Publicity System (国家企业信用信息公示系统)
- China Judgments Online (中国裁判文书网)
- China Execution Information (中国执行信息公开网)
- State Taxation Administration (国家税务总局)
- SAMR (国家市场监督管理总局)

### 18-Risk Categories for Supply Chain (供应链专用)

**设计原则**: 供应链评估聚焦"供应连续性风险"，与法务合同审核的关注点不同

| Risk Category | QCC MCP Server | Supply Chain Focus | Priority |
|--------------|----------------|-------------------|----------|
| **SUPPLY INTERRUPTION RISKS** ||||
| **Judicial Execution** | Risk Control | 直接影响生产资金链 | 🔴 CRITICAL |
| - Dishonest (失信) | | 信用崩溃，履约能力丧失 | |
| - Executed person (被执行人) | | 现金流危机，影响原材料采购 | |
| - Limit high consumption (限高) | | 法人受限，商务活动受阻 | |
| - Final case (终本案件) | | 历史债务累积，财务恶化 | |
| - Judicial auction (司法拍卖) | | 核心资产被拍卖，产能受损 | |
| **Bankruptcy Liquidation** | Risk Control | 供应关系终止 | 🔴 CRITICAL |
| - Bankruptcy reorganization (破产重整) | | 需立即切换供应商 | |
| **OPERATIONAL CONTINUITY RISKS** ||||
| **Operational Abnormal** | Enterprise Base | 经营稳定性 | 🔴 HIGH |
| - Abnormal operation (经营异常) | | 工商监管介入，经营不稳定 | |
| - Serious violation (严重违法) | | 可能被吊销执照，供应中断 | |
| - Cancellation filing (注销备案) | | 主动终止经营，供应中断 | |
| **Environmental Penalty** | Risk Control | 可能导致停产 | 🟡 MEDIUM |
| - Environmental penalty (环保处罚) | | 责令停产整改，影响交付 | |
| **FINANCIAL HEALTH RISKS** ||||
| **Property Restricted** | Enterprise Base | 财务稳定性指标 | 🟡 MEDIUM |
| - Equity freeze (股权冻结) | | 股东纠纷，控制权不稳定 | |
| - Equity pledge (股权出质) | | 融资压力，流动性风险 | |
| - Chattel mortgage (动产抵押) | | 设备抵押，影响产能扩张 | |
| **Tax Violation** | Risk Control | 现金流与合规 | 🟡 MEDIUM |
| - Tax arrears (欠税公告) | | 现金流危机，可能拖欠货款 | |
| - Abnormal tax (非正常户) | | 税务合规严重问题 | |
| **Administrative Penalty** | Risk Control | 行业合规 | 🔵 LOW |
| - Administrative penalty (行政处罚) | | 一般合规问题 | |

### Supply Chain Specific Dimensions (供应链特有维度)

Beyond the 18 core risks, supply chain assessment MUST evaluate:

#### DIMENSION 7: CAPACITY & QUALIFICATION (产能与资质)
**QCC MCP Server: Operation + Company**

- **Business Qualifications** (资质证书):
  - Industry-specific licenses (生产许可证、经营许可证)
  - Quality certifications (ISO 9001, IATF 16949, etc.)
  - Sector permits (医疗器械、食品生产、危险品等)
  - Flags: RED - Required license expired or not held

- **Administrative Licenses** (行政许可):
  - Current validity of operating permits
  - Renewal status and timeline
  - Flags: AMBER - License expiring within 90 days

- **Bidding Activity** (招投标活跃度):
  - Recent bidding participation (indicator of business health)
  - Win/loss ratio trends
  - Flags: AMBER - Significant decline in bidding activity (>50% YoY)

#### DIMENSION 8: ORGANIZATIONAL STABILITY (组织稳定性)
**QCC MCP Server: Company**

- **Shareholder Structure** (股权结构):
  - Major shareholder changes (indicator of control instability)
  - State-owned vs. private (policy risk assessment)
  - Flags: RED - Major shareholder change within 6 months

- **Change Records** (变更记录):
  - Frequent legal representative changes
  - Registered address changes (relocation risk)
  - Business scope changes (strategy shift)
  - Flags: AMBER - >3 material changes within 12 months

- **Branch Network** (分支机构):
  - Geographic distribution of production facilities
  - Single-site vs. multi-site (business continuity)
  - Flags: AMBER - Single production site with no backup

#### DIMENSION 9: BUSINESS HEALTH (业务健康度)
**QCC MCP Server: Operation**

- **Official Credit Rating** (官方信用评价):
  - Government credit ratings (A级、B级等)
  - Tax credit rating (A级纳税人)
  - Flags: RED - Rating below B级

- **Spot Check Records** (抽查检查记录):
  - Regulatory inspection results
  - Product quality spot checks
  - Flags: RED - Failed inspection with corrective action pending

- **News Sentiment** (新闻舆情):
  - Negative news coverage (supply chain disruptions, labor issues)
  - Industry-specific concerns
  - Flags: AMBER - Negative sentiment spike (>3 negative articles in 30 days)

## ASSESSMENT WORKFLOW

### Phase 1: Vendor Classification (Kraljic Matrix)

Before any assessment, classify the vendor:

| Question                    | Strategic     | Tactical    | Commodity     | Bottleneck    |
| --------------------------- | ------------- | ----------- | ------------- | ------------- |
| Are alternatives available? | No / very few | Yes -- 2-3  | Many          | No / very few |
| Annual spend?               | High          | Medium      | Any           | Low-Medium    |
| Impact if vendor fails?     | Critical      | Significant | Manageable    | Critical      |
| Relationship depth?         | Deep / long   | Established | Transactional | Variable      |

**STRATEGIC (Tier 1):** High spend AND high dependency. Single-source or near-sole-source. Review: quarterly + event-triggered.
**TACTICAL (Tier 2):** Significant spend. Multiple alternatives available. Review: bi-annual + event-triggered.
**COMMODITY (Tier 3):** Standard goods/services. Easy to switch. Review: annual.
**BOTTLENECK (Tier 4):** LOW spend but HIGH dependency. MOST DANGEROUS -- most often neglected. Review: quarterly despite low spend.

**CLASSIFICATION RULE:** When assessing a vendor with low spend but sole-source dependency, ALWAYS classify as BOTTLENECK and flag as high-risk regardless of spend volume.

### Phase 2: Six-Dimension Assessment

#### DIMENSION 1: COMMERCIAL

Contract status:

- Active contract: Yes/No; expiry date; auto-renewal clause?
- Notice period for non-renewal: documented?
- Pricing model: fixed / index-linked / open book / variable
- Payment terms: standard for sector/market?
- Volume commitments: minimum order quantities; penalty clauses?
- IP ownership: critical for manufactured-to-spec components

**Flags:**
- RED: No contract for spend > configured threshold
- RED: Auto-renewal without documented notice window reminder
- AMBER: Fixed price contract on commodity category (index exposure)
- AMBER: Volume commitment with penalty below minimum forecast volume

#### DIMENSION 2: OPERATIONAL

Metrics from ERP (last 12 months):

- On-time delivery rate (OTD): calculate from GR dates vs. PO delivery dates
- Average lead time and variance (consistency matters as much as average)
- Quality rejection rate (from QMS or goods inward records)
- Capacity: can they scale with our growth? (ask directly)
- Business continuity: single site or multiple?

**For Chinese suppliers:** Check operational risk signals via QCC MCP:
- Abnormal operation status (经营异常)
- Administrative penalties (行政处罚)
- Environmental penalties (环保处罚)

**Flags:**
- RED: OTD < configured threshold for tier (e.g. <90% for Strategic)
- RED: Quality rejection > configured threshold (e.g. >2% for direct materials)
- RED: Abnormal operation status detected (QCC MCP)
- AMBER: OTD declining trend (even if above threshold -- trajectory matters)
- AMBER: Single production site with no documented BCP

#### DIMENSION 3: FINANCIAL

**For Chinese suppliers (QCC MCP):**

- **Property Restrictions** (RED FLAGS):
  - Equity freeze (股权冻结): Indicates judicial disputes
  - Equity pledge (股权出质): Financing pressure signal
  - Chattel mortgage (动产抵押): Working capital pressure

- **Tax Status** (RED FLAGS):
  - Tax arrears announcements (欠税公告)
  - Abnormal tax status (税务非正常户)
  - Tax violations (税收违法)

- **Bankruptcy/Liquidation** (RED FLAGS):
  - Bankruptcy reorganization proceedings (破产重整)
  - Liquidation information (清算信息)

- **Financial Data Availability:**
  - Non-listed companies: Limited financial visibility
  - For Strategic/Bottleneck vendors: Request audited financial statements annually

**Financial Risk Assessment (QCC MCP Enhanced):**

| Indicator | Data Source | Risk Signal |
|-----------|-------------|-------------|
| Equity freeze | QCC MCP Enterprise | RED - Judicial dispute |
| Equity pledge | QCC MCP Enterprise | AMBER - Financing need |
| Tax arrears | QCC MCP Risk Control | RED - Cash flow crisis |
| Abnormal tax | QCC MCP Risk Control | RED - Non-compliant |
| Bankruptcy | QCC MCP Risk Control | RED - Insolvency |

**Flags:**
- RED: Equity freeze active
- RED: Tax arrears or abnormal tax status
- RED: Bankruptcy/liquidation proceedings
- RED: Zero financial visibility on Strategic or Bottleneck vendor
- AMBER: Equity pledge registered (check if multiple)
- AMBER: Chattel mortgage (assess scale vs. business size)

#### DIMENSION 4: COMPLIANCE

Certifications required (configure by category in local settings):

- Quality: ISO 9001 / sector-specific (IATF 16949 for automotive, etc.)
- Environmental: ISO 14001 (if required by your policy)
- Data: GDPR compliance + DPA for any data-sharing arrangement
- Modern Slavery Act statement (UK vendors > GBP 36M turnover)
- Sanctions screening: verified against OFAC, EU, UK HMT lists
- Trade compliance: export licences, import documentation
- ESG/ethical sourcing: modern slavery, conflict minerals (sector-specific)

**For Chinese suppliers - QCC MCP Enhanced:**

- **Administrative Penalties:** Check via QCC MCP Risk Control
- **Environmental Penalties:** Check via QCC MCP Risk Control
- **Serious Violations:** Check via QCC MCP Enterprise Base (严重违法)

**Flags:**
- RED: Active sanctions match -- immediate escalation; stop all activity
- RED: Required certification expired with no renewal in progress
- RED: Serious violation record (严重违法)
- AMBER: Certification expiring within 90 days -- request renewal evidence
- AMBER: Administrative/environmental penalty within 12 months

#### DIMENSION 5: STRATEGIC

- Dependency: sole-source / dual-source / approved panel
- Switching timeline: how long to qualify and onboard an alternative?
- Switching cost: tooling, qualification, ramp-up period
- Relationship investment: what have we and they invested?
- Innovation: are they bringing improvements and ideas?
- Strategic alignment: do their long-term plans align with ours?

**For Chinese suppliers:**
- Check equity structure changes (investment/exit signals)
- Monitor major shareholder changes via QCC MCP Enterprise

**Flags:**
- RED: Sole-source with switching timeline >6 months and no backup qualified
- AMBER: No alternative vendor qualified or in qualification for critical category
- AMBER: Vendor has indicated desire to exit the relationship or market segment

#### DIMENSION 6: GEOPOLITICAL / SUSTAINABILITY

- Country risk: political stability; trade restriction risk; sanctions exposure
- Currency risk: contract currency vs. payment currency
- Supply chain depth: do we know Tier 2 sub-suppliers for critical components?
- Carbon footprint and Scope 3 reporting (increasingly mandatory)
- Ethical sourcing: conflict minerals, child labour risk by geography
- Single-geography concentration: are all suppliers for this category in the same country or region?

**For Chinese suppliers:**
- Consider China-specific risks: policy changes, trade restrictions
- Check if supplier is in restricted entity list (QCC MCP can cross-reference)

**Flags:**
- RED: Vendor in sanctioned country or subject to active export restrictions
- RED: Entity list / restricted party match
- AMBER: All suppliers for a critical category in a single high-risk geography
- AMBER: No Tier 2 supplier mapping for Strategic vendors

## QCC MCP ASSESSMENT OUTPUT FORMAT

```
VENDOR ASSESSMENT: [Vendor Name]
================================================================
Classification:  [STRATEGIC / TACTICAL / COMMODITY / BOTTLENECK]
Tier:            [1 / 2 / 3 / 4]
Rationale:       [Brief justification for classification]

-- ENTITY VERIFICATION (QCC MCP) ---------------------------------
Entity Status:    [Verified / Not Found / Multiple Matches]
Credit Code:      [Unified Social Credit Code]
Legal Status:     [存续/在业/注销/吊销/etc.]
Legal Person:     [Name]
Registered Cap:   [Amount]
Verification:     [实体锚定确认信息]

-- COMMERCIAL ----------------------------------------------------
[Findings and flags per item above]

-- OPERATIONAL ---------------------------------------------------
OTD (12M):     [X]%   Threshold: [X]%   Status: [PASS / WARNING / FAIL]
Lead time avg: [X] days  Variance: +/-[X] days
Quality rej:   [X]%   Threshold: [X]%   Status: [PASS / WARNING / FAIL]

QCC MCP Signals:
  - Abnormal Operation: [Yes - details / No]
  - Administrative Penalties: [Count and details]
  - Environmental Penalties: [Count and details]

-- FINANCIAL (QCC MCP Enhanced) ----------------------------------
Property Restrictions:
  - Equity Freeze:    [Yes - amount/date / No]
  - Equity Pledge:    [Yes - amount/creditor / No]
  - Chattel Mortgage: [Yes - amount/scope / No]

Tax Status:
  - Tax Arrears:      [Yes - amount/type / No]
  - Abnormal Tax:     [Yes - date/office / No]
  - Tax Violations:   [Count]

Bankruptcy/Liquidation:
  - Bankruptcy:       [Yes - type/status / No]
  - Liquidation:      [Yes / No]

Financial Visibility: [Available / Limited / None]
Data Source: QCC MCP (official SAMR/National Tax sources)

-- COMPLIANCE ----------------------------------------------------
Certifications: [Status]
QCC MCP Compliance Check:
  - Administrative Penalties: [Count and details]
  - Environmental Penalties: [Count and details]
  - Serious Violations: [Yes/No - details]
Sanctions:      [Clear / Flagged - details]

-- STRATEGIC -----------------------------------------------------
[Dependency level; switching timeline; backup vendor status]

-- GEOPOLITICAL / SUSTAINABILITY ---------------------------------
[Country risk; currency; Tier 2 visibility; ESG]

RISK SUMMARY
RED CRITICAL: [list]
AMBER MODERATE: [list]
GREEN LOW: [list]

RECOMMENDED ACTIONS -- RANKED BY URGENCY
[N]. [Priority] [Action] -- [Owner] -- by [Date]

QCC MCP ASSESSMENT TRACE
Data Sources: 企查查MCP-企业基座, 企查查MCP-风控大脑
Assessment Time: [Timestamp]
Next QCC MCP Refresh: [Date + 90 days recommended]
================================================================
```

## NEVER DO THESE

- NEVER classify a sole-source supplier as low-risk because spend is low
- NEVER complete a financial assessment with fabricated data --
  if data unavailable: flag explicitly as "financial visibility: NONE"
  and recommend requesting audited accounts
- NEVER conduct a sanctions screening check manually --
  always use an authoritative list (OFAC, EU, UK HMT)
- NEVER close an assessment without a recommended action list
- NEVER skip the Tier 2 visibility check for Strategic vendors
- **NEVER use Companies House or Creditsafe for Chinese suppliers** --
  these sources have ZERO coverage for Chinese entities
- **NEVER fabricate QCC MCP data** -- if MCP unavailable,
  flag as "QCC MCP: NOT CONFIGURED" and use manual verification

ALL OUTPUTS REQUIRE REVIEW BY A QUALIFIED PROFESSIONAL BEFORE USE IN BUSINESS DECISIONS.
