# MySQL 知识库（源码）

> ⚠️ 这里是编辑用的源码目录。构建后拷贝到 `skills/qzz-mysql/references/mysql/`，通过 `npx skills add qinzhaiz/qzz-skill --skill qzz-mysql` 安装。

面向大学生和初级开发工程师，从零到能干活。71 个概念，覆盖 MySQL 8.0 核心知识。

## 怎么用

1. 先看 [roadmap.md](roadmap.md) — 确定学习路线
2. 按编号顺序学，01 → 02 → 03 ……
3. 需要查概念时用 [glossary.md](glossary.md)
4. 每篇文章看完就敲，别光读

## 目录

| # | 章节 | 学什么 | 篇数 |
|---|------|--------|------|
| 01 | [基础知识](01-basic/) | 数据库是什么 → 安装 → 客户端 → 第一条SELECT | 4 |
| 02 | [DDL 数据定义](02-ddl/) | 建库、建表、数据类型、约束、修改表结构 | 5 |
| 03 | [DML 数据操作](03-dml/) | INSERT、UPDATE、DELETE | 3 |
| 04 | [查询](04-query/) | SELECT、WHERE、排序分页、JOIN、子查询、UNION、CTE | 8 |
| 05 | [函数](05-function/) | 聚合、字符串、日期、窗口函数、条件函数、存储过程 | 6 |
| 06 | [索引](06-index/) | B+Tree、聚簇/二级索引、联合索引、覆盖索引、何时建索引 | 6 |
| 07 | [事务](07-transaction/) | 事务基础、ACID、隔离级别、MVCC | 4 |
| 08 | [锁](08-lock/) | 表锁、行锁（Record/Gap/Next-Key）、死锁、乐观锁与悲观锁 | 4 |
| 09 | [执行流程](09-execution/) | SQL 生命周期、索引下推、redo/undo log、两阶段提交 | 4 |
| 10 | [性能优化](10-performance/) | EXPLAIN、慢查询日志、SQL 优化、配置调优 | 4 |
| 11 | [数据库设计](11-design/) | ER 模型、范式、命名规范、常见设计模式 | 4 |
| 12 | [存储引擎](12-engine/) | InnoDB 架构、Buffer Pool、Change Buffer、MyISAM 对比 | 4 |
| 13 | [主从复制](13-replication/) | 主从搭建、读写分离、主从延迟 | 3 |
| 14 | [备份与恢复](14-backup/) | mysqldump、XtraBackup、时间点恢复 | 3 |
| 15 | [安全](15-security/) | 用户权限、SQL 注入防护、SSL/TLS 加密 | 3 |
| 16 | [集群](16-cluster/) | 高可用、数据库代理、分库分表 | 3 |
| 17 | [源码](17-source/) | 源码结构、InnoDB 源码导读、编译与调试 | 3 |

**总计：17 章 / 71 个概念**

每个概念包含 7 个标准文件：正文（README.md）+ 元数据 + 示例 + 练习 + 常见错误 + 面试题 + 参考资料。

## 配合技能

- 学某一个概念 → 用 `/qzz-explain` 深入讲解
- 不知道怎么学 → 用 `/qzz-roadmap` 生成路线
