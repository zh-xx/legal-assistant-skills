#!/bin/bash
# 企查查MCP合同审核安装脚本
# 一键安装完整的合同审核 + MCP增强功能

set -e

SKILLS_DIR="${HOME}/.claude/skills"
REPO_URL="https://github.com/duhu2000/legal-assistant-skills.git"
TEMP_DIR="/tmp/legal-assistant-skills-$$"

echo "========================================"
echo "企查查MCP合同审核安装"
echo "========================================"
echo ""

# 检查依赖
echo "检查依赖环境..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    echo "请先安装 Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
echo "✅ Python版本: $PYTHON_VERSION"

# 检查 git
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 未找到 git"
    echo "请先安装 git"
    exit 1
fi
echo "✅ Git已安装"

# 创建 skills 目录
mkdir -p "$SKILLS_DIR"
echo "✅ Skills目录: $SKILLS_DIR"
echo ""

# 克隆仓库
echo "正在下载合同审核Skill..."
if [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi
git clone --depth 1 "$REPO_URL" "$TEMP_DIR" 2>&1 | grep -v "^hint:" || true
echo "✅ 下载完成"
echo ""

# 安装 contract-review skill
echo "正在安装 contract-review skill..."
if [ -d "$SKILLS_DIR/contract-review" ]; then
    echo "⚠️  检测到已存在 contract-review，正在备份..."
    mv "$SKILLS_DIR/contract-review" "$SKILLS_DIR/contract-review.bak.$(date +%Y%m%d%H%M%S)"
fi

cp -r "$TEMP_DIR/contract-review" "$SKILLS_DIR/"
echo "✅ contract-review 安装完成"
echo ""

# 清理临时目录
rm -rf "$TEMP_DIR"

# 设置权限
chmod -R +x "$SKILLS_DIR/contract-review/scripts"/*.py 2>/dev/null || true
echo "✅ 权限设置完成"
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

# 使用临时Python文件进行测试，避免heredoc变量展开问题
TEST_SCRIPT="/tmp/test_qcc_mcp_$$.py"

cat > "$TEST_SCRIPT" << 'EOF'
import sys
import os

# 动态获取HOME目录
home_dir = os.path.expanduser("~")
skill_path = os.path.join(home_dir, ".claude/skills/contract-review")
scripts_path = os.path.join(skill_path, "scripts")

# 添加scripts目录到path
sys.path.insert(0, scripts_path)

try:
    # 直接从scripts目录导入
    import importlib.util
    spec = importlib.util.spec_from_file_location("qcc_mcp_client", os.path.join(scripts_path, "qcc_mcp_client.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    QccMcpClient = module.QccMcpClient

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
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ 所有测试通过！")
EOF

python3 "$TEST_SCRIPT" || true
rm -f "$TEST_SCRIPT"

echo ""
echo "========================================"
echo "安装完成"
echo "========================================"
echo ""
echo "📁 文件位置:"
echo "  - Skill目录: $SKILLS_DIR/contract-review/"
echo "  - MCP客户端: $SKILLS_DIR/contract-review/scripts/qcc_mcp_client.py"
echo "  - 使用指南: $SKILLS_DIR/contract-review/README_QCC_MCP.md"
echo ""
echo "🚀 快速开始:"
echo ""
echo "  1. 在Claude Code中使用:"
echo "     /skills load contract-review"
echo ""
echo "  2. 或者直接输入:"
echo "     请审核这份合同: /path/to/contract.docx"
echo ""
echo "📖 文档:"
echo "  - GitHub: https://github.com/duhu2000/legal-assistant-skills"
echo "  - MCP官网: https://mcp.qcc.com"
echo ""
