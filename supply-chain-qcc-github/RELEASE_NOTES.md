# Release Notes - QCC MCP Supply Chain Plugin v2.0

## 🎉 版本 2.0 - Supply Chain Enhanced

**发布日期**: 2024-03-24

### 主要更新

#### ✨ 新功能

1. **9维度评估模型**
   - 基础4维度：财务、经营、合规、法律
   - 供应链特有3维度：产能资质、组织稳定性、业务健康度

2. **18类风险供应链分级**
   - CRITICAL (< 4小时响应): 破产、失信、环保停产
   - HIGH (< 48小时响应): 严重违法、股权冻结
   - MEDIUM (< 7天响应): 欠税、股权出质
   - LOW (< 30天响应): 一般处罚

3. **7个新增MCP工具**
   - 资质证书查询
   - 行政许可查询
   - 招投标信息查询
   - 信用评级查询
   - 抽查检查记录查询
   - 变更记录查询
   - 分支机构查询

#### 🔧 改进

- 重新设计风险分类（供应链视角）
- 新增供应链特有数据类
- 优化评估报告格式
- 增加响应时间分级

#### 📚 文档

- 全新用户友好README
- 详细安装指南
- 常见问题解答
- 快速参考文档

---

## 📦 文件清单

### 核心文件
- `install_qcc_mcp_supply_chain.sh` - 一键安装脚本
- `example.py` - 使用示例
- `scripts/qcc_mcp_connector.py` - QCC MCP连接器

### Skill文件
- `skills/vendor-assessment/SKILL.md` - 供应商评估Skill
- `skills/supplier-risk/SKILL.md` - 风险监控Skill

### 文档文件
- `README.md` - 主文档
- `CHANGES.md` - 变更对比
- `OPTIMIZATION_SUMMARY.md` - 优化总结
- `SUPPLY_CHAIN_RISKS.md` - 风险设计原理
- `QUICK_REFERENCE.md` - 快速参考
- `RELEASE_NOTES.md` - 本文件

---

## 🚀 快速开始

```bash
# 安装
bash install_qcc_mcp_supply_chain.sh

# 配置
export QCC_MCP_API_KEY="your_api_key_here"

# 使用
/vendor-assessment-qcc 供应商名称
```

---

## 🙏 致谢

感谢 Panaversity 的原版 Supply Chain Plugin 和企查查MCP团队的支持。
