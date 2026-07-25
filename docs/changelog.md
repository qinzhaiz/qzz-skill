# Changelog

## 2026-07-25 — 架构重构 v2

### 变更

- 新增 `docs/architecture.md` 和 `docs/conventions/`（5 个规范文件）
- 重新组织 `shared/templates/`：拆分为 `knowledge/`、`skill/knowledge/`、`skill/flow/`、`metadata/`
- 明确区分两种技能类型：知识型和流程型
- MySQL 知识库从 `knowledge/mysql/` 迁移到 `skills/qzz-mysql/knowledge/`
- 新增 `skills/qzz-practice/`（练习）
- 新增 `tools/lint.py`、`tools/toc.py`、`tools/metadata.py`
- 新增 `scripts/` 目录（build.ps1, release.ps1, test.ps1）
- `CLAUDE.md` 精简为 AI 最小上下文

### 原因

从 "3 个 skill + 1 个知识库的临时结构" 升级为 "可扩展的多技能体系"。核心驱动：
1. 知识库应与对应技能内聚（而非根目录独立）
2. 不同技能类型需要不同目录模板
3. 维护文档和 AI 指令应分离
