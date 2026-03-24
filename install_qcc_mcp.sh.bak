#!/bin/bash
# 企查查MCP集成安装脚本
# 用于在现有 legal-assistant-skills 基础上添加 QCC MCP 支持

set -e

SKILLS_DIR="${HOME}/.claude/skills"
QCC_MCP_URL="https://raw.githubusercontent.com/YOUR_USERNAME/legal-assistant-skills/main/contract-review"

echo "========================================"
echo "企查查MCP集成安装"
echo "========================================"
echo ""

# 检查是否已安装 contract-review skill
if [ ! -d "$SKILLS_DIR/contract-review" ]; then
    echo "❌ 错误: 未找到 contract-review skill"
    echo "请先安装 legal-assistant-skills:"
    echo "  bash <(curl -sL https://raw.githubusercontent.com/zh-xx/legal-assistant-skills/main/install_legal_skills.sh)"
    exit 1
fi

echo "✅ 找到 contract-review skill"
echo ""

# 下载 QCC MCP 客户端
echo "正在下载企查查MCP客户端..."
curl -sL "$QCC_MCP_URL/scripts/qcc_mcp_client.py" \
    -o "$SKILLS_DIR/contract-review/scripts/qcc_mcp_client.py" \
    || echo "⚠️  下载失败，请手动下载"

# 设置执行权限
chmod +x "$SKILLS_DIR/contract-review/scripts/qcc_mcp_client.py" 2>/dev/null || true

echo "✅ QCC MCP客户端安装完成"
echo ""

# 检查环境变量
echo "========================================"
echo "环境配置检查"
echo "========================================"
echo ""

if [ -z "$QCC_MCP_API_KEY" ]; then
    echo "⚠️  未设置 QCC_MCP_API_KEY 环境变量"
    echo ""
    echo "请按以下步骤配置："
    echo ""
    echo "1. 访问 https://mcp.qcc.com 申请API Key"
    echo ""
    echo "2. 临时设置（当前终端）："
    echo "   export QCC_MCP_API_KEY='your_api_key_here'"
    echo ""
    echo "3. 永久设置（推荐）："
    echo ""

    # 检测shell类型
    if [ -n "$ZSH_VERSION" ] || [ "${SHELL##*/}" = "zsh" ]; then
        echo "   # Zsh用户，添加到 ~/.zshrc:"
        echo "   echo 'export QCC_MCP_API_KEY=\"your_api_key_here\"' >> ~/.zshrc"
        echo "   source ~/.zshrc"
    elif [ -n "$BASH_VERSION" ] || [ "${SHELL##*/}" = "bash" ]; then
        echo "   # Bash用户，添加到 ~/.bashrc:"
        echo "   echo 'export QCC_MCP_API_KEY=\"your_api_key_here\"' >> ~/.bashrc"
        echo "   source ~/.bashrc"
    else
        echo "   # 根据你的shell类型，添加到对应的配置文件"
        echo "   export QCC_MCP_API_KEY='your_api_key_here'"
    fi
    echo ""
else
    echo "✅ QCC_MCP_API_KEY 已设置"
    echo "   值: ${QCC_MCP_API_KEY:0:10}...${QCC_MCP_API_KEY: -5}"
    echo ""
fi

# 测试安装
echo "========================================"
echo "测试安装"
echo "========================================"
echo ""

python3 << 'PYTHON_TEST'
import sys
sys.path.insert(0, "${HOME}/.claude/skills/contract-review")

try:
    from scripts.qcc_mcp_client import QccMcpClient
    client = QccMcpClient()

    if client.is_enabled():
        print("✅ MCP客户端初始化成功")
        print("✅ MCP服务已启用")

        # 简单测试
        print("\n正在测试企业核验...")
        result = client.verify_company("企查查科技股份有限公司")
        if result and result.get('企业名称'):
            print(f"✅ 企业核验测试成功")
            print(f"   企业: {result.get('企业名称')}")
            print(f"   法人: {result.get('法定代表人')}")
        else:
            print("⚠️  企业核验测试未返回结果")
    else:
        print("⚠️  MCP客户端已初始化但未启用")
        print("   原因: 未设置 QCC_MCP_API_KEY 环境变量")
        print("   不影响使用，将自动回退到Web Search")

except Exception as e:
    print(f"❌ 测试失败: {e}")
    sys.exit(1)

print("\n✅ 所有测试通过！")
PYTHON_TEST

echo ""
echo "========================================"
echo "安装完成"
echo "========================================"
echo ""
echo "文件位置:"
echo "  - MCP客户端: $SKILLS_DIR/contract-review/scripts/qcc_mcp_client.py"
echo "  - 使用指南: $SKILLS_DIR/contract-review/README_QCC_MCP.md"
echo ""
echo "使用说明:"
echo "  1. 确保已设置 QCC_MCP_API_KEY 环境变量"
echo "  2. 正常使用 contract-review skill"
echo "  3. 系统将自动使用MCP进行企业核验（如果启用）"
echo ""
echo "如需帮助，请查看:"
echo "  cat $SKILLS_DIR/contract-review/README_QCC_MCP.md"
echo ""
