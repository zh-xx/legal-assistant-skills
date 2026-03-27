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

# 创建 MCP 配置文件
echo "正在配置 MCP 服务器..."
CLAUDE_DIR="${HOME}/.claude"
MCP_CONFIG="$CLAUDE_DIR/.mcp.json"

if [ -f "$MCP_CONFIG" ]; then
    echo "⚠️  检测到已存在 MCP 配置，正在备份..."
    cp "$MCP_CONFIG" "$MCP_CONFIG.bak.$(date +%Y%m%d%H%M%S)"
fi

cat > "$MCP_CONFIG" << 'MCPJSONEOF'
{
  "mcpServers": {
    "qcc-company": {
      "url": "https://mcp.qcc.com/data/company/stream",
      "headers": {
        "Authorization": "Bearer ${QCC_MCP_API_KEY}"
      }
    },
    "qcc-risk": {
      "url": "https://mcp.qcc.com/data/risk/stream",
      "headers": {
        "Authorization": "Bearer ${QCC_MCP_API_KEY}"
      }
    },
    "qcc-ipr": {
      "url": "https://mcp.qcc.com/data/ipr/stream",
      "headers": {
        "Authorization": "Bearer ${QCC_MCP_API_KEY}"
      }
    },
    "qcc-operation": {
      "url": "https://mcp.qcc.com/data/operation/stream",
      "headers": {
        "Authorization": "Bearer ${QCC_MCP_API_KEY}"
      }
    }
  }
}
MCPJSONEOF

echo "✅ MCP 配置文件已创建: $MCP_CONFIG"
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

# 安装Python依赖
echo "正在安装Python依赖..."
if python3 -c "import requests" 2>/dev/null; then
    echo "✅ requests 模块已安装"
else
    echo "正在安装 requests 模块..."
    pip3 install --user requests 2>/dev/null || \
    pip install --user requests 2>/dev/null || \
    python3 -m pip install --user requests 2>/dev/null || \
    echo "⚠️  自动安装失败，请手动运行: pip3 install --user requests"
fi
echo "✅ 依赖检查完成"
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

# 简单测试：检查关键文件是否存在
SKILL_INSTALLED="$SKILLS_DIR/contract-review"
MCP_CLIENT="$SKILL_INSTALLED/scripts/qcc_mcp_client.py"

if [ -f "$MCP_CLIENT" ]; then
    echo "✅ MCP客户端文件存在"

    # 检查Python语法
    if python3 -m py_compile "$MCP_CLIENT" 2>/dev/null; then
        echo "✅ MCP客户端语法正确"
    else
        echo "⚠️  MCP客户端语法检查失败"
    fi

    # 尝试导入测试（直接在scripts目录下运行）
    cd "$SKILL_INSTALLED/scripts" && python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from qcc_mcp_client import QccMcpClient
    client = QccMcpClient()
    if client.is_enabled():
        print('✅ MCP客户端可正常导入和初始化')
        print('✅ MCP服务配置已启用')
    else:
        print('✅ MCP客户端可正常导入')
        print('⚠️  MCP服务未启用（未设置QCC_MCP_API_KEY）')
        print('   提示：设置环境变量后可启用企业核验功能')
except Exception as e:
    print(f'❌ 导入测试失败: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
" 2>&1 || echo "⚠️  MCP导入测试失败，但不影响基础功能"
else
    echo "❌ MCP客户端文件不存在"
fi

echo ""
echo "========================================"
echo "⚠️  重要：安装后步骤"
echo "========================================"
echo ""
echo -e "\033[1;33m必须重启 Claude Code 以加载 MCP 配置！\033[0m"
echo ""
echo "步骤 1: 完全退出 Claude Code"
echo "步骤 2: 确保已设置 QCC_MCP_API_KEY:"
echo "       export QCC_MCP_API_KEY='your_api_key_here'"
echo "步骤 3: 重启 Claude Code"
echo "步骤 4: 验证 MCP 服务器已加载:"
echo "       你应该能看到 'qcc-company', 'qcc-risk' 等工具"
echo ""
echo "========================================"
echo "安装完成"
echo "========================================"
echo ""
echo "📁 文件位置:"
echo "  - Skill目录: $SKILLS_DIR/contract-review/"
echo "  - MCP配置: $CLAUDE_DIR/.mcp.json"
echo "  - MCP客户端: $SKILLS_DIR/contract-review/scripts/qcc_mcp_client.py"
echo "  - 使用指南: $SKILLS_DIR/contract-review/README_QCC_MCP.md"
echo ""
echo "🚀 快速开始（重启 Claude 后）:"
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
