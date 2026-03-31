# 企查查MCP集成指南

本指南介绍如何在 contract-review skill 中启用企查查MCP（Model Context Protocol）服务，实现自动化的企业信息核验和风险排查。

## 功能特性

启用企查查MCP后，合同审核将自动进行：

1. **企业信息核验**
   - 企业全称核实
   - 法定代表人验证
   - 统一社会信用代码核对
   - 登记状态确认（存续/在业/注销等）
   - 注册资本、成立日期等基本信息

2. **风险信息排查（18类核心风险）**

   **司法执行类（最高风险）**
   - 失信信息（老赖）
   - 被执行人
   - 限制高消费
   - 终本案件
   - 司法拍卖

   **经营异常类**
   - 经营异常
   - 严重违法
   - 注销备案
   - 简易注销

   **财产受限类**
   - 股权冻结
   - 股权出质
   - 动产抵押

   **税务违法类**
   - 税务非正常户
   - 欠税公告
   - 税收违法

   **环保/行政处罚类**
   - 环保处罚
   - 行政处罚

   **破产清算类**
   - 破产重整
   - 清算信息

3. **智能批注生成**
   - 自动识别合同主体
   - 根据核验结果生成结构化批注
   - 风险等级自动标记（🔴高风险/🟡中风险/🟢低风险）

## 快速开始

### 步骤1：申请企查查MCP API Key

1. 访问企查查MCP开放平台：https://agent.qcc.com
2. 注册账号并申请API访问权限
3. 获取API Key（格式类似：`M81hQFzTBO4lSS9YRk9BSD...`）

### 步骤2：设置环境变量

**临时设置（当前终端会话）**
```bash
export QCC_MCP_API_KEY="your_api_key_here"
```

**永久设置（推荐）**

**macOS/Linux:**
```bash
# 根据你的shell类型选择
# Bash用户
echo 'export QCC_MCP_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc

# Zsh用户
echo 'export QCC_MCP_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("QCC_MCP_API_KEY", "your_api_key_here", "User")
```

### 步骤3：验证配置

```bash
# 进入skill目录
cd ~/.claude/skills/contract-review

# 运行测试
python scripts/qcc_mcp_client.py
```

如果配置正确，将看到企业核验测试输出。

## 使用方式

### 方式1：直接使用 Python API

```python
from scripts.qcc_mcp_client import QccMcpClient, verify_and_check_risk

# 初始化客户端（自动读取 QCC_MCP_API_KEY 环境变量）
client = QccMcpClient()

# 检查MCP是否启用
if client.is_enabled():
    # 核验单个企业
    info = client.verify_company("企查查科技股份有限公司")
    print(f"企业名称: {info.get('企业名称')}")
    print(f"法定代表人: {info.get('法定代表人')}")
    print(f"登记状态: {info.get('登记状态')}")

    # 查询企业风险
    risk_result = client.check_company_risk("企查查科技股份有限公司")
    print(f"风险统计: {risk_result['summary']}")
```

### 方式2：结合合同文本自动核验

```python
from scripts.qcc_mcp_client import verify_and_check_risk

# 读取合同文本
with open('contract.docx', 'r', encoding='utf-8') as f:
    contract_text = f.read()

# 自动提取合同主体并核验
verification_comments, risk_comments = verify_and_check_risk(contract_text)

# 核验批注
for comment in verification_comments:
    print(f"[{comment['reviewer']}] {comment['comment']}")

# 风险批注
for comment in risk_comments:
    print(f"[{comment['reviewer']}] {comment['comment']}")
```

### 方式3：在完整审核流程中使用

在 contract-review skill 的标准审核流程中，只要设置了 `QCC_MCP_API_KEY` 环境变量，系统会自动：

1. 从合同文本中提取甲方、乙方等合同主体
2. 调用企查查MCP进行企业信息核验
3. 自动进行18类风险排查
4. 将核验结果和风险批注添加到审核版合同中

无需修改任何代码，只需设置环境变量即可启用。

## 降级策略

本实现采用**优雅降级**设计：

| 场景 | 行为 |
|------|------|
| 已设置 `QCC_MCP_API_KEY` | 使用企查查MCP进行企业核验和风险排查 |
| 未设置 `QCC_MCP_API_KEY` | 自动回退到 Web Search 进行企业核验（原skill行为） |
| MCP调用失败 | 返回错误信息，不影响其他审核流程 |
| 未找到企业信息 | 生成高风险批注，提示核实企业名称 |

## API 参考

### QccMcpClient 类

```python
class QccMcpClient:
    def __init__(self, auth_token: str = None):
        """
        初始化MCP客户端

        Args:
            auth_token: 授权令牌，默认从环境变量 QCC_MCP_API_KEY 读取
        """

    def is_enabled(self) -> bool:
        """检查MCP服务是否可用"""

    def verify_company(self, company_name: str) -> Optional[Dict]:
        """
        核验企业工商信息

        Returns:
            企业工商信息字典，包含：
            - 企业名称
            - 法定代表人
            - 统一社会信用代码
            - 登记状态
            - 注册资本
            - 成立日期
            - 注册地址
        """

    def check_company_risk(self, company_name: str) -> Dict[str, Any]:
        """
        查询企业风险信息（18类核心风险）

        Returns:
            {
                "risks": {风险类型: 风险详情},
                "summary": {
                    "total": 总风险数,
                    "high": 高风险数,
                    "medium": 中风险数
                }
            }
        """

    def batch_verify_parties(self, party_names: List[str]) -> Dict[str, Optional[Dict]]:
        """批量核验多个合同主体"""
```

### 便捷函数

```python
def verify_and_check_risk(contract_text: str) -> Tuple[List[Dict], List[Dict]]:
    """
    完整的企业核验和风险排查流程

    Returns:
        (核验批注列表, 风险批注列表)
    """

def extract_companies_from_contract(contract_text: str) -> List[str]:
    """
    从合同文本中提取企业名称

    支持识别：甲方、乙方、买方、卖方、发包方、承包方、出租方、承租方、委托方、受托方
    """

def generate_verification_comments(party_info: Dict[str, Optional[Dict]]) -> List[Dict]:
    """
    根据核验结果生成合同批注

    Returns:
        批注列表，每个批注包含 search, comment, reviewer 字段
    """

def generate_risk_comments(party_name: str, risk_result: Dict[str, Any]) -> List[Dict]:
    """根据风险查询结果生成风险批注"""
```

## 批注格式示例

### 核验成功（正常企业）

```
【问题类型】主体信息核实
【核实结果】经企查查MCP服务核实：
  - 企业全称：XXX科技有限公司
  - 法定代表人：张三
  - 统一社会信用代码：91350100M0001XXXXX
  - 登记状态：存续
  - 注册资本：1000万元人民币
  - 成立日期：2020-01-15
【核实结论】企业工商信息正常，登记状态为存续/在业。
【修订建议】建议在合同首部补充完整主体信息，核实签署人授权情况。
```

**审核人**: 🟡 中风险-主体核验

### 核验失败（企业不存在）

```
【问题类型】主体信息核实
【风险原因】通过企查查MCP服务未查询到该企业的工商登记信息，该企业可能不存在、已注销或名称有误。
【修订建议】核实企业全称的准确性，要求对方提供营业执照复印件，或通过官方渠道核实企业存续状态。
```

**审核人**: 🔴 高风险-主体核验

### 风险排查（发现失信记录）

```
【问题类型】主体司法执行风险
【风险企业】XXX建设有限公司
【风险原因】经企查查MCP服务风险排查，发现该企业存在以下高风险事项：
  1. 失信信息（老赖）
  2. 被执行人
  3. 限制高消费
【法律后果】上述风险可能导致：
  - 企业履约能力严重受限
  - 财产被查封、冻结或拍卖
  - 法定代表人被限制高消费或出境
  - 合同无法正常履行
【修订建议】
  1. 🔴 建议立即终止合作谈判
  2. 如已签署合同，建议启动解约程序
  3. 要求对方提供风险解除证明或担保措施
  4. 必要时通过诉讼保全维护权益
```

**审核人**: 🔴 高风险-司法执行

## 故障排除

### 问题1：MCP未启用

**现象**: `client.is_enabled()` 返回 `False`

**解决**:
```bash
# 检查环境变量是否设置
echo $QCC_MCP_API_KEY

# 如果为空，重新设置
export QCC_MCP_API_KEY="your_api_key_here"
```

### 问题2：API调用失败

**现象**: 返回 `{"error": "..."}`

**可能原因**:
- API Key 无效或过期
- 网络连接问题
- 企业服务暂时不可用

**解决**:
1. 检查API Key有效性
2. 测试网络连通性：`curl https://agent.qcc.com`
3. 查看错误信息中的具体原因

### 问题3：未从合同中提取到企业名称

**现象**: `extract_companies_from_contract` 返回空列表

**解决**:
- 确保合同使用标准称谓（甲方、乙方、买方、卖方等）
- 企业名称后应有"公司"、"集团"等后缀
- 可手动传入企业名称列表进行核验

## 隐私与安全

- API Key 仅存储在环境变量中，不会写入代码或日志
- 企业查询记录不会本地保存
- 建议在可信环境中使用，避免API Key泄露

## 技术支持

- 企查查MCP官方文档：https://agent.qcc.com/docs
- API问题请联系企查查技术支持
- Skill使用问题请提交GitHub Issue

## 许可证

与主项目一致：Apache License 2.0
