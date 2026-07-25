# qzz-mysql — MySQL 知识库

面向大学生和初级开发工程师的 MySQL 结构化知识库。从零到能干活，覆盖 MySQL 8.0 核心知识。

## 怎么用

1. 先看 [roadmap.md](roadmap.md) — 确定学习路线
2. 按编号顺序学，01 → 02 → 03 ……
3. 需要查概念时用 [glossary.md](glossary.md) 快速定位
4. 每篇文章看完就动手敲，别光读

## 目录

| # | 章节 | 学什么 | 篇数 |
|---|------|--------|------|
| 01 | [基础知识](knowledge/01-basic/) | 数据库是什么 → 安装 → 客户端 → 第一条 SELECT | 4 |
| 02 | [DDL 数据定义](knowledge/02-ddl/) | 建库、建表、数据类型、约束、修改表结构 | 5 |
| 03 | [DML 数据操作](knowledge/03-dml/) | INSERT、UPDATE、DELETE | 3 |
| 04 | [查询](knowledge/04-query/) | SELECT、WHERE、排序分页、JOIN、子查询、UNION、CTE | 8 |
| 05 | [函数](knowledge/05-function/) | 聚合、字符串、日期、窗口函数、条件函数、存储过程 | 6 |
| 06 | [索引](knowledge/06-index/) | B+Tree、聚簇/二级索引、联合索引、覆盖索引、何时建索引 | 6 |
| 07 | [事务](knowledge/07-transaction/) | 事务基础、ACID、隔离级别、MVCC | 4 |
| 08 | [锁](knowledge/08-lock/) | 表锁、行锁（Record/Gap/Next-Key）、死锁、乐观锁与悲观锁 | 4 |
| 09 | [执行流程](knowledge/09-execution/) | SQL 生命周期、索引下推、redo/undo log、两阶段提交 | 4 |
| 10 | [性能优化](knowledge/10-performance/) | EXPLAIN、慢查询日志、SQL 优化、配置调优 | 4 |
| 11 | [数据库设计](knowledge/11-design/) | ER 模型、范式、命名规范、常见设计模式 | 4 |
| 12 | [存储引擎](knowledge/12-engine/) | InnoDB 架构、Buffer Pool、Change Buffer、MyISAM 对比 | 4 |
| 13 | [主从复制](knowledge/13-replication/) | 主从搭建、读写分离、主从延迟 | 3 |
| 14 | [备份与恢复](knowledge/14-backup/) | mysqldump、XtraBackup、时间点恢复 | 3 |
| 15 | [安全](knowledge/15-security/) | 用户权限、SQL 注入防护、SSL/TLS 加密 | 3 |
| 16 | [集群](knowledge/16-cluster/) | 高可用、数据库代理、分库分表 | 3 |
| 17 | [源码](knowledge/17-source/) | 源码结构、InnoDB 源码导读、编译与调试 | 3 |

**总计：17 章 / 71 个概念**

## 每个概念包含

| 文件 | 内容 |
|------|------|
| `README.md` | 正文：为什么需要 → 是什么 → 怎么工作 → 怎么用 → 注意事项（200-500 字） |
| `metadata.yaml` | 元数据：章节、难度、前置概念、标签 |
| `examples.md` | 可独立运行的代码示例 |
| `exercises.md` | 基础练习 + 进阶练习 + 答案 |
| `mistakes.md` | 常见错误：症状 → 原因 → 修复 |
| `interview.md` | 面试题：考点 → 回答 → 加分点 |
| `references.md` | 官方文档和公开文章链接 |

## 目录结构

```
qzz-mysql/
├── SKILL.md           # 技能定义
├── README.md          # 本文档
├── metadata.yaml      # 技能级元数据
├── glossary.md        # 术语速查表
├── roadmap.md         # 五阶段学习路线
├── knowledge/         # 17 章知识内容
├── assets/            # 配图、SQL 文件、数据集
├── references/        # 外部参考资料索引
└── tests/             # 测试和检查清单
```

## 配合技能

- 学某一个概念 → 用 `/qzz-explain` 深入讲解
- 不知道怎么学 → 用 `/qzz-roadmap` 生成路线
- 做练习 → 用 `/qzz-practice` 生成题目

## 维护

- 新增概念：从 `shared/templates/knowledge/` 复制 7 个文件到对应章节目录
- 校验：`python tools/lint.py && python tools/metadata.py`
- 生成目录：`python tools/toc.py --output skills/qzz-mysql/knowledge/TOC.md`
- 章节编号固定（01-17），新概念追加到对应章节末尾，不插入新章节
