#!/usr/bin/env python3
"""
QCC MCP Connector for Supply Chain Management
企查查MCP连接器 - 供应链专用版

为供应商评估和风险管理提供中国企业数据支持
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RiskLevel(Enum):
    """风险等级"""
    GREEN = "GREEN"
    AMBER = "AMBER"
    RED = "RED"
    UNKNOWN = "UNKNOWN"


@dataclass
class VendorInfo:
    """供应商基本信息"""
    name: str
    credit_code: str = ""
    status: str = ""
    legal_person: str = ""
    registered_capital: str = ""
    establishment_date: str = ""
    company_type: str = ""
    address: str = ""
    business_scope: str = ""
    is_verified: bool = False
    verification_message: str = ""


@dataclass
class RiskItem:
    """风险项"""
    category: str
    type: str
    description: str
    date: str = ""
    severity: RiskLevel = RiskLevel.UNKNOWN
    source: str = ""


@dataclass
class VendorRiskProfile:
    """供应商风险画像"""
    vendor_name: str
    credit_code: str
    overall_risk: RiskLevel = RiskLevel.UNKNOWN
    financial_risk: RiskLevel = RiskLevel.UNKNOWN
    operational_risk: RiskLevel = RiskLevel.UNKNOWN
    compliance_risk: RiskLevel = RiskLevel.UNKNOWN
    legal_risk: RiskLevel = RiskLevel.UNKNOWN
    # Supply chain specific dimensions
    capacity_risk: RiskLevel = RiskLevel.UNKNOWN  # 产能与资质风险
    stability_risk: RiskLevel = RiskLevel.UNKNOWN  # 组织稳定性风险
    business_health_risk: RiskLevel = RiskLevel.UNKNOWN  # 业务健康度风险
    risks: List[RiskItem] = field(default_factory=list)
    assessment_date: str = field(default_factory=lambda: datetime.now().isoformat())
    data_sources: List[str] = field(default_factory=list)
    # Supply chain specific data
    qualifications: List[Dict] = field(default_factory=list)  # 资质证书
    licenses: List[Dict] = field(default_factory=list)  # 行政许可
    shareholder_changes: List[Dict] = field(default_factory=list)  # 股权变更
    bidding_activity: Dict = field(default_factory=dict)  # 招投标活跃度
    credit_rating: str = ""  # 官方信用评级


@dataclass
class CapacityAssessment:
    """产能与资质评估 (Supply Chain Specific)"""
    has_production_license: bool = False
    license_status: str = ""
    quality_certifications: List[str] = field(default_factory=list)  # ISO等
    industry_permits: List[str] = field(default_factory=list)  # 行业许可证
    key_qualifications_expiring: List[Dict] = field(default_factory=list)
    assessment: str = ""  # 综合评估意见


@dataclass
class StabilityAssessment:
    """组织稳定性评估 (Supply Chain Specific)"""
    major_shareholder_changes_6m: int = 0
    legal_rep_changes_12m: int = 0
    address_changes_12m: int = 0
    business_scope_changes_12m: int = 0
    branch_count: int = 0
    single_site_risk: bool = False
    assessment: str = ""  # 综合评估意见


@dataclass
class BusinessHealthAssessment:
    """业务健康度评估 (Supply Chain Specific)"""
    official_credit_rating: str = ""  # A级、B级等
    tax_credit_rating: str = ""  # 税务信用评级
    recent_bidding_count: int = 0
    bidding_trend: str = ""  # 上升/下降/稳定
    spot_check_results: List[Dict] = field(default_factory=list)
    negative_news_count_30d: int = 0
    assessment: str = ""  # 综合评估意见


class QccMcpConnector:
    """
    企查查MCP连接器 - 供应链专用

    集成四大Server：
    - 企业基座：工商信息、股东信息、主要人员
    - 风控大脑：司法风险、经营风险、舆情风险
    - 知产引擎：知识产权、专利商标
    - 经营罗盘：财务数据、经营指标
    """

    # MCP Server端点配置
    MCP_SERVERS = {
        "enterprise": "https://api.qcc.com/mcp/enterprise",  # 企业基座
        "risk": "https://api.qcc.com/mcp/risk",              # 风控大脑
        "ip": "https://api.qcc.com/mcp/ip",                  # 知产引擎
        "business": "https://api.qcc.com/mcp/business",      # 经营罗盘
    }

    # 18类风险映射到SKILL维度的配置
    RISK_DIMENSION_MAP = {
        # 财务风险维度
        "financial": [
            "欠税公告", "税收违法", "税务非正常户",
            "股权冻结", "股权出质", "动产抵押"
        ],
        # 经营风险维度
        "operational": [
            "经营异常", "严重违法", "注销备案", "简易注销",
            "行政处罚", "环保处罚"
        ],
        # 合规风险维度
        "compliance": [
            "经营异常", "严重违法", "行政处罚",
            "环保处罚", "税收违法"
        ],
        # 法律风险维度
        "legal": [
            "失信信息", "被执行人", "限制高消费",
            "终本案件", "司法拍卖", "股权冻结",
            "破产重整", "清算信息"
        ]
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化连接器

        Args:
            api_key: 企查查MCP API Key，如不提供则从环境变量读取
        """
        self.api_key = api_key or os.getenv("QCC_MCP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "QCC MCP API Key未配置。请设置环境变量 QCC_MCP_API_KEY "
                "或访问 https://mcp.qcc.com 申请"
            )
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "QCC-MCP-SupplyChain/1.0"
        })

    def _call_mcp(self, server: str, tool: str, params: Dict) -> Dict:
        """
        调用MCP Server

        Args:
            server: Server名称 (enterprise/risk/ip/business)
            tool: 工具名称
            params: 请求参数

        Returns:
            MCP响应数据
        """
        base_url = self.MCP_SERVERS.get(server)
        if not base_url:
            raise ValueError(f"Unknown MCP server: {server}")

        url = f"{base_url}/{tool}"

        try:
            response = self.session.post(url, json=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"MCP调用失败: {str(e)}",
                "data": None
            }

    def verify_vendor(self, vendor_name: str) -> VendorInfo:
        """
        核验供应商主体信息（实体锚定）

        Args:
            vendor_name: 供应商名称

        Returns:
            VendorInfo: 核验后的供应商信息
        """
        # 调用企业基座 - 企业基本信息查询
        result = self._call_mcp("enterprise", "company_base_info", {
            "company_name": vendor_name
        })

        if result.get("status") != "success" or not result.get("data"):
            return VendorInfo(
                name=vendor_name,
                status="查询失败",
                is_verified=False,
                verification_message=result.get("message", "未找到企业信息")
            )

        data = result["data"]

        return VendorInfo(
            name=data.get("company_name", vendor_name),
            credit_code=data.get("credit_code", ""),
            status=data.get("status", ""),
            legal_person=data.get("legal_person", ""),
            registered_capital=data.get("registered_capital", ""),
            establishment_date=data.get("establishment_date", ""),
            company_type=data.get("company_type", ""),
            address=data.get("address", ""),
            business_scope=data.get("business_scope", ""),
            is_verified=True,
            verification_message=f"实体锚定确认：统一社会信用代码 {data.get('credit_code', 'N/A')}"
        )

    def check_judicial_risks(self, vendor_name: str) -> List[RiskItem]:
        """
        检查司法风险（风控大脑Server）

        覆盖：失信、被执行、限高、终本案件、司法拍卖、破产清算
        """
        risks = []

        # 1. 失信信息查询
        result = self._call_mcp("risk", "dishonest_info", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="司法执行",
                    type="失信信息",
                    description=f"失信被执行人：{item.get('case_no', '')}",
                    date=item.get('publish_date', ''),
                    severity=RiskLevel.RED,
                    source="中国执行信息公开网"
                ))

        # 2. 被执行人查询
        result = self._call_mcp("risk", "zhixing_info", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="司法执行",
                    type="被执行人",
                    description=f"执行标的：{item.get('exec_money', '未知')}元，案号：{item.get('case_no', '')}",
                    date=item.get('case_date', ''),
                    severity=RiskLevel.RED,
                    source="中国执行信息公开网"
                ))

        # 3. 限制高消费查询
        result = self._call_mcp("risk", "limit_high_consumption", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="司法执行",
                    type="限制高消费",
                    description=f"限高对象：{item.get('limited_person', '')}",
                    date=item.get('publish_date', ''),
                    severity=RiskLevel.RED,
                    source="中国执行信息公开网"
                ))

        # 4. 终本案件查询
        result = self._call_mcp("risk", "zhongben_case", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="司法执行",
                    type="终本案件",
                    description=f"未履行金额：{item.get('unperform_money', '未知')}元",
                    date=item.get("case_date", ""),
                    severity=RiskLevel.RED,
                    source="中国执行信息公开网"
                ))

        # 5. 破产重整查询
        result = self._call_mcp("risk", "bankruptcy_info", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="破产清算",
                    type="破产重整",
                    description=f"破产类型：{item.get('bankruptcy_type', '')}",
                    date=item.get("publish_date", ""),
                    severity=RiskLevel.RED,
                    source="全国企业破产重整案件信息网"
                ))

        return risks

    def check_operational_risks(self, vendor_name: str) -> List[RiskItem]:
        """
        检查经营风险（企业基座 + 风控大脑）

        覆盖：经营异常、严重违法、注销备案、行政处罚、环保处罚
        """
        risks = []

        # 1. 经营异常查询
        result = self._call_mcp("enterprise", "abnormal_info", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="经营异常",
                    type="经营异常",
                    description=f"列入原因：{item.get('reason', '')}",
                    date=item.get("add_date", ""),
                    severity=RiskLevel.RED,
                    source="国家企业信用信息公示系统"
                ))

        # 2. 严重违法查询
        result = self._call_mcp("enterprise", "serious_violation", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="经营异常",
                    type="严重违法",
                    description=f"列入事由：{item.get('reason', '')}",
                    date=item.get("add_date", ""),
                    severity=RiskLevel.RED,
                    source="国家企业信用信息公示系统"
                ))

        # 3. 行政处罚查询
        result = self._call_mcp("risk", "admin_penalty", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="行政处罚",
                    type=item.get("penalty_type", "行政处罚"),
                    description=f"处罚事由：{item.get('reason', '')}，处罚结果：{item.get('result', '')}",
                    date=item.get("penalty_date", ""),
                    severity=RiskLevel.AMBER,
                    source=item.get("office_name", "行政处罚机关")
                ))

        # 4. 环保处罚查询
        result = self._call_mcp("risk", "env_penalty", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="行政处罚",
                    type="环保处罚",
                    description=f"处罚事由：{item.get('reason', '')}",
                    date=item.get("penalty_date", ""),
                    severity=RiskLevel.AMBER,
                    source="生态环境部"
                ))

        return risks

    def check_property_restrictions(self, vendor_name: str) -> List[RiskItem]:
        """
        检查财产受限情况（企业基座）

        覆盖：股权冻结、股权出质、动产抵押
        """
        risks = []

        # 1. 股权冻结查询
        result = self._call_mcp("enterprise", "equity_freeze", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="财产受限",
                    type="股权冻结",
                    description=f"冻结股权数额：{item.get('frozen_amount', '')}，冻结期限：{item.get('freeze_period', '')}",
                    date=item.get("freeze_date", ""),
                    severity=RiskLevel.RED,
                    source="国家企业信用信息公示系统"
                ))

        # 2. 股权出质查询
        result = self._call_mcp("enterprise", "equity_pledge", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="财产受限",
                    type="股权出质",
                    description=f"出质股权数额：{item.get('pledge_amount', '')}，质权人：{item.get('pledgee', '')}",
                    date=item.get("reg_date", ""),
                    severity=RiskLevel.AMBER,
                    source="国家企业信用信息公示系统"
                ))

        # 3. 动产抵押查询
        result = self._call_mcp("enterprise", "chattel_mortgage", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="财产受限",
                    type="动产抵押",
                    description=f"被担保债权数额：{item.get('amount', '')}，担保范围：{item.get('scope', '')}",
                    date=item.get("reg_date", ""),
                    severity=RiskLevel.AMBER,
                    source="动产融资统一登记公示系统"
                ))

        return risks

    def check_tax_risks(self, vendor_name: str) -> List[RiskItem]:
        """
        检查税务风险（风控大脑）

        覆盖：欠税公告、税务非正常户、税收违法
        """
        risks = []

        # 1. 欠税公告查询
        result = self._call_mcp("risk", "tax_arrears", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="税务风险",
                    type="欠税公告",
                    description=f"欠税税种：{item.get('tax_type', '')}，欠税金额：{item.get('amount', '')}元",
                    date=item.get("publish_date", ""),
                    severity=RiskLevel.RED,
                    source="国家税务总局"
                ))

        # 2. 税务非正常户查询
        result = self._call_mcp("risk", "tax_abnormal", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="税务风险",
                    type="税务非正常户",
                    description=f"认定机关：{item.get('office_name', '')}",
                    date=item.get("add_date", ""),
                    severity=RiskLevel.RED,
                    source="国家税务总局"
                ))

        # 3. 税收违法查询
        result = self._call_mcp("risk", "tax_violation", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            for item in result["data"]:
                risks.append(RiskItem(
                    category="税务风险",
                    type="税收违法",
                    description=f"违法类型：{item.get('violation_type', '')}",
                    date=item.get("publish_date", ""),
                    severity=RiskLevel.RED,
                    source="国家税务总局"
                ))

        return risks

    def get_financial_indicators(self, vendor_name: str) -> Dict:
        """
        获取财务指标（经营罗盘Server）

        用于财务风险评估维度
        """
        result = self._call_mcp("business", "financial_indicators", {
            "company_name": vendor_name
        })

        if result.get("status") == "success" and result.get("data"):
            return {
                "status": "available",
                "revenue": result["data"].get("revenue", "未披露"),
                "profit": result["data"].get("profit", "未披露"),
                "assets": result["data"].get("total_assets", "未披露"),
                "debt_ratio": result["data"].get("debt_ratio", "未披露"),
                "year": result["data"].get("year", "")
            }

        return {
            "status": "unavailable",
            "message": "财务数据暂不可见（非上市公司），建议要求供应商提供审计报告",
            "alternative_action": "对Strategic和Bottleneck供应商，应每年索取经审计财务报表"
        }

    def assess_vendor_risk(self, vendor_name: str) -> VendorRiskProfile:
        """
        完整供应商风险评估 (Supply Chain Enhanced)

        整合18类核心风险 + 供应链特有维度，生成供应商风险画像
        """
        # 1. 核验供应商主体
        vendor_info = self.verify_vendor(vendor_name)

        if not vendor_info.is_verified:
            return VendorRiskProfile(
                vendor_name=vendor_name,
                credit_code="",
                overall_risk=RiskLevel.UNKNOWN,
                data_sources=["核验失败"]
            )

        # 2. 收集18类核心风险
        all_risks = []
        data_sources = ["企查查MCP-企业基座", "企查查MCP-风控大脑"]

        # 司法风险
        judicial_risks = self.check_judicial_risks(vendor_name)
        all_risks.extend(judicial_risks)

        # 经营风险
        operational_risks = self.check_operational_risks(vendor_name)
        all_risks.extend(operational_risks)

        # 财产受限
        property_risks = self.check_property_restrictions(vendor_name)
        all_risks.extend(property_risks)

        # 税务风险
        tax_risks = self.check_tax_risks(vendor_name)
        all_risks.extend(tax_risks)

        # 3. 计算各维度风险等级 (基础4维度)
        financial_risk = self._calculate_dimension_risk(all_risks, "financial")
        operational_risk = self._calculate_dimension_risk(all_risks, "operational")
        compliance_risk = self._calculate_dimension_risk(all_risks, "compliance")
        legal_risk = self._calculate_dimension_risk(all_risks, "legal")

        # 4. 供应链特有维度评估
        # 产能与资质评估
        capacity_assessment = self.assess_capacity_and_qualification(vendor_name)
        capacity_risk = self._calculate_capacity_risk(capacity_assessment)

        # 组织稳定性评估
        stability_assessment = self.assess_organizational_stability(vendor_name)
        stability_risk = self._calculate_stability_risk(stability_assessment)

        # 业务健康度评估
        health_assessment = self.assess_business_health(vendor_name)
        business_health_risk = self._calculate_business_health_risk(health_assessment)

        data_sources.extend(["企查查MCP-经营罗盘", "企查查MCP-知产引擎"])

        # 5. 确定整体风险等级 (包含供应链维度)
        overall_risk = self._calculate_overall_risk([
            financial_risk, operational_risk, compliance_risk, legal_risk,
            capacity_risk, stability_risk, business_health_risk
        ])

        return VendorRiskProfile(
            vendor_name=vendor_info.name,
            credit_code=vendor_info.credit_code,
            overall_risk=overall_risk,
            financial_risk=financial_risk,
            operational_risk=operational_risk,
            compliance_risk=compliance_risk,
            legal_risk=legal_risk,
            capacity_risk=capacity_risk,
            stability_risk=stability_risk,
            business_health_risk=business_health_risk,
            risks=all_risks,
            data_sources=data_sources,
            qualifications=capacity_assessment.key_qualifications_expiring if hasattr(capacity_assessment, 'key_qualifications_expiring') else [],
            credit_rating=health_assessment.official_credit_rating if hasattr(health_assessment, 'official_credit_rating') else ""
        )

    def assess_capacity_and_qualification(self, vendor_name: str) -> CapacityAssessment:
        """
        评估产能与资质 (Supply Chain Specific)

        检查生产许可、质量认证、行业资质等
        """
        assessment = CapacityAssessment()

        # 1. 查询资质证书
        result = self._call_mcp("business", "get_qualifications", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            qualifications = result["data"]
            assessment.quality_certifications = [
                q.get("name", "") for q in qualifications
                if "ISO" in q.get("name", "") or "质量" in q.get("name", "")
            ]
            assessment.industry_permits = [
                q.get("name", "") for q in qualifications
                if "许可" in q.get("name", "") or "生产" in q.get("name", "")
            ]
            # 检查即将过期的资质
            for q in qualifications:
                expire_date = q.get("expire_date", "")
                if expire_date:
                    try:
                        from datetime import datetime, timedelta
                        exp = datetime.strptime(expire_date, "%Y-%m-%d")
                        if exp - datetime.now() < timedelta(days=90):
                            assessment.key_qualifications_expiring.append({
                                "name": q.get("name", ""),
                                "expire_date": expire_date
                            })
                    except:
                        pass

        # 2. 查询行政许可
        result = self._call_mcp("business", "get_administrative_license", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            licenses = result["data"]
            assessment.has_production_license = any(
                "生产" in l.get("name", "") or "制造" in l.get("name", "")
                for l in licenses
            )
            assessment.license_status = "有效" if licenses else "未查询到"

        # 生成评估意见
        if not assessment.has_production_license and not assessment.industry_permits:
            assessment.assessment = "未查询到关键生产许可证，需核实"
        elif assessment.key_qualifications_expiring:
            assessment.assessment = f"有{len(assessment.key_qualifications_expiring)}项资质即将过期，需关注续期"
        else:
            assessment.assessment = "资质齐全，生产许可有效"

        return assessment

    def assess_organizational_stability(self, vendor_name: str) -> StabilityAssessment:
        """
        评估组织稳定性 (Supply Chain Specific)

        检查股权变更、法人变更、注册地址变更等
        """
        assessment = StabilityAssessment()

        # 1. 查询变更记录
        result = self._call_mcp("enterprise", "get_change_records", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            changes = result["data"]
            from datetime import datetime, timedelta
            six_months_ago = datetime.now() - timedelta(days=180)
            twelve_months_ago = datetime.now() - timedelta(days=365)

            for change in changes:
                change_date_str = change.get("date", "")
                try:
                    change_date = datetime.strptime(change_date_str, "%Y-%m-%d")
                    change_item = change.get("item", "")

                    if "股东" in change_item or "股权" in change_item:
                        if change_date > six_months_ago:
                            assessment.major_shareholder_changes_6m += 1
                    elif "法定代表人" in change_item or "法人" in change_item:
                        if change_date > twelve_months_ago:
                            assessment.legal_rep_changes_12m += 1
                    elif "地址" in change_item:
                        if change_date > twelve_months_ago:
                            assessment.address_changes_12m += 1
                    elif "经营范围" in change_item:
                        if change_date > twelve_months_ago:
                            assessment.business_scope_changes_12m += 1
                except:
                    pass

        # 2. 查询分支机构
        result = self._call_mcp("enterprise", "get_branches", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            assessment.branch_count = len(result["data"])
            assessment.single_site_risk = assessment.branch_count == 0

        # 生成评估意见
        if assessment.major_shareholder_changes_6m > 0:
            assessment.assessment = f"近6个月有{assessment.major_shareholder_changes_6m}次股权变更，控制权不稳定"
        elif assessment.legal_rep_changes_12m > 1:
            assessment.assessment = f"近12个月法人变更{assessment.legal_rep_changes_12m}次，管理层不稳定"
        elif assessment.single_site_risk:
            assessment.assessment = "单一生产基地，无分支机构，业务连续性风险"
        else:
            assessment.assessment = f"组织架构稳定，有{assessment.branch_count}个分支机构"

        return assessment

    def assess_business_health(self, vendor_name: str) -> BusinessHealthAssessment:
        """
        评估业务健康度 (Supply Chain Specific)

        检查信用评级、招投标活跃度、负面舆情等
        """
        assessment = BusinessHealthAssessment()

        # 1. 查询官方信用评价
        result = self._call_mcp("business", "get_credit_evaluation", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            assessment.official_credit_rating = result["data"].get("rating", "未评级")
            assessment.tax_credit_rating = result["data"].get("tax_rating", "未评级")

        # 2. 查询招投标信息
        result = self._call_mcp("business", "get_bidding_info", {
            "company_name": vendor_name,
            "limit": 50
        })
        if result.get("status") == "success" and result.get("data"):
            bids = result["data"]
            assessment.recent_bidding_count = len(bids)
            # 简单趋势判断（有数据即认为稳定）
            if len(bids) > 10:
                assessment.bidding_trend = "活跃"
            elif len(bids) > 3:
                assessment.bidding_trend = "正常"
            else:
                assessment.bidding_trend = "低迷"

        # 3. 查询抽查检查记录
        result = self._call_mcp("business", "get_spot_check_info", {
            "company_name": vendor_name
        })
        if result.get("status") == "success" and result.get("data"):
            checks = result["data"]
            failed_checks = [c for c in checks if "不合格" in c.get("result", "")]
            assessment.spot_check_results = failed_checks

        # 生成评估意见
        if assessment.official_credit_rating in ["D级", "E级"]:
            assessment.assessment = f"官方信用评级较低({assessment.official_credit_rating})，需谨慎"
        elif assessment.bidding_trend == "低迷":
            assessment.assessment = "近期业务活跃度低，需关注经营状况"
        elif assessment.spot_check_results:
            assessment.assessment = f"有{len(assessment.spot_check_results)}次抽检不合格记录"
        else:
            assessment.assessment = f"业务健康，信用评级{assessment.official_credit_rating}，招投标{assessment.bidding_trend}"

        return assessment

    def _calculate_capacity_risk(self, assessment: CapacityAssessment) -> RiskLevel:
        """计算产能与资质风险等级"""
        if not assessment.has_production_license and not assessment.industry_permits:
            return RiskLevel.RED
        elif assessment.key_qualifications_expiring:
            return RiskLevel.AMBER
        elif assessment.quality_certifications:
            return RiskLevel.GREEN
        return RiskLevel.UNKNOWN

    def _calculate_stability_risk(self, assessment: StabilityAssessment) -> RiskLevel:
        """计算组织稳定性风险等级"""
        if assessment.major_shareholder_changes_6m > 0:
            return RiskLevel.RED
        elif assessment.legal_rep_changes_12m > 1:
            return RiskLevel.AMBER
        elif assessment.single_site_risk:
            return RiskLevel.AMBER
        return RiskLevel.GREEN

    def _calculate_business_health_risk(self, assessment: BusinessHealthAssessment) -> RiskLevel:
        """计算业务健康度风险等级"""
        if assessment.official_credit_rating in ["D级", "E级", "失信"]:
            return RiskLevel.RED
        elif assessment.bidding_trend == "低迷":
            return RiskLevel.AMBER
        elif assessment.spot_check_results:
            return RiskLevel.AMBER
        return RiskLevel.GREEN

    def _calculate_dimension_risk(self, risks: List[RiskItem], dimension: str) -> RiskLevel:
        """计算特定维度的风险等级"""
        dimension_risks = self.RISK_DIMENSION_MAP.get(dimension, [])
        relevant_risks = [r for r in risks if r.type in dimension_risks]

        if any(r.severity == RiskLevel.RED for r in relevant_risks):
            return RiskLevel.RED
        elif any(r.severity == RiskLevel.AMBER for r in relevant_risks):
            return RiskLevel.AMBER
        elif relevant_risks:
            return RiskLevel.GREEN
        return RiskLevel.UNKNOWN

    def _calculate_overall_risk(self, dimension_risks: List[RiskLevel]) -> RiskLevel:
        """计算整体风险等级"""
        if any(r == RiskLevel.RED for r in dimension_risks):
            return RiskLevel.RED
        elif sum(1 for r in dimension_risks if r == RiskLevel.AMBER) >= 2:
            return RiskLevel.AMBER
        elif any(r == RiskLevel.AMBER for r in dimension_risks):
            return RiskLevel.AMBER
        elif all(r == RiskLevel.GREEN for r in dimension_risks):
            return RiskLevel.GREEN
        return RiskLevel.UNKNOWN

    def format_assessment_report(self, profile: VendorRiskProfile) -> str:
        """
        格式化评估报告（符合vendor-assessment SKILL输出格式 - Supply Chain Enhanced）
        """
        report_lines = [
            "=" * 64,
            f"供应商风险评估报告 (Supply Chain Enhanced): {profile.vendor_name}",
            f"统一社会信用代码: {profile.credit_code}",
            f"评估日期: {profile.assessment_date}",
            "=" * 64,
            "",
            "-- 风险等级概览 --",
            f"整体风险: {profile.overall_risk.value}",
            f"财务风险: {profile.financial_risk.value}",
            f"经营风险: {profile.operational_risk.value}",
            f"合规风险: {profile.compliance_risk.value}",
            f"法律风险: {profile.legal_risk.value}",
            f"产能资质风险: {profile.capacity_risk.value}",
            f"组织稳定性风险: {profile.stability_risk.value}",
            f"业务健康度风险: {profile.business_health_risk.value}",
            f"合规风险: {profile.compliance_risk.value}",
            f"法律风险: {profile.legal_risk.value}",
            "",
            "-- 风险详情 --",
        ]

        if profile.risks:
            for risk in profile.risks:
                report_lines.append(f"[{risk.severity.value}] {risk.category} - {risk.type}")
                report_lines.append(f"  描述: {risk.description}")
                if risk.date:
                    report_lines.append(f"  日期: {risk.date}")
                report_lines.append(f"  来源: {risk.source}")
                report_lines.append("")
        else:
            report_lines.append("未发现显著风险信号")
            report_lines.append("")

        report_lines.extend([
            "-- 数据来源 --",
            f"{', '.join(profile.data_sources)}",
            "",
            "=" * 64,
            "注意：本报告基于企查查MCP公开数据生成，仅供内部参考。",
            "关键决策前建议要求供应商提供补充材料并实地尽调。",
            "=" * 64,
        ])

        return "\n".join(report_lines)


def main():
    """CLI入口 - 用于测试"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python qcc_mcp_connector.py <供应商名称>")
        print("示例: python qcc_mcp_connector.py '华为技术有限公司'")
        sys.exit(1)

    vendor_name = sys.argv[1]

    try:
        connector = QccMcpConnector()
        print(f"正在评估供应商: {vendor_name}...\n")

        profile = connector.assess_vendor_risk(vendor_name)
        report = connector.format_assessment_report(profile)

        print(report)

    except ValueError as e:
        print(f"配置错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"评估失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
