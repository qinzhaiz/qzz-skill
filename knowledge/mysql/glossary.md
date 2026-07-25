---
updated: 2026-07-25
---

# 术语表

> 按关键词快速定位到具体概念。中文术语按拼音排序，英文术语按字母排序。

## A–C

| 术语 | 章节 | 概念 |
|------|------|------|
| ACID | [07-transaction](07-transaction/acid/) | 原子性、一致性、隔离性、持久性 |
| ALTER TABLE | [02-ddl](02-ddl/alter-table/) | 修改表结构 |
| B+Tree | [06-index](06-index/btree/) | InnoDB 索引数据结构 |
| binlog | [09-execution](09-execution/two-phase-commit/) | Server 层逻辑日志，主从复制基础 |
| Buffer Pool | [12-engine](12-engine/buffer-pool/) | InnoDB 内存缓存区 |
| CASE WHEN | [05-function](05-function/conditional/) | 条件表达式 |
| Change Buffer | [12-engine](12-engine/change-buffer/) | 二级索引写缓冲 |
| COUNT(*) | [05-function](05-function/aggregate/) | 计数查询 |
| CTE | [04-query](04-query/cte/) | 公用表表达式（WITH 子句） |
| CREATE TABLE | [02-ddl](02-ddl/create-table/) | 建表 |

## D–F

| 术语 | 章节 | 概念 |
|------|------|------|
| DDL | [02-ddl](02-ddl/) | 数据定义语言 |
| DELETE | [03-dml](03-dml/delete/) | 删除数据 |
| DISTINCT | [04-query](04-query/select-basic/) | 去重查询 |
| doublewrite buffer | [12-engine](12-engine/innodb-architecture/) | 防部分写损坏 |
| ER 模型 | [11-design](11-design/er-model/) | 实体关系建模 |
| EXPLAIN | [10-performance](10-performance/explain/) | 查看执行计划 |
| FOR UPDATE | [08-lock](08-lock/row-lock/) | 排他锁查询 |
| FOR SHARE | [08-lock](08-lock/row-lock/) | 共享锁查询 |

## G–I

| 术语 | 章节 | 概念 |
|------|------|------|
| GROUP BY | [04-query](04-query/group-by/) | 分组聚合 |
| GTID | [13-replication](13-replication/master-slave/) | 全局事务 ID |
| HAVING | [04-query](04-query/group-by/) | 分组后过滤 |
| ICP | [09-execution](09-execution/index-pushdown/) | 索引条件下推 |
| InnoDB | [12-engine](12-engine/innodb-architecture/) | 默认存储引擎 |
| INSERT | [03-dml](03-dml/insert/) | 插入数据 |
| InnoDB Cluster | [16-cluster](16-cluster/high-availability/) | 官方高可用方案 |

## J–L

| 术语 | 章节 | 概念 |
|------|------|------|
| JOIN | [04-query](04-query/join/) | 多表连接查询 |
| JSON 列 | [02-ddl](02-ddl/datatypes/) | JSON 数据类型 |
| LIKE | [04-query](04-query/where/) | 模糊匹配 |
| LIMIT | [04-query](04-query/order-limit/) | 限制返回行数 |
| LOCK TABLES | [08-lock](08-lock/table-lock/) | 手动表锁 |

## M–O

| 术语 | 章节 | 概念 |
|------|------|------|
| MDL | [08-lock](08-lock/table-lock/) | 元数据锁 |
| MVCC | [07-transaction](07-transaction/mvcc/) | 多版本并发控制 |
| MyISAM | [12-engine](12-engine/myisam-vs-innodb/) | 旧存储引擎（已过时） |
| MySQL Router | [16-cluster](16-cluster/proxy/) | 官方数据库代理 |
| mysqldump | [14-backup](14-backup/mysqldump/) | 逻辑备份工具 |
| Next-Key Lock | [08-lock](08-lock/row-lock/) | 行锁 + 间隙锁 |
| NULL | [04-query](04-query/where/) | 空值处理 |
| ORDER BY | [04-query](04-query/order-limit/) | 排序 |

## P–R

| 术语 | 章节 | 概念 |
|------|------|------|
| PRIMARY KEY | [02-ddl](02-ddl/constraints/) | 主键约束 |
| ProxySQL | [16-cluster](16-cluster/proxy/) | 第三方数据库代理 |
| ReadView | [07-transaction](07-transaction/mvcc/) | 快照读的可见性判断 |
| redo log | [09-execution](09-execution/redo-undo-log/) | InnoDB 物理日志，崩溃恢复 |
| RELAY LOG | [13-replication](13-replication/master-slave/) | 从库中继日志 |

## S–U

| 术语 | 章节 | 概念 |
|------|------|------|
| SQL 注入 | [15-security](15-security/sql-injection/) | 注入攻击与参数化查询防御 |
| SSL/TLS | [15-security](15-security/ssl/) | 加密连接 |
| SUBQUERY | [04-query](04-query/subquery/) | 子查询 |
| UNDO LOG | [09-execution](09-execution/redo-undo-log/) | 回滚日志 + MVCC 版本链 |
| UNION | [04-query](04-query/union/) | 结果集合并 |
| UPDATE | [03-dml](03-dml/update/) | 更新数据 |

## V–Z

| 术语 | 章节 | 概念 |
|------|------|------|
| WAL | [09-execution](09-execution/redo-undo-log/) | 预写日志 |
| WHERE | [04-query](04-query/where/) | 条件过滤 |
| WINDOW FUNCTION | [05-function](05-function/window/) | 窗口函数 |
| XtraBackup | [14-backup](14-backup/xtrabackup/) | 物理热备份工具 |

## 中文术语（拼音排序）

| 术语 | 章节 | 概念 |
|------|------|------|
| 安装 | [01-basic](01-basic/install/) | MySQL 安装 |
| 悲观锁 | [08-lock](08-lock/optimistic-pessimistic/) | FOR UPDATE |
| 编译源码 | [17-source](17-source/compile-debug/) | 编译与调试 MySQL |
| 表锁 | [08-lock](08-lock/table-lock/) | 表级锁 |
| 查询缓存（已删除） | [09-execution](09-execution/sql-lifecycle/) | MySQL 8.0 已移除 |
| 存储过程 | [05-function](05-function/stored-procedure/) | CREATE PROCEDURE |
| 存储引擎 | [12-engine](12-engine/innodb-architecture/) | InnoDB 架构 |
| 读写分离 | [13-replication](13-replication/read-write-split/) | 主写从读 |
| 范式 | [11-design](11-design/normalization/) | 1NF / 2NF / 3NF |
| 反范式化 | [11-design](11-design/normalization/) | 故意冗余优化查询 |
| 分库分表 | [16-cluster](16-cluster/sharding/) | 水平拆分 |
| 覆盖索引 | [06-index](06-index/covering-index/) | 不回表 |
| 隔离级别 | [07-transaction](07-transaction/isolation/) | RU / RC / RR / Serializable |
| 故障切换 | [16-cluster](16-cluster/high-availability/) | Failover |
| 行锁 | [08-lock](08-lock/row-lock/) | 行级锁 |
| 回表 | [06-index](06-index/clustered-secondary/) | 二级索引回聚簇索引取数据 |
| 恢复 | [14-backup](14-backup/recovery/) | 数据恢复 / PITR |
| 间隙锁 | [08-lock](08-lock/row-lock/) | Gap Lock 防幻读 |
| 聚簇索引 | [06-index](06-index/clustered-secondary/) | 主键索引 |
| 乐观锁 | [08-lock](08-lock/optimistic-pessimistic/) | 版本号 CAS |
| 联合索引 | [06-index](06-index/composite-index/) | 多列索引 |
| 两阶段提交 | [09-execution](09-execution/two-phase-commit/) | redo + binlog 一致性 |
| 慢查询 | [10-performance](10-performance/slow-query/) | 慢查询日志分析 |
| 命名规范 | [11-design](11-design/naming-convention/) | 表/字段/索引命名 |
| 配置调优 | [10-performance](10-performance/config-tuning/) | my.cnf 参数优化 |
| 权限管理 | [15-security](15-security/user-privileges/) | GRANT / REVOKE |
| 软删除 | [11-design](11-design/design-patterns/) | 标记删除替代真删除 |
| 数据库代理 | [16-cluster](16-cluster/proxy/) | ProxySQL / MySQL Router |
| 数据库设计 | [11-design](11-design/er-model/) | ER 图 + 范式 |
| 数据类型 | [02-ddl](02-ddl/datatypes/) | INT / VARCHAR / DECIMAL / DATE |
| 死锁 | [08-lock](08-lock/deadlock/) | 死锁检测与处理 |
| 索引 | [06-index](06-index/what-is-index/) | 索引基础 |
| 索引下推 | [09-execution](09-execution/index-pushdown/) | ICP 减少回表 |
| 事务 | [07-transaction](07-transaction/what-is-transaction/) | BEGIN / COMMIT / ROLLBACK |
| 外键 | [02-ddl](02-ddl/constraints/) | FOREIGN KEY |
| 唯一约束 | [02-ddl](02-ddl/constraints/) | UNIQUE |
| 性能优化 | [10-performance](10-performance/sql-optimization/) | SQL 改写技巧 |
| 预处理语句 | [15-security](15-security/sql-injection/) | 参数化查询 |
| 源码结构 | [17-source](17-source/source-structure/) | MySQL 源码目录 |
| 主从复制 | [13-replication](13-replication/master-slave/) | binlog 同步 |
| 主从延迟 | [13-replication](13-replication/replication-lag/) | Seconds_Behind_Master |
| 最左前缀 | [06-index](06-index/composite-index/) | 联合索引匹配规则 |
