---
name: qzz-mysql
description: >
  MySQL 结构化知识库。包含 17 章的完整学习资料：基础→DDL→DML→查询→函数→索引→事务→锁→执行→优化→设计→引擎→复制→备份→安全→集群→源码。当用户问 MySQL 相关问题、需要查 MySQL 文档、做练习、准备面试、或需要理解 MySQL 底层原理时使用。每个概念含正文、代码示例、练习题、常见错误、面试题和参考资料。
license: CC BY-NC 4.0
---

# Purpose

MySQL 结构化知识库，面向大学生和初级开发工程师。17 章覆盖从基础到源码的完整学习路径，每章包含若干概念，每个概念含 7 个文件（正文、示例、练习、常见错误、面试题、参考资料、元数据）。

## 知识库结构

```
knowledge/
├── 01-basic/                    ← 基础知识
├── 02-ddl/                      ← DDL
├── 03-dml/                      ← DML
├── 04-query/                    ← 查询
├── 05-function/                 ← 函数
├── 06-index/                    ← 索引
├── 07-transaction/              ← 事务
├── 08-lock/                     ← 锁
├── 09-execution/                ← 执行流程
├── 10-performance/              ← 性能优化
├── 11-design/                   ← 数据库设计
├── 12-engine/                   ← 存储引擎
├── 13-replication/              ← 主从复制
├── 14-backup/                   ← 备份恢复
├── 15-security/                 ← 安全
├── 16-cluster/                  ← 集群
└── 17-source/                   ← 源码
```

根目录另有 `roadmap.md`（学习路线）、`glossary.md`（术语速查表）。

# When to use

用户提出任何 MySQL 相关问题时触发：
- 问 MySQL 概念或原理："覆盖索引怎么工作？""事务的隔离级别是什么？"
- 查语法或用法："MySQL 怎么建表？""JOIN 有哪几种？"
- 做练习或测验："给我出几道 MySQL 的题"
- 准备面试："MySQL 索引面试问什么？"
- 排查问题："为什么我的查询这么慢？"

# Workflow

1. **查概念**：先查 `glossary.md` 定位概念所在章节
2. **读正文**：打开对应概念目录的 `README.md`
3. **看示例**：代码在 `examples.md`，可直接复制运行
4. **做练习**：基础题和进阶题在 `exercises.md`，答案附后
5. **避坑**：常见错误在 `mistakes.md`
6. **准备面试**：面试题在 `interview.md`
7. **扩展阅读**：官方文档链接在 `references.md`

已有内容直接提炼关键点回答，引导用户阅读原文和练习。没有覆盖或需要深讲时，切换到通用讲解模式（配合 `qzz-explain`），结束后可建议保存到知识库。

# Output style

- 提炼关键点直接回答，不照搬全文
- 引导用户阅读原文、做练习、看示例
- 配合 `qzz-explain` 深讲，配合 `qzz-roadmap` 生成学习路线

# Constraints

- 基于知识库已有内容回答，不凭空编造
- 中文正文，技术名词保留英文
- 基于 MySQL 8.0
- 不深入源码级实现细节（留给 17-source）
- 不引用版权书籍或付费内容
