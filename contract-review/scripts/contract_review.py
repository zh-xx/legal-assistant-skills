#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合同审核入口脚本
Contract Review Entry Point

Usage:
    python contract_review.py <contract_path> [options]

Example:
    python contract_review.py "合同.docx"
    python contract_review.py "合同.docx" --enable-mcp
"""

import sys
import os
from pathlib import Path

# 添加父目录到路径
script_dir = Path(__file__).parent
skill_dir = script_dir.parent
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

from scripts.workflow import ContractReviewWorkflow, review_contract
from scripts.qcc_mcp_client import QccMcpClient, generate_verification_comments


def main():
    if len(sys.argv) < 2:
        print("Usage: python contract_review.py <contract_path> [--enable-mcp]")
        sys.exit(1)

    contract_path = sys.argv[1]
    enable_mcp = "--enable-mcp" in sys.argv or os.environ.get("QCC_MCP_API_KEY")

    print(f"合同审核: {contract_path}")
    print(f"MCP启用: {bool(enable_mcp)}")
    print()

    # 创建workflow
    workflow = ContractReviewWorkflow(
        contract_path=contract_path,
        reviewer_name="合同审核助手",
        enable_mcp_verification=bool(enable_mcp)
    )

    # 执行MCP核验（如果启用）
    comments = []
    if workflow.enable_mcp_verification and workflow.mcp_client:
        print("=" * 60)
        print("执行企业核验...")
        print("=" * 60)
        try:
            mcp_comments = workflow.step_mcp_verify_parties()
            if mcp_comments:
                comments.extend(mcp_comments)
                print(f"✅ 生成 {len(mcp_comments)} 条核验批注")
            else:
                print("⚠️  未生成核验批注")
        except Exception as e:
            print(f"❌ 核验失败: {e}")

    print()
    print("=" * 60)
    print("执行合同审核流程...")
    print("=" * 60)

    # 执行完整审核流程
    # 注意：summary_text, opinion_text, flowchart_mermaid 应由 AI 生成后传入
    # 这里作为入口脚本，先执行基础流程
    success = workflow.run_full_workflow(
        comments=comments,
        output_docx_filename=None,  # 自动生成
        report_filename="审核报告.txt",
        summary_text=None,  # AI 应生成
        opinion_text=None,  # AI 应生成
        flowchart_mermaid=None,  # AI 应生成
        parallel_outputs=True
    )

    if success:
        print()
        print("=" * 60)
        print("审核完成！")
        print("=" * 60)
        print(f"输出目录: {workflow.output_dir}")
        return 0
    else:
        print()
        print("=" * 60)
        print("审核失败！")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
