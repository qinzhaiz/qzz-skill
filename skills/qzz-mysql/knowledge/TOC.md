# MySQL 知识库目录

17 章 · 71 个概念

## 01-basic
- [第一次查询](knowledge/01-basic/first-query/README.md)
- [安装 MySQL](knowledge/01-basic/install/README.md)
- [什么是数据库](knowledge/01-basic/what-is-database/README.md)
- [MySQL 是什么](knowledge/01-basic/what-is-mysql/README.md)

## 02-ddl
- [修改表](knowledge/02-ddl/alter-table/README.md)
- [约束](knowledge/02-ddl/constraints/README.md)
- [创建数据库](knowledge/02-ddl/create-database/README.md)
- [创建表](knowledge/02-ddl/create-table/README.md)
- [数据类型](knowledge/02-ddl/datatypes/README.md)

## 03-dml
- [删除数据](knowledge/03-dml/delete/README.md)
- [插入数据](knowledge/03-dml/insert/README.md)
- [更新数据](knowledge/03-dml/update/README.md)

## 04-query
- [CTE 公用表表达式](knowledge/04-query/cte/README.md)
- [分组统计](knowledge/04-query/group-by/README.md)
- [JOIN 联结](knowledge/04-query/join/README.md)
- [排序和分页](knowledge/04-query/order-limit/README.md)
- [SELECT 基础](knowledge/04-query/select-basic/README.md)
- [子查询](knowledge/04-query/subquery/README.md)
- [UNION 合并](knowledge/04-query/union/README.md)
- [WHERE 条件](knowledge/04-query/where/README.md)

## 05-function
- [聚合函数](knowledge/05-function/aggregate/README.md)
- [条件函数](knowledge/05-function/conditional/README.md)
- [日期函数](knowledge/05-function/date/README.md)
- [存储过程](knowledge/05-function/stored-procedure/README.md)
- [字符串函数](knowledge/05-function/string/README.md)
- [窗口函数](knowledge/05-function/window/README.md)

## 06-index
- [B+Tree 原理](knowledge/06-index/btree/README.md)
- [聚簇索引和二级索引](knowledge/06-index/clustered-secondary/README.md)
- [联合索引和最左前缀](knowledge/06-index/composite-index/README.md)
- [覆盖索引](knowledge/06-index/covering-index/README.md)
- [索引是什么](knowledge/06-index/what-is-index/README.md)
- [什么时候该建索引](knowledge/06-index/when-to-use/README.md)

## 07-transaction
- [ACID](knowledge/07-transaction/acid/README.md)
- [隔离级别](knowledge/07-transaction/isolation/README.md)
- [MVCC](knowledge/07-transaction/mvcc/README.md)
- [事务是什么](knowledge/07-transaction/what-is-transaction/README.md)

## 08-lock
- [死锁](knowledge/08-lock/deadlock/README.md)
- [乐观锁与悲观锁](knowledge/08-lock/optimistic-pessimistic/README.md)
- [行级锁](knowledge/08-lock/row-lock/README.md)
- [表级锁](knowledge/08-lock/table-lock/README.md)

## 09-execution
- [索引下推（ICP）](knowledge/09-execution/index-pushdown/README.md)
- [redo log 和 undo log](knowledge/09-execution/redo-undo-log/README.md)
- [SQL 执行流程](knowledge/09-execution/sql-lifecycle/README.md)
- [两阶段提交](knowledge/09-execution/two-phase-commit/README.md)

## 10-performance
- [配置调优](knowledge/10-performance/config-tuning/README.md)
- [EXPLAIN 执行计划](knowledge/10-performance/explain/README.md)
- [慢查询日志](knowledge/10-performance/slow-query/README.md)
- [SQL 优化](knowledge/10-performance/sql-optimization/README.md)

## 11-design
- [常见设计模式](knowledge/11-design/design-patterns/README.md)
- [ER 模型](knowledge/11-design/er-model/README.md)
- [命名规范](knowledge/11-design/naming-convention/README.md)
- [数据库范式](knowledge/11-design/normalization/README.md)

## 12-engine
- [Buffer Pool 详解](knowledge/12-engine/buffer-pool/README.md)
- [Change Buffer](knowledge/12-engine/change-buffer/README.md)
- [InnoDB 架构](knowledge/12-engine/innodb-architecture/README.md)
- [MyISAM 与 InnoDB](knowledge/12-engine/myisam-vs-innodb/README.md)

## 13-replication
- [主从复制](knowledge/13-replication/master-slave/README.md)
- [读写分离](knowledge/13-replication/read-write-split/README.md)
- [主从延迟](knowledge/13-replication/replication-lag/README.md)

## 14-backup
- [mysqldump 逻辑备份](knowledge/14-backup/mysqldump/README.md)
- [数据恢复](knowledge/14-backup/recovery/README.md)
- [XtraBackup 物理备份](knowledge/14-backup/xtrabackup/README.md)

## 15-security
- [SQL 注入防护](knowledge/15-security/sql-injection/README.md)
- [SSL/TLS 加密连接](knowledge/15-security/ssl/README.md)
- [用户与权限管理](knowledge/15-security/user-privileges/README.md)

## 16-cluster
- [高可用架构](knowledge/16-cluster/high-availability/README.md)
- [数据库代理](knowledge/16-cluster/proxy/README.md)
- [分库分表](knowledge/16-cluster/sharding/README.md)

## 17-source
- [编译与调试](knowledge/17-source/compile-debug/README.md)
- [InnoDB 源码导读](knowledge/17-source/innodb-source/README.md)
- [MySQL 源码结构](knowledge/17-source/source-structure/README.md)
