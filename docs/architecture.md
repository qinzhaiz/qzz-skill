# Architecture

## 项目定位

个人 Claude Code 技能仓库。用一个可扩展的目录结构管理两类资产：

- **技能（Skill）** — 给 Claude Code 用的指令集，通过 skills.sh 分发
- **知识库（Knowledge）** — 结构化技术知识，面向大学生和初级开发工程师，嵌入在对应 skill 内部

## 目录总览

```
qzz-skill/
├── README.md                    # 项目说明（给人看）
├── LICENSE                      # CC BY-NC 4.0
├── CLAUDE.md                    # AI 工作指令（给 Claude Code 看）
├── .gitignore
│
├── docs/                        # 项目自身的文档
│   ├── architecture.md          # 本文档：整体架构与设计决策
│   ├── conventions/             # 规范
│   │   ├── knowledge.md         # 知识库规范
│   │   ├── metadata.md          # 元数据格式
│   │   ├── naming.md            # 命名规范
│   │   ├── skill.md             # 技能开发规范
│   │   └── testing.md           # 测试规范
│   └── changelog.md             # 变更记录
│
├── research/                    # 原始参考资料（不提交 Git）
│   └── mysql/                   # MySQL 相关：PDF、克隆仓库、DeepWiki
│
├── shared/                      # 共享资源
│   ├── assets/                  # 全局静态资源
│   │   ├── logos/               # Logo 文件
│   │   └── icons/               # 图标文件
│   └── templates/               # 文件模板（新建概念/技能时从这里复制）
│       ├── knowledge/           # 知识概念模板（7 个文件 + assets/）
│       ├── skill/               # 技能模板
│       │   ├── knowledge/       # 知识型技能模板
│       │   └── flow/            # 流程型技能模板
│       └── metadata/            # 元数据模板
│
├── skills/                      # 技能定义（每个技能一个目录）
│   ├── qzz/                     # 编排入口
│   ├── qzz-explain/             # 讲解概念
│   ├── qzz-roadmap/             # 学习路线
│   ├── qzz-practice/            # 练习
│   └── qzz-mysql/               # MySQL 知识库
│
├── tools/                       # 数据处理脚本
│   ├── pdf2md.py                # PDF → Markdown
│   ├── mdclean.py               # Markdown 后处理
│   ├── lint.py                  # 知识库格式校验
│   ├── toc.py                   # 目录生成
│   └── metadata.py              # 元数据校验
│
└── scripts/                     # 项目工程脚本
    ├── build.ps1                # 构建
    ├── release.ps1              # 发布
    └── test.ps1                 # 测试
```

## 两种技能类型

### 知识型技能

维护结构化技术知识库的技能。目录结构：

```
skill-name/
├── SKILL.md                     # 技能定义（YAML frontmatter + Markdown）
├── README.md                    # 技能说明
├── metadata.yaml                # 技能级元数据
├── roadmap.md                   # 学习路线（可选）
├── glossary.md                  # 术语速查表（可选）
├── knowledge/                   # 知识章节
│   └── NN-topic/                # 章节目录（NN = 两位数字编号）
│       └── <concept>/           # 概念子目录
│           ├── README.md        # 正文
│           ├── metadata.yaml    # 概念元数据
│           ├── examples.md      # 代码示例
│           ├── exercises.md     # 练习 + 答案
│           ├── mistakes.md      # 常见错误
│           ├── interview.md     # 面试题
│           ├── references.md    # 参考资料
│           └── assets/          # 配图、SQL 文件
├── assets/                      # 技能级资源
│   ├── images/
│   ├── diagrams/
│   ├── sql/
│   └── datasets/
├── references/                  # 外部参考索引
└── tests/                       # 测试
    ├── checklist.md             # 检查清单
    ├── benchmark/               # 基准测试
    └── regression/              # 回归测试
```

当前实例：`qzz-mysql`

### 流程型技能

纯编排/流程类技能，不维护知识库。目录结构：

```
skill-name/
├── SKILL.md                     # 技能定义
├── README.md                    # 技能说明
├── examples/                    # 输入输出示例（可选）
└── assets/                      # 配图等资源（可选）
```

当前实例：`qzz`、`qzz-explain`、`qzz-roadmap`、`qzz-practice`

## 设计决策

### 为什么知识库放在 skill 内部而非根目录？

1. **内聚**：MySQL 知识库是 `qzz-mysql` 技能的核心资产，不是独立实体
2. **分发**：skills.sh 按 skill 目录分发，知识库随 skill 一起被用户安装
3. **扩展**：未来新增知识域（如 qzz-c、qzz-golang）时，各自的知识库独立内聚

### 为什么区分知识型和流程型？

两类技能的"最小完整单元"不同：

- 知识型需要概念模板（7 文件）、章节组织、测试验证——骨架重
- 流程型只需要 SKILL.md + README.md——骨架轻

强制统一模板会让流程型技能留下大量空目录。

### 为什么 docs/ 独立于 CLAUDE.md？

- `CLAUDE.md` = AI 需要的最小上下文（精简，避免 token 浪费）
- `docs/` = 人类维护者需要的完整文档（可以写得很详细）
- 两者各司其职，CLAUDE.md 不需要重复 docs/ 里的内容

### 为什么 tools/ 和 scripts/ 分开？

- `tools/` = 内容生产流水线（PDF 转换、格式清理、校验），操作对象是知识库内容
- `scripts/` = 项目工程自动化（构建、发布、测试），操作对象是整个仓库

## 章节编号

MySQL 知识库使用固定的两位数字编号：

```
01-basic → 02-ddl → 03-dml → 04-query → 05-function →
06-index → 07-transaction → 08-lock → 09-execution →
10-performance → 11-design → 12-engine → 13-replication →
14-backup → 15-security → 16-cluster → 17-source
```

编号不可变（章节之间有依赖引用）。新增章节插入到末尾。
