# 法律 AI 技能集

适用于 Claude Code、Codex 等代码代理平台的法律工作技能仓库。每个技能以独立目录组织，核心说明写在 `SKILL.md` 中，可按需附带 `references/`、`scripts/`、`assets/` 等资源。

> **免责声明**：本仓库提供的是工作流与辅助工具，不构成正式法律意见或律师执业服务。

## 当前技能

| 技能 | 主要用途 | 典型输出 |
|------|----------|----------|
| `contract-review` | 合同审查，在不改原文的前提下添加批注式问题标注 | 审核版合同、合同摘要、综合审核意见、业务流程图 |
| `contract-gen` | 根据交易背景、主体信息和立场生成完整合同 | Markdown 合同，可选导出 DOCX |
| `law-to-markdown` | 将法条/规范文件 `.txt` / `.docx` / `.pdf` 转为 Markdown | 最终 Markdown、审核报告、阶段校验产物 |
| `ad-compliance-review` | 审核广告文案或素材的广告法合规性 | Markdown 审核报告，可选导出 DOCX |
| `food-label-review` | 审核预包装食品标签是否符合 GB 7718 / GB 28050 | Markdown 审核报告，可选导出 DOCX |
| `legal-risk-visualization` | 将法律分析文本转为结构化风险图表 | 风险报告、雷达图、风险矩阵、影响路径图、决策树 |

## 技能概览

### `contract-review`

四层审查模型：

- 主体核验
- 基础文本审查
- 商务条款审查
- 法律条款审查

主要特点：

- 仅添加评论，不改原文
- 评论结构固定为问题类型、风险原因、修订建议
- 风险等级通过 reviewer 名称编码
- 生成合同摘要、综合意见和 Mermaid 业务流程图

### `contract-gen`

面向起草场景的合同生成技能，按“信息收集 → 合同生成 → 质量校验与输出”三阶段工作。

主要特点：

- 支持根据甲乙方立场做合法范围内的条款倾斜
- 按合同类型增删必备条款
- 缺失但无法推断的关键数据用 `[____]` 占位
- 可调用 `scripts/generate_contract.js` 导出 DOCX

### `law-to-markdown`

将法律文本转换为结构化 Markdown，并执行格式保真与结构校验。

标题层级对应：

| 层级 | Markdown |
|------|----------|
| 法律名称 | `#` |
| 编 / 分编 | `##` |
| 章 | `###` |
| 节 | `####` |
| 条 | `#####` |
| 款 / 项 / 目 | 无标题，按正文换行 |

主要特点：

- `.txt` 直接转换
- `.pdf` / `.docx` 优先联动 `mineru-ocr`
- 支持本地回退，但仅在用户明确同意时启用
- 默认执行 Stage 3 双重校验，确保文字内容保真

### `ad-compliance-review`

广告合规审核技能，采用“四阶段流水线”：

- 广告定性与分类
- 通用红线审核
- 行业专项审核
- 生成审核报告

覆盖《广告法》《反不正当竞争法》以及房地产、食品、医疗、药品、互联网广告等专项规则。

### `food-label-review`

预包装食品标签合规审核技能，采用“四阶段流水线”：

- 版本确定与预筛
- 一般标签审核
- 营养标签审核
- 生成审核报告

主要特点：

- 支持 `2011` 版与 `2025` 版标准
- 同时覆盖一般标签与营养标签
- 适配直接消费者、B2B、进口预包装食品三类场景

### `legal-risk-visualization`

将法律分析文本转为四层风险可视化输出：

- 风险雷达图
- 风险矩阵
- 影响路径图
- 决策树

主要特点：

- 以影响路径图为唯一底层数据源
- 同时面向法律团队和业务决策者
- 支持输出 Markdown 报告和 PNG 图片

## 仓库结构

```text
.
├── README.md
├── LICENSE
├── contract-review/
├── contract-gen/
├── law-to-markdown/
├── ad-compliance-review/
├── food-label-review/
└── legal-risk-visualization/
```

单个技能目录通常包含以下内容：

- `SKILL.md`：技能入口与执行规则
- `references/`：法规、模板、检查清单或方法说明
- `scripts/`：导出、渲染、校验等辅助脚本
- `assets/`：报告模板、静态资源

## 安装

### Claude Code

将所需技能目录复制到：

```bash
~/.claude/skills/
```

### Codex

将所需技能目录复制到：

```bash
~/.codex/skills/
```

安装时请保持目录名和 `SKILL.md` 文件名不变，并一并复制该技能依赖的 `references/`、`scripts/`、`assets/`。


## 许可证

本仓库所有技能统一采用 Apache License 2.0，许可证原文见仓库根目录 `LICENSE`。

SPDX-License-Identifier: Apache-2.0

Copyright (c) 2026 JiCheng
