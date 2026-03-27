#!/usr/bin/env python3
"""
QCC MCP Supply Chain Plugin - Example Usage
企查查MCP供应链增强版 - 使用示例

此示例展示如何使用QCC MCP连接器评估供应商
"""

import sys
import os

# 添加脚本路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from qcc_mcp_connector import QccMcpConnector, VendorRiskProfile, RiskLevel


def demo_basic_assessment():
    """示例1: 基础供应商评估"""
    print("=" * 64)
    print("示例1: 基础供应商评估")
    print("=" * 64)
    print()

    # 初始化连接器
    try:
        connector = QccMcpConnector()
    except ValueError as e:
        print(f"配置错误: {e}")
        print("\n请设置环境变量:")
        print("  export QCC_MCP_API_KEY='your_key_here'")
        return

    # 评估供应商
    vendor_name = "华为技术有限公司"
    print(f"正在评估供应商: {vendor_name}")
    print()

    profile = connector.assess_vendor_risk(vendor_name)

    # 输出基本信息
    print(f"供应商名称: {profile.vendor_name}")
    print(f"统一社会信用代码: {profile.credit_code}")
    print(f"整体风险等级: {profile.overall_risk.value}")
    print()

    # 输出各维度风险
    print("各维度风险等级:")
    print(f"  财务风险: {profile.financial_risk.value}")
    print(f"  经营风险: {profile.operational_risk.value}")
    print(f"  合规风险: {profile.compliance_risk.value}")
    print(f"  法律风险: {profile.legal_risk.value}")
    print()

    # 输出风险详情
    if profile.risks:
        print(f"发现 {len(profile.risks)} 项风险信号:")
        for i, risk in enumerate(profile.risks, 1):
            print(f"\n{i}. [{risk.severity.value}] {risk.category} - {risk.type}")
            print(f"   描述: {risk.description}")
            if risk.date:
                print(f"   日期: {risk.date}")
    else:
        print("未发现显著风险信号")

    print()


def demo_detailed_report():
    """示例2: 生成详细评估报告"""
    print("=" * 64)
    print("示例2: 生成详细评估报告")
    print("=" * 64)
    print()

    try:
        connector = QccMcpConnector()
    except ValueError as e:
        print(f"配置错误: {e}")
        return

    vendor_name = "阿里巴巴集团"
    print(f"正在生成报告: {vendor_name}")
    print()

    profile = connector.assess_vendor_risk(vendor_name)
    report = connector.format_assessment_report(profile)

    print(report)


def demo_specific_checks():
    """示例3: 单独检查特定风险"""
    print("=" * 64)
    print("示例3: 单独检查特定风险类型")
    print("=" * 64)
    print()

    try:
        connector = QccMcpConnector()
    except ValueError as e:
        print(f"配置错误: {e}")
        return

    vendor_name = "腾讯科技（深圳）有限公司"
    print(f"检查供应商: {vendor_name}")
    print()

    # 检查司法风险
    print("1. 司法风险扫描...")
    judicial_risks = connector.check_judicial_risks(vendor_name)
    print(f"   发现 {len(judicial_risks)} 项司法风险")
    for risk in judicial_risks:
        print(f"   - [{risk.severity.value}] {risk.type}: {risk.description}")
    print()

    # 检查税务风险
    print("2. 税务风险扫描...")
    tax_risks = connector.check_tax_risks(vendor_name)
    print(f"   发现 {len(tax_risks)} 项税务风险")
    for risk in tax_risks:
        print(f"   - [{risk.severity.value}] {risk.type}: {risk.description}")
    print()

    # 获取财务指标
    print("3. 财务指标查询...")
    financial = connector.get_financial_indicators(vendor_name)
    if financial.get("status") == "available":
        print(f"   营业收入: {financial.get('revenue', 'N/A')}")
        print(f"   净利润: {financial.get('profit', 'N/A')}")
        print(f"   总资产: {financial.get('assets', 'N/A')}")
    else:
        print(f"   {financial.get('message', '财务数据暂不可见')}")
        print(f"   建议: {financial.get('alternative_action', '')}")

    print()


def demo_multiple_vendors():
    """示例4: 批量评估多个供应商"""
    print("=" * 64)
    print("示例4: 批量评估多个供应商")
    print("=" * 64)
    print()

    try:
        connector = QccMcpConnector()
    except ValueError as e:
        print(f"配置错误: {e}")
        return

    vendors = [
        "华为技术有限公司",
        "比亚迪股份有限公司",
        "小米科技有限责任公司",
    ]

    results = []
    for vendor in vendors:
        print(f"评估中: {vendor}...", end=" ")
        profile = connector.assess_vendor_risk(vendor)
        results.append({
            "name": vendor,
            "risk": profile.overall_risk.value,
            "risk_count": len(profile.risks)
        })
        print(f"完成 [{profile.overall_risk.value}]")

    print()
    print("=" * 64)
    print("批量评估结果汇总")
    print("=" * 64)
    print()
    print(f"{'供应商名称':<30} {'风险等级':<12} {'风险数量'}")
    print("-" * 64)
    for result in results:
        print(f"{result['name']:<30} {result['risk']:<12} {result['risk_count']}")

    print()


def main():
    """主函数 - 运行所有示例"""
    print()
    print("╔" + "=" * 62 + "╗")
    print("║" + " " * 14 + "QCC MCP Supply Chain Plugin" + " " * 23 + "║")
    print("║" + " " * 10 + "企查查MCP供应链增强版 - 使用示例" + " " * 16 + "║")
    print("╚" + "=" * 62 + "╝")
    print()

    # 运行示例
    examples = [
        ("基础评估", demo_basic_assessment),
        ("详细报告", demo_detailed_report),
        ("特定检查", demo_specific_checks),
        ("批量评估", demo_multiple_vendors),
    ]

    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except KeyboardInterrupt:
            print("\n用户中断")
            break
        except Exception as e:
            print(f"\n示例{i}出错: {e}")

        if i < len(examples):
            input("\n按Enter继续下一个示例...")
            print()

    print()
    print("=" * 64)
    print("示例运行完成!")
    print("=" * 64)
    print()
    print("更多用法请参考:")
    print("  - README.md - 详细文档")
    print("  - CHANGES.md - 变更说明")
    print("  - SKILL.md - 技能定义")
    print()


if __name__ == "__main__":
    main()
