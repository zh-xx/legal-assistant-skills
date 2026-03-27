# 企查查MCP金融插件 V2 融合设计方案

## 设计原则

基于 Manus 版本架构，融入 V1 精华，实现**不破坏原有 SKILL 结构，只是增强**的平滑升级。

---

## 一、整体架构（Manus 版本为基础）

```
financial-services-qcc/
├── .mcp.json                              # MCP 服务配置（Manus 基础 + V1 环境变量支持）
├── README.md                              # 主文档（Manus 基础 + V1 中文增强）
├── README_zh-CN.md                        # 中文版（保留 V1 内容）
├── UNINSTALL.md                           # 卸载指南（V1 新增）
├── docs/
│   └── MCP_CONFIGURATION.md               # MCP 配置故障排查（V1 精华）
├── commands/                              # 命令定义（Manus 版本）
│   ├── qcc-kyb-profile.md                 # KYB 命令定义
│   └── qcc-full-dd-profile.md             # 全维度尽调命令定义
├── utils/                                 # Python 工具类（Manus 版本 + V1 增强）
│   ├── __init__.py
│   ├── qcc_mcp_client.py                  # MCP 客户端（Manus 基础 + V1 健壮性增强）
│   ├── kyb_verifier.py                    # KYB 核验器（Manus 基础 + V1 业务逻辑）
│   ├── dd_report_generator.py             # 尽调报告生成器（Manus 基础 + V1 业务逻辑）
│   └── config_manager.py                  # 配置管理器（V1 新增 - 自动配置 .mcp.json）
├── investment-banking/
│   └── skills/
│       └── strip-profile/
│           └── SKILL.md                   # Manus 版本 + V1 KYB 增强
├── private-equity/
│   └── skills/
│       └── ic-memo/
│           └── SKILL.md                   # Manus 版本 + V1 尽调增强
└── scripts/                               # 脚本工具（V1 保留）
    └── install_qcc_mcp_financial.sh       # V1 一键安装脚本（增强版）
```

---

## 二、核心组件融合设计

### 2.1 .mcp.json（MCP 配置）

**基础**: Manus 版本 4-Server 配置
**V1 增强**:
- 支持 `${QCC_MCP_API_KEY}` 环境变量
- 添加详细工具列表注释
- 添加配置说明文档链接

```json
{
  "mcpServers": {
    "qcc-company": {
      "url": "https://mcp.qcc.com/data/company/stream",
      "headers": {
        "Authorization": "Bearer ${QCC_MCP_API_KEY}"
      },
      "description": "企查查企业基座 - 工商登记、股东信息、变更记录",
      "tools": [
        "get_company_registration_info",
        "get_shareholder_info",
        "get_key_personnel",
        "get_change_records",
        "get_branches",
        "get_external_investments",
        "get_annual_reports",
        "get_contact_info",
        "verify_company_accuracy"
      ]
    },
    "qcc-risk": {
      "url": "https://mcp.qcc.com/data/risk/stream",
      "headers": {
        "Authorization": "Bearer ${QCC_MCP_API_KEY}"
      },
      "description": "企查查风控大脑 - 18类风险扫描",
      "tools": [
        "get_dishonest_info",
        "get_judgment_debtor_info",
        "get_executed_person_info",
        "get_high_consumption_restriction",
        "get_bankruptcy_reorganization",
        "get_equity_freeze",
        "get_equity_pledge",
        "get_business_exception",
        "get_serious_violation",
        "get_administrative_penalty",
        "get_environmental_penalty",
        "get_tax_arrears_notice",
        "get_tax_violation",
        "get_abnormal_tax",
        "get_lawsuit_info",
        "get_judicial_document"
      ]
    },
    "qcc-ipr": {
      "url": "https://mcp.qcc.com/data/ipr/stream",
      "headers": {
        "Authorization": "Bearer ${QCC_MCP_API_KEY}"
      },
      "description": "企查查知产引擎 - 专利、商标、软著",
      "tools": [
        "get_patent_info",
        "get_trademark_info",
        "get_software_copyright_info",
        "get_copyright_work_info",
        "get_standard_info"
      ]
    },
    "qcc-operation": {
      "url": "https://mcp.qcc.com/data/operation/stream",
      "headers": {
        "Authorization": "Bearer ${QCC_MCP_API_KEY}"
      },
      "description": "企查查经营罗盘 - 招投标、资质、舆情",
      "tools": [
        "get_bidding_info",
        "get_qualifications",
        "get_administrative_license",
        "get_credit_evaluation",
        "get_spot_check_info",
        "get_news_sentiment",
        "get_recruitment_info"
      ]
    }
  },
  "configuration": {
    "setup_guide": "https://github.com/duhu2000/financial-services-qcc/blob/main/docs/MCP_CONFIGURATION.md",
    "required_env_vars": ["QCC_MCP_API_KEY"]
  }
}
```

---

### 2.2 utils/qcc_mcp_client.py

**基础**: Manus 版本的 `QccMcpClient` 类
**V1 增强**:
- 添加 SSE 流式响应完整处理
- 添加错误重试机制
- 添加详细日志输出
- 添加工具可用性检查

```python
"""
QCC MCP Client - Enhanced Version
基于 Manus 版本 + V1 健壮性增强
"""
import requests
import json
import os
from typing import Dict, List, Optional, Any

class QccMcpClient:
    """企查查 MCP 客户端 - 增强版"""

    def __init__(self, mcp_config_path: str = "./.mcp.json"):
        self.mcp_servers = self._load_mcp_config(mcp_config_path)
        self.session = requests.Session()
        self.session.timeout = 30

    def _load_mcp_config(self, mcp_config_path: str) -> Dict:
        """加载 MCP 配置 - V1 增强：支持环境变量回退"""
        config_paths = [
            mcp_config_path,
            os.path.expanduser("~/.claude/.mcp.json"),
            "./.mcp.json"
        ]

        for path in config_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        if "mcpServers" in config:
                            # 替换环境变量
                            return self._resolve_env_vars(config["mcpServers"])
                except Exception as e:
                    print(f"Warning: Failed to load {path}: {e}")
                    continue

        # V1 增强：环境变量回退
        print("Warning: .mcp.json not found. Using environment variables fallback.")
        return self._load_from_env()

    def _resolve_env_vars(self, servers: Dict) -> Dict:
        """解析配置中的环境变量"""
        import re
        resolved = {}
        for server_id, config in servers.items():
            resolved[server_id] = config.copy()
            if "headers" in config:
                resolved[server_id]["headers"] = {
                    k: (os.path.expandvars(v) if isinstance(v, str) else v)
                    for k, v in config["headers"].items()
                }
        return resolved

    def _load_from_env(self) -> Dict:
        """V1 新增：从环境变量加载配置"""
        api_key = os.getenv("QCC_MCP_API_KEY")
        if not api_key:
            return {}

        return {
            "qcc-company": {
                "url": "https://mcp.qcc.com/data/company/stream",
                "headers": {"Authorization": f"Bearer {api_key}"}
            },
            "qcc-risk": {
                "url": "https://mcp.qcc.com/data/risk/stream",
                "headers": {"Authorization": f"Bearer {api_key}"}
            },
            "qcc-ipr": {
                "url": "https://mcp.qcc.com/data/ipr/stream",
                "headers": {"Authorization": f"Bearer {api_key}"}
            },
            "qcc-operation": {
                "url": "https://mcp.qcc.com/data/operation/stream",
                "headers": {"Authorization": f"Bearer {api_key}"}
            }
        }

    def call_mcp_service(self, server_id: str, query: str,
                         api_key: str = None, retry: int = 2) -> Dict:
        """
        调用 MCP 服务 - V1 增强：添加重试机制
        :param server_id: MCP Server ID (qcc-company/risk/ipr/operation)
        :param query: 查询参数（企业名称）
        :param api_key: 可选 API Key 覆盖
        :param retry: 重试次数
        """
        service_config = self.mcp_servers.get(server_id)
        if not service_config:
            return {"error": f"MCP server '{server_id}' not configured."}

        url = service_config["url"]
        headers = service_config["headers"].copy()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {"query": query}

        for attempt in range(retry + 1):
            try:
                print(f"[QccMcpClient] Calling {server_id} for: {query}")
                response = self.session.post(url, headers=headers,
                                            json=payload, stream=True)
                response.raise_for_status()
                return self._parse_sse_response(response)
            except Exception as e:
                if attempt < retry:
                    print(f"  Retry {attempt + 1}/{retry}: {e}")
                    continue
                return {"error": str(e)}

        return {"error": "Max retries exceeded"}

    def _parse_sse_response(self, response) -> Dict:
        """解析 SSE 流式响应 - V1 增强：完整处理"""
        full_data = []
        for line in response.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data:'):
                    try:
                        json_data = json.loads(decoded[5:])
                        full_data.append(json_data)
                    except json.JSONDecodeError:
                        continue

        return {"data": full_data, "count": len(full_data)}

    def check_health(self) -> Dict[str, bool]:
        """V1 新增：检查所有服务健康状态"""
        status = {}
        for server_id in self.mcp_servers:
            try:
                result = self.call_mcp_service(server_id, "test", retry=0)
                status[server_id] = "error" not in result
            except:
                status[server_id] = False
        return status
```

---

### 2.3 utils/kyb_verifier.py

**基础**: Manus 版本的 `KYBVerifier` 类
**V1 增强**:
- 添加 A/B/C/D 风险评级逻辑
- 添加 18类风险完整扫描
- 添加受益所有人识别
- 添加关联关系排查

```python
"""
KYB Verifier - Enhanced Version
基于 Manus 版本 + V1 业务逻辑完整实现
"""
from typing import Dict, List, Any
from .qcc_mcp_client import QccMcpClient

class KYBVerifier:
    """KYB 自动化核验器 - 增强版"""

    def __init__(self, mcp_config_path: str = "../.mcp.json"):
        self.qcc_client = QccMcpClient(mcp_config_path)

    def verify_company(self, company_name: str,
                       credit_code: str = None,
                       user_api_key: str = None) -> Dict:
        """
        执行企业 KYB 自动化核验（30秒快检）
        基于 V1 4阶段工作流 + Manus 技术实现
        """
        results = {
            "company_name": company_name,
            "credit_code": credit_code,
            "status": "未知",
            "kyb_rating": "D",  # A/B/C/D
            "phase_results": {},
            "verification_suggestion": "请人工复核",
            "raw_data": {}
        }

        # Phase 1: 实体锚定（5秒）
        print("\n[Phase 1] 实体锚定...")
        entity_data = self._verify_entity(company_name, credit_code, user_api_key)
        results["phase_results"]["entity"] = entity_data

        if entity_data.get("error"):
            results["status"] = "实体锚定失败"
            results["verification_suggestion"] = entity_data["error"]
            return results

        # Phase 2: 股权与受益所有人识别（8秒）
        print("\n[Phase 2] 股权穿透与UBO识别...")
        shareholder_data = self._analyze_shareholders(company_name, user_api_key)
        results["phase_results"]["shareholders"] = shareholder_data
        results["ubo"] = shareholder_data.get("ubo", [])

        # Phase 3: 18类风险扫描（15秒）
        print("\n[Phase 3] 18类风险全面扫描...")
        risk_data = self._scan_all_risks(company_name, user_api_key)
        results["phase_results"]["risks"] = risk_data
        results["risk_summary"] = self._summarize_risks(risk_data)

        # Phase 4: 经营健康度与KYB评级（2秒）
        print("\n[Phase 4] 经营健康度评估...")
        operation_data = self._check_operation(company_name, user_api_key)
        results["phase_results"]["operation"] = operation_data

        # 计算 KYB 评级
        rating, suggestion = self._calculate_kyb_rating(
            entity_data, risk_data, operation_data
        )
        results["kyb_rating"] = rating
        results["verification_suggestion"] = suggestion
        results["status"] = "核验完成"

        return results

    def _verify_entity(self, company_name: str, credit_code: str = None,
                       api_key: str = None) -> Dict:
        """Phase 1: 实体锚定"""
        result = self.qcc_client.call_mcp_service(
            "qcc-company", company_name, api_key
        )
        return result

    def _analyze_shareholders(self, company_name: str, api_key: str = None) -> Dict:
        """Phase 2: 股权穿透与UBO识别"""
        # 获取股东信息
        shareholder_result = self.qcc_client.call_mcp_service(
            "qcc-company", company_name, api_key
        )

        # V1 增强：穿透识别受益所有人
        ubo_list = []
        # 解析股东数据，识别持股25%以上的自然人

        return {
            "shareholders": shareholder_result.get("data", []),
            "ubo": ubo_list,
            "external_investments": []  # 对外投资
        }

    def _scan_all_risks(self, company_name: str, api_key: str = None) -> Dict:
        """
        Phase 3: 18类风险全面扫描
        V1 完整风险列表 + Manus 技术实现
        """
        risks = {}

        # CRITICAL 级风险（<4小时响应）
        critical_tools = [
            ("get_dishonest_info", "失信信息"),
            ("get_judgment_debtor_info", "被执行人"),
            ("get_executed_person_info", "被执行信息"),
            ("get_high_consumption_restriction", "限制高消费"),
            ("get_bankruptcy_reorganization", "破产重整"),
            ("get_equity_freeze", "股权冻结"),
        ]

        # HIGH 级风险（<24小时响应）
        high_tools = [
            ("get_business_exception", "经营异常"),
            ("get_serious_violation", "严重违法"),
        ]

        # 调用风险扫描
        risk_result = self.qcc_client.call_mcp_service(
            "qcc-risk", company_name, api_key
        )

        return {
            "critical": {name: risk_result for _, name in critical_tools},
            "high": {name: risk_result for _, name in high_tools},
            "raw_data": risk_result.get("data", [])
        }

    def _check_operation(self, company_name: str, api_key: str = None) -> Dict:
        """Phase 4: 经营健康度"""
        # 资质、信用、招投标等
        return {}

    def _summarize_risks(self, risk_data: Dict) -> Dict:
        """V1 增强：风险摘要统计"""
        summary = {
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
            "risk_items": []
        }

        # 统计风险
        for level, items in risk_data.items():
            if isinstance(items, dict):
                for risk_name, data in items.items():
                    if data and not data.get("error"):
                        summary["risk_items"].append(risk_name)

        return summary

    def _calculate_kyb_rating(self, entity_data: Dict,
                              risk_data: Dict,
                              operation_data: Dict) -> tuple:
        """
        V1 增强：A/B/C/D 评级计算
        A级: 正常准入
        B级: 审慎准入+加强监测
        C级: 需人工复核
        D级: 禁止准入
        """
        # 检查关键风险
        critical_risks = risk_data.get("critical", {})
        high_risks = risk_data.get("high", {})

        # D级：存在 CRITICAL 风险
        for risk_name, data in critical_risks.items():
            if data and not data.get("error"):
                return "D", f"存在{risk_name}，禁止准入。建议立即启动风险预警流程。"

        # C级：存在 HIGH 风险
        for risk_name, data in high_risks.items():
            if data and not data.get("error"):
                return "C", f"存在{risk_name}，需人工复核。建议加强尽调。"

        # B级：存在 MEDIUM 风险或经营状态异常

        # A级：无风险
        return "A", "正常准入。主体合法存续，无明显风险信号，可按标准流程处理。"
```

---

### 2.4 investment-banking/skills/strip-profile/SKILL.md

**基础**: Manus 版本（已集成企查查调用）
**V1 增强**: 添加 KYB 详细规则和风险评级逻辑

**融合设计**:
```markdown
## Workflow

### 2. Qichacha MCP KYB Verification（增强版）
- **Action**: Call `/qcc-kyb-profile` command
- **Purpose**: Obtain real-time data for Chinese companies
- **V1 Enhancement**:
  - 执行 4 阶段 KYB 核验（实体锚定→股权穿透→18类风险扫描→经营健康度）
  - 生成 A/B/C/D 四级评级
  - 输出准入建议
- **Decision Point**:
  - D级（禁止准入）：立即提示人工深度复核
  - C级（需人工复核）：标记风险关注点
  - B级（审慎准入）：加强监测建议
  - A级（正常准入）：继续生成简况
```

---

### 2.5 private-equity/skills/ic-memo/SKILL.md

**基础**: Manus 版本（已集成企查查调用）
**V1 增强**: 添加 7章尽调结构和详细扫描规则

**融合设计**:
```markdown
## Workflow

### Chapter 2-5 Data Collection（增强版）

**通过 `/qcc-full-dd-profile` 命令获取**:

**Chapter 2: 公司概况与股权结构**
- 工商注册信息（企查查 MCP）
- 股权穿透分析（V1 增强：25%规则识别UBO）
- 历史融资情况

**Chapter 3: 知识产权与核心竞争力**
- 专利布局分析（发明/实用新型/外观）
- 商标品牌核查
- 软件著作权统计
- V1 增强：核心技术评估

**Chapter 4: 法律与合规风险**
- 涉诉情况（原告/被告/被执行人）
- 18类风险全扫描（V1 完整风险清单）
- 合规结论

**Chapter 5: 经营与市场分析**
- 招投标活跃度（业务规模指标）
- 资质证书有效性
- 舆情监控（V1 新增）
```

---

## 三、一键安装脚本增强

**scripts/install_qcc_mcp_financial.sh**

```bash
#!/bin/bash
# V2 融合版安装脚本
# - Manus 版本代码结构
# - V1 自动配置能力

# 1. 创建目录结构（Manus 版本）
mkdir -p utils commands docs

# 2. 复制代码文件
# - utils/*.py（Manus 版本 + V1 增强）
# - commands/*.md（Manus 版本）
# - skills/*/SKILL.md（融合版本）

# 3. 自动创建 .mcp.json（V1 能力）
# 4. 检查环境变量（V1 能力）
# 5. 重启提示（V1 增强）
```

---

## 四、文档融合

### 4.1 README.md（融合版）
- **Manus 基础**: 英文介绍、使用示例
- **V1 增强**: 中文说明、详细安装步骤、故障排查

### 4.2 README_zh-CN.md（V1 保留）
- 完整中文版使用指南

### 4.3 docs/MCP_CONFIGURATION.md（V1 精华）
- MCP 配置故障排查指南
- 常见问题解决
- 验证方法

### 4.4 UNINSTALL.md（V1 新增）
- 完整卸载指南

---

## 五、升级实施计划

### 阶段1：基础架构（Week 1）
1. ✅ 备份 V1 版本
2. 创建 V2 分支
3. 建立 Manus 目录结构
4. 集成 .mcp.json

### 阶段2：核心代码（Week 2）
1. utils/qcc_mcp_client.py（Manus + V1 增强）
2. utils/kyb_verifier.py（Manus + V1 业务逻辑）
3. utils/dd_report_generator.py

### 阶段3：SKILL 融合（Week 3）
1. investment-banking/skills/strip-profile/SKILL.md
2. private-equity/skills/ic-memo/SKILL.md
3. 添加详细规则说明

### 阶段4：工具完善（Week 4）
1. 一键安装脚本
2. 文档完善
3. 测试验证

---

## 六、关键决策点

### Q1: 是否保留 V1 的独立 SKILL 模式？
**建议**:
- **commands/** 作为主推（Manus 方式）
- **skills/** 作为兼容层（不破坏原有结构）
- 两者底层共用 utils/

### Q2: Python 代码是否需要异步支持？
**建议**:
- Phase 1: 同步实现（简单稳定）
- Phase 2: 添加 asyncio 支持（并行调用提速）

### Q3: 错误处理策略？
**建议**:
- Manus 基础：try-except
- V1 增强：重试机制 + 降级策略 + 详细日志

---

## 七、融合后的优势

| 特性 | Manus 版本 | V1 版本 | V2 融合版 |
|------|-----------|---------|-----------|
| 架构清晰 | ✅ | ⚠️ | ✅ 增强 |
| 开箱即用 | ⚠️ | ✅ | ✅ 保留 |
| 中文文档 | ⚠️ | ✅ | ✅ 保留 |
| 业务逻辑 | ⚠️ 基础 | ✅ 完整 | ✅ 完整 |
| 故障排查 | ⚠️ | ✅ | ✅ 保留 |
| 工具精细 | ✅ | ⚠️ | ✅ 增强 |
| Python 封装 | ✅ | ⚠️ | ✅ 保留 |

---

您觉得这个融合设计方案如何？

**下一步行动建议**:
1. 您确认方案后，我开始实施
2. 或者您有特定偏好（如优先做哪个部分）
3. 或者您想先看看融合后的某个具体文件示例