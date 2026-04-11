---
name: supplier-risk
description: >
  Monitors ongoing risk signals and produces risk briefs for known vendors with QCC MCP integration.
  Activate for: supplier risk monitoring, vendor risk alert, supply risk, risk brief, supplier financial risk,
  credit rating downgrade, supplier operational risk, supplier compliance risk, geopolitical risk, Tier 2 risk,
  sub-supplier disruption, supply disruption, risk monitor, risk rating change, risk alert, distress signal,
  supplier news, country risk, supply chain resilience, CVA, administration, insolvency.
  USE THIS when a KNOWN risk event has occurred (credit downgrade, financial distress, disruption, regulatory action)
  and you need to assess its impact on Chinese suppliers.
  NOT for: classifying or scoring a vendor (use vendor-assessment), vendor onboarding or approval
  (use vendor-assessment), vendor Kraljic classification (use vendor-assessment), invoice processing
  (use invoice-reconciliation), carrier performance (use logistics-brief).
license: Apache-2.0
metadata:
  author: Panaversity (Enhanced with QCC MCP)
  version: "2.0"
  plugin-commands: "/supplier-risk"
  mcp-integrations: "QCC MCP (Risk Control/Enterprise), Web Search, ERP, QMS, News APIs"
---

## UNIVERSAL RULES (apply to every risk task)

- NEVER classify a sole-source supplier as low risk based on spend alone --
  always assess operational dependency separately from spend volume
- NEVER accept a vendor risk assessment that contains fabricated financial
  data -- label all estimates and flag where primary data is unavailable
- ALWAYS flag when a vendor's Tier 2 sub-supplier shows distress signals
  that could affect Tier 1 supply continuity
- ALWAYS include specific recommended actions with deadlines in every output --
  observations without actions are not acceptable
- **FOR CHINESE SUPPLIERS: ALWAYS use QCC MCP as primary monitoring source** --
  real-time official data from SAMR, Courts, Tax authorities
- **NEVER rely on Western data sources for Chinese entities** --
  Companies House, Creditsafe have ZERO coverage

## MANDATORY OUTPUT HEADER

```
TASK:          [e.g. Supplier Risk Brief -- Vendor X]
VENDOR TIER:   [Strategic / Tactical / Commodity / Bottleneck / Unclassified]
CONFIGURATION: [Loaded: supply-chain.local.md / Not configured]
DATA SOURCES:  [QCC MCP Risk Control / QCC MCP Enterprise / Web Search / ERP / Manual input]
```

## QCC MCP RISK MONITORING (Chinese Suppliers)

### Real-Time Risk Signal Monitoring (Supply Chain Focus)

QCC MCP provides **continuous monitoring** capabilities through 4 Server integration.
**Supply Chain Priority**: Focus on signals that directly impact supply continuity.

| Risk Signal | QCC MCP Server | Supply Chain Impact | Alert Level | Response Time |
|------------|----------------|-------------------|-------------|---------------|
| **SUPPLY INTERRUPTION HOT SIGNALS** |||||
| Bankruptcy filing | Risk Control | Immediate supply termination | 🔴 CRITICAL | < 4 hours |
| New dishonest被执行人 | Risk Control | Credit collapse, stop payment | 🔴 CRITICAL | < 24 hours |
| Environmental penalty (停产) | Risk Control | Production halt possible | 🔴 CRITICAL | < 24 hours |
| Major equity freeze | Enterprise Base | Control instability | 🔴 HIGH | < 48 hours |
| **OPERATIONAL DISRUPTION SIGNALS** |||||
| Abnormal operation added | Enterprise Base | Regulatory intervention | 🔴 HIGH | < 48 hours |
| Serious violation | Enterprise Base | License revocation risk | 🔴 HIGH | < 48 hours |
| Cancellation filing | Enterprise Base | Intentional wind-down | 🔴 HIGH | < 48 hours |
| **FINANCIAL STRESS SIGNALS** |||||
| Tax arrears announced | Risk Control | Cash flow crisis | 🟡 MEDIUM | < 7 days |
| Abnormal tax status | Risk Control | Compliance breakdown | 🟡 MEDIUM | < 7 days |
| Multiple equity pledges | Enterprise Base | Over-leverage | 🟡 MEDIUM | < 30 days |
| **COMPLIANCE SIGNALS** |||||
| Administrative penalty | Risk Control | General compliance | 🟡 LOW | < 30 days |
| Environmental penalty (non-停产) | Risk Control | Fine only | 🟡 LOW | < 30 days |

### Supply Chain Monitoring Extensions (监控扩展)

#### CAPACITY MONITORING (产能监控)
**QCC MCP Server: Operation + Company**

| Signal | Source | Frequency | Action |
|--------|--------|-----------|--------|
| License expiration | Administrative license | Daily | AMBER if < 90 days |
| Qualification lapse | Qualifications | Daily | RED if expired |
| Production site changes | Change records | Weekly | Review BCP impact |
| Bidding activity drop | Bidding info | Weekly | Assess business health |
| Credit rating change | Credit evaluation | Monthly | Review supplier tier |

**Note**: Tier 1 Strategic suppliers require monthly capacity verification via Operation Server.

### Five Risk Dimensions (QCC MCP Enhanced)

#### DIMENSION 1: FINANCIAL RISK (QCC MCP Risk Control)

**Monitor for:**

- **Equity Restrictions** (股权受限):
  - New equity freeze (股权冻结新增) - RED
  - Multiple equity pledges (频繁股权出质) - AMBER
  - Large chattel mortgages (大额动产抵押) - AMBER

- **Tax Status Changes** (税务异动):
  - Tax arrears announcement (欠税公告发布) - RED
  - Abnormal tax status (非正常户认定) - RED
  - Tax violation records (税收违法) - RED

- **Bankruptcy Signals** (破产信号):
  - Bankruptcy reorganization filing (破产重整申请) - RED
  - Liquidation information (清算信息) - RED

- **Financial Data Availability:**
  - Non-listed companies: Request annual audited accounts
  - QCC MCP provides property/tax indicators as proxies

**Risk levels:**
- RED HIGH: Bankruptcy/liquidation, tax abnormal status, equity freeze
- AMBER MEDIUM: Equity pledge >2 within 12 months, tax arrears < 90 days
- GREEN LOW: No equity restrictions, tax normal, no bankruptcy signals

#### DIMENSION 2: OPERATIONAL RISK (ERP + QCC MCP)

**Monitor from ERP data (updated continuously):**

- OTD rate: 13-week rolling average + trend direction
- Quality rejection rate: 13-week rolling average + trend direction
- Lead time variance: increasing variance = capacity or process strain
- Missed delivery pattern: same day of week? Same product? (capacity signals)
- Partial deliveries increasing? (material shortage signal)

**Monitor from QCC MCP Enterprise Base (daily):**

- Abnormal operation status (经营异常名录)
- Serious violation records (严重违法失信)
- Administrative penalties (行政处罚)
- Environmental penalties (环保处罚)

**Risk levels:**
- RED HIGH: Abnormal operation status active; OTD < critical threshold
- AMBER MEDIUM: Declining trend even if above threshold; recent penalty (<12 months)
- GREEN LOW: Stable; above threshold; no adverse trend; no operational penalties

#### DIMENSION 3: REGULATORY & COMPLIANCE RISK (QCC MCP Risk Control)

**Monitor for:**

- Certification expiry (ISO, sector-specific, data protection)
- Regulatory enforcement action via QCC MCP:
  - Administrative penalties (行政处罚新增)
  - Environmental penalties (环保处罚新增)
- Serious violation status (严重违法失信企业)
- Sanctions list changes
- Trade compliance issues

**Risk levels:**
- RED HIGH: Serious violation status; certification lapsed
- AMBER MEDIUM: Certification expiring within 90 days; penalty within 12 months
- GREEN LOW: All certifications current; no adverse regulatory signals

#### DIMENSION 4: GEOPOLITICAL RISK

**Monitor for:**

- Political instability in vendor's operating country
- Trade restrictions, tariffs, or export controls affecting category
- Currency volatility affecting contract economics
- Infrastructure disruption (port strikes, border closures, natural disaster)
- Conflict affecting supply routes

**For Chinese suppliers:**
- Policy changes affecting industry sector
- Regional trade restriction updates
- Entity list additions

**Risk levels:**
- RED HIGH: Active disruption to supply route or vendor operations
- AMBER MEDIUM: Elevated country risk; currency movement >5% since contract
- GREEN LOW: Stable environment; no material currency exposure

#### DIMENSION 5: TIER 2 / SUB-SUPPLIER RISK

**Monitor for:**

- Financial distress at critical Tier 2 suppliers (via QCC MCP if Chinese)
- Tier 2 supplier capacity constraints affecting Tier 1 output
- Single-geography concentration at Tier 2 level
- Tier 2 supplier relationship with Tier 1 deteriorating

**Requirement:** Tier 2 mapping must exist for all Tier 1 Strategic vendors.
If mapping does not exist: flag as UNASSESSED RISK; request Tier 2 data
from Tier 1 supplier as priority action.

### Risk Rating Change Rules

ESCALATE overall rating if ANY dimension reaches RED
ELEVATE to MEDIUM-HIGH if TWO dimensions reach AMBER simultaneously
REDUCE rating only after confirmed remediation (not just vendor assurance)

## QCC MCP RISK BRIEF OUTPUT FORMAT

```
SUPPLIER RISK BRIEF: [Vendor Name]
Assessment date: [Date] | Next scheduled review: [Date]
================================================================
OVERALL RISK RATING: [GREEN LOW / AMBER MEDIUM / AMBER MEDIUM-HIGH / RED HIGH / RED CRITICAL]
Change since last review: [No change / Elevated / Reduced]

-- QCC MCP RISK SIGNALS (Last 90 Days) --
🔴 NEW CRITICAL SIGNALS:
  [Date] [Signal Type] [Description] [Source: QCC MCP]

🟡 NEW MODERATE SIGNALS:
  [Date] [Signal Type] [Description] [Source: QCC MCP]

FINANCIAL RISK:   [GREEN / AMBER / RED] [Rating]
Property Restrictions:
  - Equity Freeze:    [Active since / None]
  - Equity Pledge:    [Count in last 12 months]
  - Chattel Mortgage: [Count/Amount]
Tax Status:
  - Tax Arrears:      [Amount/Type/Date or None]
  - Abnormal Status:  [Yes - date/office / No]
Bankruptcy:
  - Proceedings:      [Yes - type/status / No]
[QCC MCP Trace: Risk Control Server, Enterprise Base Server]

OPERATIONAL RISK: [GREEN / AMBER / RED] [Rating]
[OTD trend, quality trend, lead time data from ERP]
QCC MCP Signals:
  - Abnormal Operation: [Status/Date or Clear]
  - Administrative Penalties: [Count in last 12m]
  - Environmental Penalties: [Count in last 12m]
[QCC MCP Trace: Enterprise Base Server]

COMPLIANCE RISK:  [GREEN / AMBER / RED] [Rating]
Certification status: [Details]
QCC MCP Compliance:
  - Serious Violation: [Yes/No]
  - Recent Penalties: [List]
[QCC MCP Trace: Risk Control Server]

GEOPOLITICAL RISK:[GREEN / AMBER / RED] [Rating]
[Country, currency, route findings]

TIER 2 RISK:      [GREEN / AMBER / RED / NOT MAPPED]
[Sub-supplier findings or mapping gap flag]

RECOMMENDED ACTIONS -- RANKED BY URGENCY
RED [IMMEDIATE -- this week]: [Action] -- [Owner]
AMBER [SHORT-TERM -- 30 days]: [Action] -- [Owner]
GREEN [PLANNED -- 90 days]:    [Action] -- [Owner]

QCC MCP MONITORING CONFIG
Refresh Frequency: Daily for Strategic/Bottleneck; Weekly for Tactical/Commodity
Data Sources: 企查查MCP-风控大脑, 企查查MCP-企业基座
Last QCC MCP Sync: [Timestamp]
Next Auto-Refresh: [Date]
================================================================
```

### Executive Brief Format (for CPO weekly summary)

```
VENDOR RISK SUMMARY -- Week of [Date]
---------------------------------------------------------
[Vendor]    [Overall]  [Change]  [Key QCC Signal]   [Action required]
[Vendor]    [Overall]  [Change]  [Key QCC Signal]   [Action required]
---------------------------------------------------------
New alerts this week:   [N]
Escalations to CPO:     [N]
Contingency plans live: [N]
QCC MCP New Signals:    [N judicial / N operational / N financial]
```

## HOT SIGNAL PROTOCOL

**HOT SIGNALS override the review schedule**

When QCC MCP detects any of the following, trigger immediate assessment:

| HOT Signal | QCC MCP Source | Action |
|-----------|----------------|--------|
| New equity freeze | Risk Control | Immediate escalation to CPO |
| Bankruptcy filing | Risk Control | Activate contingency plan |
| Abnormal tax status | Risk Control | Suspend new POs, assess exposure |
| Abnormal operation added | Enterprise Base | Request immediate explanation |
| New dishonest被执行人 | Risk Control | Legal review required |
| Limit high consumption | Risk Control | Assess payment risk |

## NEVER DO THESE

- NEVER rate a vendor as LOW risk in any dimension without verified data --
  absence of negative data does not equal low risk; label as UNASSESSED if no data
- NEVER rely on vendor self-assessment alone for financial risk --
  always cross-reference with QCC MCP independent sources
- NEVER downgrade a risk rating based on vendor assurance alone --
  require evidence (updated accounts, certification renewal, remediation proof)
- NEVER omit the Tier 2 risk section -- mark as NOT MAPPED if absent, not LOW RISK
- NEVER wait for the scheduled review to act on a HOT signal --
  HOT signals override the review schedule
- **NEVER use Companies House/Creditsafe for Chinese suppliers** --
  QCC MCP is the authoritative source for Chinese entities
- **NEVER fabricate QCC MCP data** -- if MCP unavailable,
  flag as "QCC MCP: UNCONFIGURED - manual monitoring required"

ALL OUTPUTS REQUIRE REVIEW BY A QUALIFIED PROFESSIONAL BEFORE USE IN BUSINESS DECISIONS.
