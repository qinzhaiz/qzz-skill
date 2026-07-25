# 练习

## 基础练习

1. 用 mysqldump 备份自己的测试数据库，查看生成的 SQL 文件内容。找一个 CREATE TABLE 语句和一条 INSERT 语句，理解它们的格式。

2. 比较 `--single-transaction` 和 `--lock-tables` 的区别。分别在 InnoDB 和 MyISAM 表上测试，观察哪种情况会锁表。

## 进阶练习

1. 写一个 shell 脚本：每天凌晨 3 点自动备份，保留最近 7 天的备份文件，自动删除过期备份。加上日志记录和失败告警。

2. 在 10GB 和 100MB 数据库上分别用 mysqldump 做备份和恢复。对比时间和文件大小，评估 mysqldump 的适用边界。

## 答案

1. SQL 文件中包含 DDL（CREATE TABLE）+ DML（INSERT）。InnoDB 表用 `--single-transaction` 不锁表（基于 MVCC 快照），MyISAM 表必须 `--lock-tables` 才能获得一致性备份。

2. 脚本关键：`mysqldump ... | gzip > file` + `find ... -mtime +7 -delete` + `echo "$(date) backup done/failed" >> backup.log`。定时用 cron：`0 3 * * * /path/to/backup.sh`。

3. 100MB 数据库：备份几秒，恢复几秒。10GB 数据库：备份 5-20 分钟，恢复 30-60 分钟。超过 10GB 恢复时间急剧增长（逐行 INSERT 的瓶颈），建议用 XtraBackup。
