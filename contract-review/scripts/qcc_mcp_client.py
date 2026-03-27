#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企查查MCP服务客户端
支持4个服务：企业信息、风险信息、知识产权、经营信息
共65个工具，通过StreamableHTTP方式连接

使用方式：
1. 设置环境变量 QCC_MCP_API_KEY="your_api_key"
2. 初始化客户端: client = QccMcpClient()
3. 企业核验: client.verify_company("企业名称")
4. 风险排查: client.check_company_risk("企业名称")

降级策略：
- 如果未设置 QCC_MCP_API_KEY，所有方法返回 None
- 调用失败时返回包含 error 字段的字典
"""

import json
import os
import re
import requests
from typing import Dict, List, Any, Optional, Tuple


class QccMcpClient:
    """企查查MCP客户端 - 支持4个服务，65个工具

    服务分布:
    - company (企业信息): 12个工具
    - risk (风险信息): 34个工具
    - ipr (知识产权): 6个工具
    - operation (经营信息): 13个工具

    环境变量:
        QCC_MCP_API_KEY: 企查查MCP授权令牌
    """

    # MCP服务配置 - 完整65个工具
    SERVICES = {
        "company": {
            "name": "企业信息",
            "url": "https://mcp.qcc.com/data/company/stream",
            "tools": [
                "get_company_registration_info",   # 企业工商信息
                "get_shareholder_info",             # 股东信息
                "get_key_personnel",                # 主要人员
                "get_contact_info",                 # 联系方式
                "get_external_investments",         # 对外投资
                "get_change_records",               # 变更记录
                "get_branches",                     # 分支机构
                "get_company_profile",              # 企业简介
                "verify_company_accuracy",          # 企业准确性验证
                "get_annual_reports",               # 企业年度报告
                "get_listing_info",                 # 上市信息
                "get_tax_invoice_info",             # 税号开票信息
            ]
        },
        "risk": {
            "name": "风险信息",
            "url": "https://mcp.qcc.com/data/risk/stream",
            "tools": [
                # 核心风险（18类）
                "get_dishonest_info",               # 失信信息（老赖）
                "get_judgment_debtor_info",         # 被执行人
                "get_business_exception",           # 经营异常
                "get_equity_pledge_info",           # 股权出质
                "get_equity_freeze",                # 股权冻结
                "get_administrative_penalty",       # 行政处罚
                "get_case_filing_info",             # 立案信息
                "get_judicial_documents",           # 裁判文书
                "get_serious_violation",            # 严重违法
                # 扩展风险
                "get_bankruptcy_reorganization",    # 破产重整
                "get_cancellation_record_info",     # 注销备案
                "get_chattel_mortgage_info",        # 动产抵押
                "get_court_notice",                 # 法院公告
                "get_default_info",                 # 债券/票据违约
                "get_disciplinary_list",            # 惩戒名单
                "get_environmental_penalty",        # 环保处罚
                "get_exit_restriction",             # 限制出境
                "get_guarantee_info",               # 担保信息
                "get_hearing_notice",               # 开庭公告
                "get_high_consumption_restriction", # 限制高消费
                "get_judicial_auction",             # 司法拍卖
                "get_land_mortgage_info",           # 土地抵押
                "get_liquidation_info",             # 清算信息
                "get_pre_litigation_mediation",     # 诉前调解
                "get_public_exhortation",           # 公示催告
                "get_service_announcement",         # 劳动仲裁公告
                "get_service_notice",               # 送达公告
                "get_simple_cancellation_info",     # 简易注销
                "get_stock_pledge_info",            # 股权质押
                "get_tax_abnormal",                 # 税务非正常户
                "get_tax_arrears_notice",           # 欠税公告
                "get_tax_violation",                # 税收违法
                "get_terminated_cases",             # 终本案件
                "get_valuation_inquiry",            # 资产询价评估
            ]
        },
        "ipr": {
            "name": "知识产权",
            "url": "https://mcp.qcc.com/data/ipr/stream",
            "tools": [
                "get_trademark_info",               # 商标
                "get_patent_info",                  # 专利
                "get_software_copyright_info",      # 软件著作权
                "get_copyright_work_info",          # 作品著作权
                "get_internet_service_info",        # ICP/APP/小程序备案
                "get_standard_info",                # 参与制定的标准
            ]
        },
        "operation": {
            "name": "经营信息",
            "url": "https://mcp.qcc.com/data/operation/stream",
            "tools": [
                "get_qualifications",               # 资质证书
                "get_administrative_license",       # 行政许可
                "get_bidding_info",                 # 招投标信息
                "get_recruitment_info",             # 招聘信息
                "get_company_announcement",         # 企业公告
                "get_credit_evaluation",            # 官方信用评价
                "get_financing_records",            # 融资信息
                "get_honor_info",                   # 荣誉信息
                "get_import_export_credit",         # 进出口信用
                "get_news_sentiment",               # 新闻舆情
                "get_ranking_list_info",            # 榜单信息
                "get_spot_check_info",              # 抽查检查记录
                "get_telecom_license",              # 电信业务许可
            ]
        }
    }

    def __init__(self, auth_token: str = None):
        """
        初始化MCP客户端

        Args:
            auth_token: 授权令牌，默认从环境变量 QCC_MCP_API_KEY 读取
        """
        self.auth_token = auth_token or os.environ.get("QCC_MCP_API_KEY")

        if not self.auth_token:
            self.enabled = False
        else:
            self.enabled = True
            self.headers = {
                "accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}"
            }

    def is_enabled(self) -> bool:
        """检查MCP服务是否可用"""
        return self.enabled

    def call_tool(self, service_key: str, tool_name: str, params: Dict) -> Optional[Dict]:
        """
        调用指定服务的工具

        Args:
            service_key: 服务标识 (company/risk/ipr/operation)
            tool_name: 工具名称
            params: 调用参数

        Returns:
            工具返回结果，失败返回None或包含error字段的字典
        """
        if not self.enabled:
            return {"error": "MCP client not enabled. Set QCC_MCP_API_KEY environment variable."}

        service = self.SERVICES.get(service_key)
        if not service:
            return {"error": f"Unknown service: {service_key}"}

        payload = {
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": params,
                "_meta": {"progressToken": 1}
            },
            "jsonrpc": "2.0",
            "id": 1
        }

        try:
            response = requests.post(
                service["url"],
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            # 解析流式响应
            for line in response.text.strip().split('\n'):
                if line.startswith('data:'):
                    data = json.loads(line[5:].strip())
                    if 'result' in data and 'content' in data['result']:
                        for item in data['result']['content']:
                            if item.get('type') == 'text':
                                text_content = item['text']
                                # 修复编码问题：latin-1 编码的UTF-8字节
                                try:
                                    fixed_text = text_content.encode('latin-1').decode('utf-8')
                                    result = json.loads(fixed_text)
                                    return result
                                except (UnicodeError, json.JSONDecodeError):
                                    try:
                                        result = json.loads(text_content)
                                        return result
                                    except json.JSONDecodeError:
                                        return {"raw_text": text_content}
            return {"error": "No result in response"}

        except requests.exceptions.RequestException as e:
            return {"error": f"MCP call failed [{service_key}/{tool_name}]: {e}"}
        except Exception as e:
            return {"error": f"MCP call exception [{service_key}/{tool_name}]: {e}"}

    def verify_company(self, company_name: str) -> Optional[Dict]:
        """
        核验企业工商信息

        Args:
            company_name: 企业名称

        Returns:
            企业工商信息，包含：
            - 企业名称
            - 法定代表人
            - 统一社会信用代码
            - 登记状态
            - 注册资本
            - 成立日期
            - 注册地址
        """
        if not self.enabled:
            return None

        result = self.call_tool(
            "company",
            "get_company_registration_info",
            {"searchKey": company_name}
        )

        if result and result.get('企业名称'):
            return result
        return None

    def check_company_risk(self, company_name: str) -> Dict[str, Any]:
        """
        查询企业风险信息 - 增强版（查询18类核心风险）

        Args:
            company_name: 企业名称

        Returns:
            风险信息汇总，包含18类风险详情和统计
        """
        if not self.enabled:
            return {"error": "MCP client not enabled", "risks": {}, "summary": {"total": 0, "high": 0, "medium": 0}}

        risks = {
            # 司法执行类风险（最高优先级）
            "dishonest": None,               # 失信信息（老赖）
            "executed": None,                # 被执行人
            "high_consumption_restriction": None,  # 限制高消费
            "terminated_cases": None,        # 终本案件
            "judicial_auction": None,        # 司法拍卖

            # 经营异常类风险
            "business_exception": None,      # 经营异常
            "serious_violation": None,       # 严重违法
            "cancellation_record": None,     # 注销备案
            "simple_cancellation": None,     # 简易注销

            # 财产受限类风险
            "equity_freeze": None,           # 股权冻结
            "equity_pledge": None,           # 股权出质
            "chattel_mortgage": None,        # 动产抵押

            # 税务违法类风险
            "tax_abnormal": None,            # 税务非正常户
            "tax_arrears": None,             # 欠税公告
            "tax_violation": None,           # 税收违法

            # 环保/行政处罚类风险
            "environmental_penalty": None,   # 环保处罚
            "administrative_penalty": None,  # 行政处罚

            # 其他风险
            "bankruptcy_reorganization": None,  # 破产重整
            "liquidation": None,             # 清算信息
        }

        # 查询18类核心风险
        risk_tools = [
            ("dishonest", "risk", "get_dishonest_info"),
            ("executed", "risk", "get_judgment_debtor_info"),
            ("high_consumption_restriction", "risk", "get_high_consumption_restriction"),
            ("terminated_cases", "risk", "get_terminated_cases"),
            ("business_exception", "risk", "get_business_exception"),
            ("serious_violation", "risk", "get_serious_violation"),
            ("cancellation_record", "risk", "get_cancellation_record_info"),
            ("simple_cancellation", "risk", "get_simple_cancellation_info"),
            ("equity_freeze", "risk", "get_equity_freeze"),
            ("equity_pledge", "risk", "get_equity_pledge_info"),
            ("chattel_mortgage", "risk", "get_chattel_mortgage_info"),
            ("tax_abnormal", "risk", "get_tax_abnormal"),
            ("tax_arrears", "risk", "get_tax_arrears_notice"),
            ("tax_violation", "risk", "get_tax_violation"),
            ("environmental_penalty", "risk", "get_environmental_penalty"),
            ("administrative_penalty", "risk", "get_administrative_penalty"),
            ("bankruptcy_reorganization", "risk", "get_bankruptcy_reorganization"),
            ("liquidation", "risk", "get_liquidation_info"),
        ]

        for risk_key, service, tool in risk_tools:
            risks[risk_key] = self.call_tool(service, tool, {"searchKey": company_name})

        # 统计风险数量
        high_risk_items = ["dishonest", "executed", "high_consumption_restriction", "bankruptcy_reorganization", "liquidation"]
        medium_risk_items = ["business_exception", "serious_violation", "tax_abnormal", "tax_arrears", "tax_violation"]

        risk_count = 0
        high_risk_count = 0
        medium_risk_count = 0

        for key, value in risks.items():
            if not value or not isinstance(value, dict):
                continue
            # 检查是否有风险记录（不是"未发现"）
            has_risk = False
            for field in ['搜索结果', '摘要', '风险等级', 'status']:
                field_value = value.get(field, '')
                if field_value and isinstance(field_value, str):
                    if '未发现' not in field_value and '无' not in field_value:
                        has_risk = True
                        break

            if has_risk:
                risk_count += 1
                if key in high_risk_items:
                    high_risk_count += 1
                elif key in medium_risk_items:
                    medium_risk_count += 1

        return {
            "risks": risks,
            "summary": {
                "total": risk_count,
                "high": high_risk_count,
                "medium": medium_risk_count
            }
        }

    def batch_verify_parties(self, party_names: List[str]) -> Dict[str, Optional[Dict]]:
        """
        批量核验多个合同主体

        Args:
            party_names: 企业名称列表

        Returns:
            {企业名称: 工商信息}
        """
        results = {}
        for name in party_names:
            results[name] = self.verify_company(name)
        return results


def extract_companies_from_contract(contract_text: str) -> List[str]:
    """
    从合同文本中提取企业名称

    Args:
        contract_text: 合同文本内容

    Returns:
        企业名称列表
    """
    companies = []

    # 常见模式：甲方/乙方 + 公司名
    patterns = [
        r'甲方[：:]\s*([\u4e00-\u9fa5]+(?:公司|集团|企业|中心|店|厂|社|所|院|会))',
        r'乙方[：:]\s*([\u4e00-\u9fa5]+(?:公司|集团|企业|中心|店|厂|社|所|院|会))',
        r'买方[：:]\s*([\u4e00-\u9fa5]+(?:公司|集团|企业|中心|店|厂|社|所|院|会))',
        r'卖方[：:]\s*([\u4e00-\u9fa5]+(?:公司|集团|企业|中心|店|厂|社|所|院|会))',
        r'发包方[：:]\s*([\u4e00-\u9fa5]+(?:公司|集团|企业|中心|店|厂|社|所|院|会))',
        r'承包方[：:]\s*([\u4e00-\u9fa5]+(?:公司|集团|企业|中心|店|厂|社|所|院|会))',
        r'出租方[：:]\s*([\u4e00-\u9fa5]+(?:公司|集团|企业|中心|店|厂|社|所|院|会))',
        r'承租方[：:]\s*([\u4e00-\u9fa5]+(?:公司|集团|企业|中心|店|厂|社|所|院|会))',
        r'委托方[：:]\s*([\u4e00-\u9fa5]+(?:公司|集团|企业|中心|店|厂|社|所|院|会))',
        r'受托方[：:]\s*([\u4e00-\u9fa5]+(?:公司|集团|企业|中心|店|厂|社|所|院|会))',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, contract_text)
        companies.extend(matches)

    # 去重并保持顺序
    seen = set()
    unique_companies = []
    for c in companies:
        if c not in seen:
            seen.add(c)
            unique_companies.append(c)

    return unique_companies


def generate_verification_comments(party_info: Dict[str, Optional[Dict]]) -> List[Dict]:
    """
    根据MCP核验结果生成合同批注

    Args:
        party_info: {企业名称: 工商信息}

    Returns:
        批注列表，每个批注包含:
        - search: 搜索关键词列表
        - comment: 批注内容
        - reviewer: 审核人标识（风险等级）
    """
    comments = []

    for party_name, info in party_info.items():
        if not info:
            # 未找到企业信息
            comments.append({
                "search": [party_name],
                "comment": """【问题类型】主体信息核实
【风险原因】通过企查查MCP服务未查询到该企业的工商登记信息，该企业可能不存在、已注销或名称有误。
【修订建议】核实企业全称的准确性，要求对方提供营业执照复印件，或通过官方渠道核实企业存续状态。""",
                "reviewer": "🔴 高风险-主体核验"
            })
        else:
            # 找到企业信息，检查关键字段
            legal_person = info.get('法定代表人', '')
            credit_code = info.get('统一社会信用代码', '')
            status = info.get('登记状态', '')
            reg_capital = info.get('注册资本', '')
            est_date = info.get('成立日期', '')

            # 构建批注内容
            comment_parts = [
                "【问题类型】主体信息核实",
                "【核实结果】经企查查MCP服务核实：",
                f"  - 企业全称：{info.get('企业名称', party_name)}",
                f"  - 法定代表人：{legal_person}",
                f"  - 统一社会信用代码：{credit_code}",
                f"  - 登记状态：{status}",
            ]

            if reg_capital:
                comment_parts.append(f"  - 注册资本：{reg_capital}")
            if est_date:
                comment_parts.append(f"  - 成立日期：{est_date}")

            # 检查是否有风险
            risk_warnings = []
            if status and status not in ['存续', '在业', '开业', '存续（在营）']:
                risk_warnings.append(f"企业登记状态为'{status}'，存在经营异常风险")

            if risk_warnings:
                comment_parts.append(f"【风险原因】{'；'.join(risk_warnings)}")
                comment_parts.append("【修订建议】要求对方说明情况，或考虑终止合作。")
                reviewer = "🔴 高风险-主体核验"
            else:
                comment_parts.append("【核实结论】企业工商信息正常，登记状态为存续/在业。")
                comment_parts.append("【修订建议】建议在合同首部补充完整主体信息，核实签署人授权情况。")
                reviewer = "🟡 中风险-主体核验"

            comments.append({
                "search": [party_name],
                "comment": "\n".join(comment_parts),
                "reviewer": reviewer
            })

    return comments


def generate_risk_comments(party_name: str, risk_result: Dict[str, Any]) -> List[Dict]:
    """
    根据MCP风险查询结果生成风险批注

    Args:
        party_name: 企业名称
        risk_result: check_company_risk返回的结果

    Returns:
        风险批注列表
    """
    comments = []
    if not risk_result or "risks" not in risk_result:
        return comments

    risks = risk_result["risks"]

    # 风险名称映射
    risk_names = {
        "dishonest": "失信信息（老赖）",
        "executed": "被执行人",
        "high_consumption_restriction": "限制高消费",
        "terminated_cases": "终本案件",
        "judicial_auction": "司法拍卖",
        "business_exception": "经营异常",
        "serious_violation": "严重违法",
        "cancellation_record": "注销备案",
        "simple_cancellation": "简易注销",
        "equity_freeze": "股权冻结",
        "equity_pledge": "股权出质",
        "chattel_mortgage": "动产抵押",
        "tax_abnormal": "税务非正常户",
        "tax_arrears": "欠税公告",
        "tax_violation": "税收违法",
        "environmental_penalty": "环保处罚",
        "administrative_penalty": "行政处罚",
        "bankruptcy_reorganization": "破产重整",
        "liquidation": "清算信息"
    }

    # 高风险项（可能导致合同无法履行）
    critical_risks = ["dishonest", "executed", "high_consumption_restriction",
                      "bankruptcy_reorganization", "liquidation"]
    # 中风险项（影响企业信用）
    serious_risks = ["business_exception", "serious_violation", "tax_abnormal",
                     "tax_arrears", "tax_violation"]

    # 收集各类风险
    critical_risk_list = []
    serious_risk_list = []
    other_risk_list = []

    for risk_key, risk_data in risks.items():
        if not risk_data or not isinstance(risk_data, dict):
            continue

        # 检查是否有实际风险
        has_risk = False
        for field in ['搜索结果', '摘要', '详情', '风险描述']:
            field_value = risk_data.get(field, '')
            if field_value and isinstance(field_value, str) and '未发现' not in field_value:
                has_risk = True
                break

        if not has_risk:
            continue

        risk_name = risk_names.get(risk_key, risk_key)

        if risk_key in critical_risks:
            critical_risk_list.append(risk_name)
        elif risk_key in serious_risks:
            serious_risk_list.append(risk_name)
        else:
            other_risk_list.append(risk_name)

    # 生成🔴 高风险批注（关键风险）
    if critical_risk_list:
        comment_parts = [
            "【问题类型】主体司法执行风险",
            f"【风险企业】{party_name}",
            "【风险原因】经企查查MCP服务风险排查，发现该企业存在以下高风险事项：",
        ]
        for i, risk in enumerate(critical_risk_list, 1):
            comment_parts.append(f"  {i}. {risk}")

        comment_parts.extend([
            "【法律后果】上述风险可能导致：",
            "  - 企业履约能力严重受限",
            "  - 财产被查封、冻结或拍卖",
            "  - 法定代表人被限制高消费或出境",
            "  - 合同无法正常履行",
            "【修订建议】",
            "  1. 🔴 建议立即终止合作谈判",
            "  2. 如已签署合同，建议启动解约程序",
            "  3. 要求对方提供风险解除证明或担保措施",
            "  4. 必要时通过诉讼保全维护权益"
        ])

        comments.append({
            "search": [party_name],
            "comment": "\n".join(comment_parts),
            "reviewer": "🔴 高风险-司法执行"
        })

    # 生成🟡 中风险批注（经营/税务风险）
    if serious_risk_list:
        comment_parts = [
            "【问题类型】主体经营异常风险",
            f"【风险企业】{party_name}",
            "【风险原因】经企查查MCP服务风险排查，发现该企业存在以下经营风险：",
        ]
        for i, risk in enumerate(serious_risk_list, 1):
            comment_parts.append(f"  {i}. {risk}")

        comment_parts.extend([
            "【风险提示】上述风险可能影响企业信用和履约能力",
            "【修订建议】",
            "  1. 要求对方书面说明风险原因及整改计划",
            "  2. 在合同中增加履约保证金或银行保函条款",
            "  3. 缩短付款周期，减少预付款比例",
            "  4. 定期跟踪风险状态，必要时暂停合作"
        ])

        comments.append({
            "search": [party_name],
            "comment": "\n".join(comment_parts),
            "reviewer": "🟡 中风险-经营异常"
        })

    # 生成🟢 低风险提示（财产受限）
    if other_risk_list and not critical_risk_list and not serious_risk_list:
        comment_parts = [
            "【问题类型】主体财产受限提示",
            f"【风险企业】{party_name}",
            "【风险原因】经企查查MCP服务风险排查，发现该企业存在以下财产受限情况：",
        ]
        for i, risk in enumerate(other_risk_list, 1):
            comment_parts.append(f"  {i}. {risk}")

        comment_parts.extend([
            "【风险提示】上述情况可能影响企业资产流动性",
            "【修订建议】",
            "  1. 核实受限财产占企业总资产比例",
            "  2. 评估对合同履行的实际影响",
            "  3. 考虑要求提供额外担保"
        ])

        comments.append({
            "search": [party_name],
            "comment": "\n".join(comment_parts),
            "reviewer": "🟢 低风险-财产受限"
        })

    # 如果没有发现风险，生成一条安全提示
    if not comments:
        comments.append({
            "search": [party_name],
            "comment": f"【问题类型】主体风险排查\n【排查结果】经企查查MCP服务对【{party_name}】进行18类风险排查（包括失信、被执行、限制高消费、经营异常、税务违法、破产清算等），未发现重大风险记录。\n【建议】该主体当前风险状况良好，可正常开展合作，建议在合同中设置常规风险监控条款。",
            "reviewer": "🟢 低风险-风险排查"
        })

    return comments


def verify_and_check_risk(contract_text: str) -> Tuple[List[Dict], List[Dict]]:
    """
    完整的企业核验和风险排查流程

    Args:
        contract_text: 合同文本内容

    Returns:
        (核验批注列表, 风险批注列表)
    """
    client = QccMcpClient()

    # 如果MCP不可用，返回空列表（让上层使用Web Search降级）
    if not client.is_enabled():
        return [], []

    # 提取合同主体
    parties = extract_companies_from_contract(contract_text)
    if not parties:
        return [], []

    # 批量核验
    party_info = client.batch_verify_parties(parties)

    # 生成核验批注
    verification_comments = generate_verification_comments(party_info)

    # 对每个主体进行风险排查并生成批注
    risk_comments = []
    for party_name in parties:
        if party_info.get(party_name):  # 只对有工商信息的企业做风险排查
            risk_result = client.check_company_risk(party_name)
            risk_comments.extend(generate_risk_comments(party_name, risk_result))

    return verification_comments, risk_comments


# ==================== 兼容性函数（保持与旧版本一致） ====================

def verify_contract_parties(contract_text: str, auth_token: str = None) -> List[Dict]:
    """
    从合同文本中提取合同主体并自动核验（兼容旧版本接口）

    Args:
        contract_text: 合同文本内容
        auth_token: MCP授权令牌（可选，优先使用环境变量）

    Returns:
        批注列表
    """
    verification_comments, _ = verify_and_check_risk(contract_text)
    return verification_comments


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("企查查MCP客户端测试")
    print("=" * 60)

    client = QccMcpClient()

    if not client.is_enabled():
        print("\n⚠️  未设置 QCC_MCP_API_KEY 环境变量，客户端未启用")
        print("设置方法: export QCC_MCP_API_KEY='your_api_key'")
    else:
        print("\n✅ MCP客户端已启用")

        # 测试企业核验
        print("\n" + "-" * 60)
        print("测试企业核验")
        print("-" * 60)
        result = client.verify_company("企查查科技股份有限公司")
        if result:
            print(f"✅ 核验成功:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("❌ 核验失败")

    print("\n" + "=" * 60)
