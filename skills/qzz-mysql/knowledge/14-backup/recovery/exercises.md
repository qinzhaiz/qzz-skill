# 练习

## 基础练习

1. 在测试环境做一次"误删表 → 从备份恢复"的完整演练。记录每个步骤的耗时，评估 RTO。

2. 用 `mysqlbinlog` 查看一个 binlog 文件，找到其中的一条 INSERT 和 DELETE 语句。理解 binlog 的 ROW 格式如何记录数据变更。

## 进阶练习

1. 设计一个完整的灾难恢复预案：包括恢复步骤、每个步骤的预估时间、依赖条件（备份文件路径、binlog 位置等）。

2. 调研 binlog2sql 或 MyFlash 工具，尝试用它们自动生成误删操作的反向 SQL。

## 答案

1. 恢复演练步骤：(a) 确认备份文件完整性，(b) 恢复全量备份，(c) 回放 binlog，(d) 验证数据一致性。记录每步耗时 → 全量恢复通常是最大时间开销。

2. ROW 格式 binlog 记录行变更的具体数据：`### INSERT INTO db.table ### SET @1=1 @2='data'` / `### DELETE FROM db.table ### WHERE @1=1 @2='old_data'`。

3. 恢复预案关键元素：备份位置（/backup/mysql/）、全量备份周期（每周日）、binlog 保留天数（14 天）、恢复步骤清单、每步负责人、验证方法（至少检查核心表的行数）、预估 RTO（2-4 小时）。

4. binlog2sql：`python binlog2sql.py -h127.0.0.1 -P3306 -uadmin -p'admin' -d mydb -t user --start-file='mysql-bin.000050' --sql-only`。会生成满足过滤条件的 SQL 和对应的回滚 SQL（如 DELETE → INSERT）。
