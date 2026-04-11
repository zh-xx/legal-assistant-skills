# QCC MCP Supply Chain Plugin - 快速参考

## 优化完成总结

**Supply Chain 版本已明确区分于 Contract Review**

---

## 核心区别

| | Contract Review | Supply Chain |
|--|-----------------|--------------|
| **目标** | 合同主体合规 | 供应商持续供货能力 |
| **18类风险** | ✅ 基础覆盖 | ✅ 基础覆盖 + 重新分级 |
| **特有维度** | ❌ 无 | ✅ 3个新增维度 |
| **响应时间** | 标准流程 | 供应中断信号 < 4小时 |

---

## 9维度风险评估 (Supply Chain)

```
基础4维度              供应链特有3维度
├─ 财务风险            ├─ 产能资质风险 ⭐NEW
├─ 经营风险            │   └─ 生产许可、质量认证
├─ 合规风险            │   └─ 行业资质、许可证
├─ 法律风险            │
                       ├─ 组织稳定性风险 ⭐NEW
                       │   └─ 股权变更、法人变更
                       │   └─ 单点产能风险
                       │
                       └─ 业务健康度风险 ⭐NEW
                           └─ 信用评级、招投标
                           └─ 抽检记录、负面舆情
```

---

## 18类风险供应链优先级

### 🔴 CRITICAL (< 4小时响应)
- 破产重整、失信、被执行人、环保停产、经营异常

### 🔴 HIGH (< 48小时响应)
- 严重违法、注销备案、股权冻结、限高

### 🟡 MEDIUM (< 7天响应)
- 股权出质、欠税、税务异常、终本案件

### 🔵 LOW (< 30天响应)
- 一般行政处罚

---

## MCP Server 调用对比

| Server | Contract Review | Supply Chain (新增) |
|--------|-----------------|---------------------|
| risk | 18类风险查询 | 同左，重新分级 |
| enterprise | 基础工商信息 | **+变更记录、分支机构** |
| business | ❌ 不调用 | **+资质证书、行政许可** |
| | | **+招投标、信用评级** |
| | | **+抽查记录** |

**新增7个MCP工具调用**

---

## 代码使用示例

```python
from qcc_mcp_connector import QccMcpConnector

connector = QccMcpConnector()

# 完整评估 (含9维度)
profile = connector.assess_vendor_risk("华为技术有限公司")

# 访问全部9维度
print(f"财务风险: {profile.financial_risk}")
print(f"产能资质风险: {profile.capacity_risk}")      # NEW
print(f"组织稳定性风险: {profile.stability_risk}")   # NEW
print(f"业务健康度风险: {profile.business_health_risk}")  # NEW

# 访问供应链特有数据
print(f"资质证书: {profile.qualifications}")
print(f"信用评级: {profile.credit_rating}")

# 单独评估供应链特有维度
capacity = connector.assess_capacity_and_qualification("供应商名称")
print(f"生产许可: {capacity.has_production_license}")
print(f"ISO认证: {capacity.quality_certifications}")

stability = connector.assess_organizational_stability("供应商名称")
print(f"股权变更: {stability.major_shareholder_changes_6m}次/6个月")
print(f"单点风险: {stability.single_site_risk}")

health = connector.assess_business_health("供应商名称")
print(f"信用评级: {health.official_credit_rating}")
print(f"招投标趋势: {health.bidding_trend}")
```

---

## Claude Code 使用

```bash
# 供应商评估 (9维度)
/vendor-assessment-qcc 华为技术有限公司

# 风险监控 (分级响应)
/supplier-risk-qcc 阿里巴巴集团
```

---

## 关键文件

| 文件 | 说明 |
|------|------|
| `OPTIMIZATION_SUMMARY.md` | 详细优化总结 |
| `SUPPLY_CHAIN_RISKS.md` | 风险设计原理 |
| `skills/vendor-assessment/SKILL.md` | 评估技能定义 |
| `skills/supplier-risk/SKILL.md` | 监控技能定义 |
| `scripts/qcc_mcp_connector.py` | 核心连接器代码 |

---

## 验证完成 ✅

- ✅ 代码语法检查通过
- ✅ 9维度评估模型完整
- ✅ 供应链特有数据类实现
- ✅ MCP调用扩展实现
- ✅ SKILL.md 格式正确

**Supply Chain 版本已准备就绪！**
