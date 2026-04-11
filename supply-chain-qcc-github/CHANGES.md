# QCC MCP Supply Chain Plugin - Change Log

## 版本对比：原版 vs QCC MCP增强版

### 基础信息

| 项目 | 原版 | QCC MCP增强版 |
|------|------|--------------|
| 版本号 | 1.0 | 2.0 |
| 作者 | Panaversity | Panaversity + QCC MCP |
| 适用场景 | 全球供应商 | 中国供应商优先，兼容全球 |

---

## SKILL.md 变更详情

### vendor-assessment/SKILL.md

#### 新增部分

1. **QCC MCP Integration Section (Lines 25-75)**
   - 18类风险清单映射到六维度评估
   - QCC MCP Server与风险维度对应关系
   - 中国企业识别触发条件

2. **Entity Verification Section (Lines 176-183)**
   - 实体锚定确认输出格式
   - 统一社会信用代码展示
   - 工商登记状态核验

3. **Financial Dimension - QCC MCP Enhanced (Lines 120-155)**
   - 财务替代指标体系
   - 股权冻结/出质/动产抵押
   - 税务异常/欠税/破产信号
   - 非上市公司财务可见性处理

4. **Operational Dimension - QCC MCP Signals (Lines 96-108)**
   - 经营异常名录扫描
   - 行政处罚监控
   - 环保处罚检查

5. **Assessment Output Format - QCC MCP Trace (Lines 205-211)**
   - QCC MCP数据源追溯
   - 评估时间戳
   - 下次刷新建议

#### 修改部分

- **Universal Rules**: 新增第5、6条关于QCC MCP的规则
- **Data Sources**: 更新为 "QCC MCP, ERP, Web, Manual input"
- **Financial Flags**: 新增QCC MCP相关的RED/AMBER flag

---

### supplier-risk/SKILL.md

#### 新增部分

1. **QCC MCP Risk Monitoring Section (Lines 25-70)**
   - 实时风险信号监控机制
   - 4 Server集成监控频率
   - HOT Signal Protocol

2. **Financial Risk - QCC MCP Enhanced (Lines 72-115)**
   - 财产受限风险监控
   - 税务状态变化监控
   - 破产信号监控
   - 财务数据可见性替代方案

3. **Operational Risk - QCC MCP Signals (Lines 117-135)**
   - QCC MCP企业基座监控
   - 经营异常实时扫描

4. **Hot Signal Protocol (Lines 175-195)**
   - 6类HOT信号定义
   - 自动升级处理流程
   - 紧急行动模板

#### 修改部分

- **Universal Rules**: 新增第5、6条关于QCC MCP的规则
- **Data Sources**: 更新为 "QCC MCP Risk Control, QCC MCP Enterprise, Web Search, ERP, QMS"
- **Never Do**: 新增关于Companies House/Creditsafe对中国供应商无效的规则

---

## 新增文件

### scripts/qcc_mcp_connector.py

**功能**: QCC MCP连接器（供应链专用版）

**核心类**:
- `QccMcpConnector`: 主连接器类
- `VendorInfo`: 供应商基本信息
- `VendorRiskProfile`: 供应商风险画像
- `RiskItem`: 风险项

**核心方法**:
- `verify_vendor()`: 实体锚定核验
- `check_judicial_risks()`: 司法风险扫描
- `check_operational_risks()`: 经营风险扫描
- `check_property_restrictions()`: 财产受限扫描
- `check_tax_risks()`: 税务风险扫描
- `get_financial_indicators()`: 财务指标获取
- `assess_vendor_risk()`: 完整风险评估
- `format_assessment_report()`: 报告格式化

**MCP Server映射**:
```python
MCP_SERVERS = {
    "enterprise": "企业基座",  # 工商信息、股权、经营异常
    "risk": "风控大脑",        # 司法、税务、行政处罚
    "ip": "知产引擎",          # 知识产权（预留）
    "business": "经营罗盘",    # 财务指标（预留）
}
```

---

## 安装脚本

### install_qcc_mcp_supply_chain.sh

**功能**: 一键安装QCC MCP增强版供应链插件

**特性**:
- 自动检测平台 (macOS/Linux)
- QCC MCP API Key配置引导
- 自动备份现有skill
- 依赖检查和安装提示

---

## 能力提升总结

### 原版能力
- ✅ 供应商分类 (Kraljic Matrix)
- ✅ 六维度评估框架
- ✅ 输出格式标准化
- ❌ 中国企业数据依赖西方源（Companies House, Creditsafe）
- ❌ 无中国企业覆盖

### QCC MCP增强版能力
- ✅ 供应商分类 (Kraljic Matrix)
- ✅ 六维度评估框架
- ✅ 输出格式标准化
- ✅ **中国企业实时核验**（实体锚定）
- ✅ **18类风险自动扫描**
- ✅ **财务替代指标**（股权/税务/破产）
- ✅ **实时风险监控**（HOT信号）
- ✅ **官方数据源**（SAMR/法院/税务）

---

## 风险覆盖对比

| 风险维度 | 原版覆盖 | QCC MCP覆盖 | 提升 |
|---------|---------|------------|------|
| 司法执行 | ❌ 无 | ✅ 6类 | 从无到有 |
| 经营异常 | ❌ 无 | ✅ 6类 | 从无到有 |
| 财产受限 | ❌ 无 | ✅ 3类 | 从无到有 |
| 税务违法 | ❌ 无 | ✅ 3类 | 从无到有 |
| 破产清算 | ❌ 无 | ✅ 2类 | 从无到有 |
| **总计** | **0类** | **18类** | **∞** |

---

## 使用方式对比

### 原版使用
```
请评估供应商: ABC Supplier Inc.
→ 使用 Companies House / Creditsafe (仅覆盖英美)
```

### QCC MCP增强版使用
```
请评估供应商: 华为技术有限公司
→ 自动识别中国供应商
→ 调用 QCC MCP 企业基座/风控大脑
→ 实体锚定 + 18类风险扫描
→ 生成评估报告
```

---

## 输出格式对比

### 原版输出
```
VENDOR ASSESSMENT: [Vendor Name]
-- COMMERCIAL --
-- OPERATIONAL --
-- FINANCIAL --
-- COMPLIANCE --
-- STRATEGIC --
-- GEOPOLITICAL --
RISK SUMMARY
```

### QCC MCP增强版输出
```
VENDOR ASSESSMENT: [Vendor Name]
-- ENTITY VERIFICATION (QCC MCP) --  ← 新增
-- COMMERCIAL --
-- OPERATIONAL --
-- FINANCIAL (QCC MCP Enhanced) --   ← 增强
-- COMPLIANCE --
-- STRATEGIC --
-- GEOPOLITICAL --
RISK SUMMARY
QCC MCP ASSESSMENT TRACE             ← 新增
```

---

## 兼容性说明

- **向下兼容**: QCC MCP增强版完全兼容原版所有功能
- **降级策略**: 无QCC MCP Key时自动降级为原版行为
- **数据源切换**: 自动识别供应商所属地区，选择合适数据源
- **格式兼容**: 输出格式保持与原版一致，新增QCC MCP追溯信息

---

## 迁移指南

### 从原版迁移到QCC MCP增强版

1. **备份现有配置**
   ```bash
   cp -r ~/.claude/skills/vendor-assessment ~/.claude/skills/vendor-assessment.backup
   cp -r ~/.claude/skills/supplier-risk ~/.claude/skills/supplier-risk.backup
   ```

2. **安装增强版**
   ```bash
   bash install_qcc_mcp_supply_chain.sh
   ```

3. **配置QCC MCP Key**（可选但推荐）
   ```bash
   export QCC_MCP_API_KEY="your_key_here"
   ```

4. **验证安装**
   ```
   /vendor-assess 华为技术有限公司
   ```

---

## 总结

QCC MCP增强版在保持原版所有功能的基础上，通过集成企查查MCP，为中国供应商评估带来了：

1. **实体锚定**: 统一社会信用代码强制验证，消除名称幻觉
2. **18类风险**: 覆盖司法、经营、财产、税务、破产全维度
3. **财务替代**: 非上市公司也能评估财务健康状况
4. **实时监控**: HOT信号自动推送，风险预警不滞后
5. **官方数据**: 直连国家企业信用信息公示系统等权威源

这是供应链供应商管理的**革命性升级**，从"问卷调查"到"数据驱动尽调"。
