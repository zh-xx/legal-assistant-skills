#!/bin/bash
# QCC MCP Supply Chain Plugin Installation Script
# 企查查MCP供应链插件安装脚本

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "  QCC MCP Supply Chain Plugin Installer"
echo "  企查查MCP供应链增强版安装程序"
echo "=========================================="
echo ""

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macOS"
    CLAUDE_DIR="$HOME/.claude"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="Linux"
    CLAUDE_DIR="$HOME/.claude"
else
    echo -e "${RED}Unsupported platform: $OSTYPE${NC}"
    echo "This script supports macOS and Linux only."
    exit 1
fi

echo -e "${BLUE}Detected platform: $PLATFORM${NC}"
echo ""

# Check for QCC MCP API Key
if [ -z "$QCC_MCP_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  QCC_MCP_API_KEY not found in environment${NC}"
    echo ""
    echo "To use QCC MCP enhanced features, you need an API key."
    echo "Get your key at: https://mcp.qcc.com"
    echo ""
    echo "Options:"
    echo "1. Continue without QCC MCP (baseline mode only)"
    echo "2. Enter API key now"
    echo "3. Exit and configure later"
    echo ""
    read -p "Select option (1/2/3): " choice

    case $choice in
        1)
            echo -e "${YELLOW}Continuing without QCC MCP. Chinese supplier verification will be limited.${NC}"
            ;;
        2)
            read -p "Enter your QCC MCP API Key: " api_key
            export QCC_MCP_API_KEY="$api_key"
            echo -e "${GREEN}✓ API key set for this session${NC}"
            echo ""
            echo "To make this permanent, add to your shell profile:"
            echo "  echo 'export QCC_MCP_API_KEY=\"$api_key\"' >> ~/.zshrc"
            echo "  source ~/.zshrc"
            ;;
        3)
            echo "Exiting. Please set QCC_MCP_API_KEY and run again."
            exit 0
            ;;
        *)
            echo "Invalid option. Exiting."
            exit 1
            ;;
    esac
else
    echo -e "${GREEN}✓ QCC_MCP_API_KEY found${NC}"
fi

echo ""
echo "=========================================="
echo "  Step 1: Installing Skills"
echo "=========================================="

# Define source and destination
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$CLAUDE_DIR/skills"

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Install vendor-assessment skill
echo ""
echo -e "${BLUE}Installing vendor-assessment skill...${NC}"
VENDOR_DEST="$SKILLS_DIR/vendor-assessment-qcc"

if [ -d "$VENDOR_DEST" ]; then
    echo -e "${YELLOW}  Existing vendor-assessment-qcc found, backing up...${NC}"
    mv "$VENDOR_DEST" "${VENDOR_DEST}.backup.$(date +%Y%m%d%H%M%S)"
fi

# Copy vendor-assessment skill
cp -r "$SCRIPT_DIR/skills/vendor-assessment" "$VENDOR_DEST"
echo -e "${GREEN}  ✓ vendor-assessment-qcc installed${NC}"

# Install supplier-risk skill
echo ""
echo -e "${BLUE}Installing supplier-risk skill...${NC}"
RISK_DEST="$SKILLS_DIR/supplier-risk-qcc"

if [ -d "$RISK_DEST" ]; then
    echo -e "${YELLOW}  Existing supplier-risk-qcc found, backing up...${NC}"
    mv "$RISK_DEST" "${RISK_DEST}.backup.$(date +%Y%m%d%H%M%S)"
fi

# Copy supplier-risk skill
cp -r "$SCRIPT_DIR/skills/supplier-risk" "$RISK_DEST"
echo -e "${GREEN}  ✓ supplier-risk-qcc installed${NC}"

echo ""
echo "=========================================="
echo "  Step 2: Installing Python Scripts"
echo "=========================================="

SCRIPTS_DEST="$CLAUDE_DIR/supply-chain-qcc-scripts"

if [ -d "$SCRIPTS_DEST" ]; then
    echo -e "${YELLOW}Existing scripts directory found, backing up...${NC}"
    mv "$SCRIPTS_DEST" "${SCRIPTS_DEST}.backup.$(date +%Y%m%d%H%M%S)"
fi

mkdir -p "$SCRIPTS_DEST"
cp -r "$SCRIPT_DIR/scripts/"* "$SCRIPTS_DEST/"
echo -e "${GREEN}✓ Python scripts installed to: $SCRIPTS_DEST${NC}"

echo ""
echo "=========================================="
echo "  Step 3: Verifying Installation"
echo "=========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python3 not found. Please install Python 3.9+${NC}"
else
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
fi

# Check required Python packages
echo ""
echo -e "${BLUE}Checking Python dependencies...${NC}"
python3 -c "import requests" 2>/dev/null && echo -e "${GREEN}  ✓ requests${NC}" || echo -e "${YELLOW}  ⚠️  requests not installed (pip3 install requests)${NC}"

echo ""
echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
echo -e "${GREEN}QCC MCP Supply Chain Plugin has been installed successfully!${NC}"
echo ""
echo "Installed Skills:"
echo "  • vendor-assessment-qcc  - 供应商评估（企查查MCP增强版）"
echo "  • supplier-risk-qcc      - 供应商风险监控（企查查MCP增强版）"
echo ""
echo "Python Scripts:"
echo "  Location: $SCRIPTS_DEST"
echo "  • qcc_mcp_connector.py   - QCC MCP连接器"
echo ""

if [ -n "$QCC_MCP_API_KEY" ]; then
    echo -e "${GREEN}QCC MCP Status: CONFIGURED${NC}"
    echo "Chinese supplier verification: ENABLED"
else
    echo -e "${YELLOW}QCC MCP Status: NOT CONFIGURED${NC}"
    echo "To enable Chinese supplier verification:"
    echo "  export QCC_MCP_API_KEY='your_key_here'"
fi

echo ""
echo "=========================================="
echo "  Quick Start"
echo "=========================================="
echo ""
echo "1. Start Claude Code"
echo "2. Use the enhanced skills:"
echo ""
echo "   # 评估中国供应商（自动启用QCC MCP）"
echo "   /vendor-assess 华为技术有限公司"
echo ""
echo "   # 监控供应商风险（实时QCC MCP信号）"
echo "   /supplier-risk 阿里巴巴集团"
echo ""
echo "3. For programmatic use:"
echo "   python3 $SCRIPTS_DEST/qcc_mcp_connector.py '供应商名称'"
echo ""
echo "=========================================="
echo "  Documentation"
echo "=========================================="
echo ""
echo "• README.md              - 详细文档"
echo "• SKILL.md (each skill)  - 使用指南"
echo "• https://mcp.qcc.com    - QCC MCP官网"
echo ""
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
