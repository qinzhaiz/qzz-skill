# mysqldump 逻辑备份

> MySQL 自带的备份工具——把数据库导出为 SQL 文件，简单可靠，适合中小数据量。

## 为什么需要它

数据是公司最重要的资产。误删一张表、磁盘损坏、服务器宕机——任何一种情况都可能导致数据丢失。mysqldump 是最简单、最通用的备份方案：一条命令把数据导出成 SQL 文件，恢复时再导入回去。

## 它是什么

mysqldump 是 MySQL 自带的**逻辑备份**工具——它不复制数据文件，而是**读取数据库中的表结构和数据，生成 CREATE TABLE 和 INSERT 语句**。恢复时逐一执行这些 SQL 语句，重建表和数据。

逻辑备份 vs 物理备份：

| | 逻辑备份（mysqldump） | 物理备份（XtraBackup） |
|---|---|---|
| **备份内容** | SQL 语句（CREATE + INSERT） | 原始数据文件（.ibd） |
| **备份速度** | 慢（逐行读取） | 快（直接复制文件） |
| **恢复速度** | 慢（逐行执行 SQL） | 快（复制回去就行） |
| **灵活性** | 可以跨版本、跨引擎 | 必须同版本、同平台 |
| **适用数据量** | < 10GB | 任意大小 |

## 怎么工作

### 一致性备份的关键参数

```bash
# InnoDB 表：不打锁，用 MVCC 得到一致性快照
mysqldump --single-transaction --routines --triggers \
  -u root -p dbname > backup.sql

# MyISAM 表：必须锁表才能保证一致性
mysqldump --lock-tables -u root -p dbname > backup.sql
```sql

`--single-transaction` 的原理：在备份开始前执行 `START TRANSACTION WITH CONSISTENT SNAPSHOT`，利用 InnoDB 的 MVCC 机制——之后读到的数据都是备份开始时刻的快照，不需要锁表。

### 常用选项

| 选项 | 作用 |
|------|------|
| `--single-transaction` | 一致性快照，不锁表（InnoDB） |
| `--routines` | 导出存储过程和函数 |
| `--triggers` | 导出触发器 |
| `--events` | 导出事件调度器 |
| `--master-data=2` | 记录 binlog 位置（注释形式），用于搭建主从 |
| `--dump-date` | 在文件头部记录备份时间 |
| `--all-databases` | 备份所有库 |
| `--no-data` | 只导出表结构，不导出数据 |

## 怎么用

```bash
# 1. 备份单个数据库
mysqldump -u root -p mydb > mydb_backup.sql

# 2. 备份所有数据库
mysqldump --all-databases --single-transaction \
  -u root -p > all_backup.sql

# 3. 备份单张表
mysqldump -u root -p mydb user > user_backup.sql

# 4. 只导出表结构（不要数据）
mysqldump --no-data -u root -p mydb > schema.sql

# 5. InnoDB 一致性备份（生产环境推荐）
mysqldump --single-transaction --routines --triggers \
  --master-data=2 -u root -p mydb > mydb_$(date +%Y%m%d).sql

# 6. 压缩备份（节省空间）
mysqldump --single-transaction -u root -p mydb | gzip > mydb.sql.gz

# 7. 恢复
mysql -u root -p mydb < mydb_backup.sql
# 或先创建空库再导入
gunzip < mydb.sql.gz | mysql -u root -p mydb
```sql

## 注意事项

1. **`--single-transaction` 只对 InnoDB 有效**：如果有 MyISAM 表，还是会锁。确认数据库中表的引擎后再选参数。
2. **大表恢复非常慢**：INSERT 是逐行执行的，几十 GB 的 SQL 文件恢复可能需要几小时。大数据库用 XtraBackup。
3. **备份期间不影响读写**（用了 `--single-transaction`）：但会增加主库的 IO 负载。建议在从库做备份。
4. **备份文件是纯文本**：可以手动编辑（比如只恢复某几条数据），但文件很大时 gzip 压缩是标配。

## 和什么有关

- [XtraBackup 物理备份](../xtrabackup/) —— 大数据库的备份选择
- [数据恢复](../recovery/) —— 备份的最终目的是恢复
- [主从复制](../../13-replication/master-slave/) —— 在从库做备份减少主库压力
