# 面试题

## Q1：mysqldump 的 `--single-transaction` 原理是什么？

**考点**：不只是会用，要理解为什么不会锁表。

**回答**：备份开始时执行 `SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ` 和 `START TRANSACTION WITH CONSISTENT SNAPSHOT`。InnoDB 的 MVCC 机制保证——整个备份过程读到的是备份开始时刻的一致性快照，即使其他事务在修改数据，也不影响备份的一致性。因此不需要锁表。

**加分点**：能说出这个参数只对 InnoDB 有效。如果库里有 MyISAM 表，MyISAM 不支持 MVCC，仍然会锁。能解释 `--master-data=2` 和 `--single-transaction` 组合使用的必要性。

## Q2：逻辑备份和物理备份怎么选？

**考点**：理解两种备份策略的边界。

**回答**：看三个指标——(1) 数据量：< 10GB 用 mysqldump（简单方便），> 10GB 用 XtraBackup（恢复快），(2) 恢复时间要求：如果能接受 1 小时恢复 → mysqldump，要求 5 分钟内恢复 → XtraBackup，(3) 跨版本需求：需要跨 MySQL 大版本恢复 → 逻辑备份（SQL 通用），不需要 → 物理备份（更快）。

**加分点**：能说出混合策略——每周一次全量备份（XtraBackup）+ 每天增量备份（binlog），既能快速恢复又节省空间。
