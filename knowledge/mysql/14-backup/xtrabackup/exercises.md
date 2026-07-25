# 练习

## 基础练习

1. 在自己的测试环境安装 XtraBackup，对 MySQL 做一次全量备份和恢复。对比 mysqldump 备份同一数据库的时间。

2. 解释 XtraBackup 备份过程中的 prepare 阶段做了什么。如果忘了 prepare 直接恢复会发生什么？

## 进阶练习

1. 设计一个备份策略：每周日全量、每天增量。写脚本来实现这个策略，包括定期清理过期备份。

2. 用 `xtrabackup --slave-info` 在从库备份。查看备份目录中的 `xtrabackup_slave_info` 文件，理解如何在恢复时重建主从关系。

## 答案

1. XtraBackup 直接复制文件 → 速度快（与数据库大小成正比，通常几分钟到几十分钟）。mysqldump 逐行 SQL → 速度慢（几十分钟到几小时）。对比：100GB 数据库 XtraBackup 约 10-20 分钟，mysqldump 约 1-3 小时。

2. prepare 阶段对备份文件执行类似崩溃恢复的过程——用 redo log 重放备份期间产生的变更，使所有数据页达到一致状态。如果忘了 prepare 直接恢复 → 数据不一致，MySQL 可能无法启动或启动后数据损坏。

3. 脚本核心逻辑：(a) 周日做全量 `xtrabackup --backup`，(b) 周一~周六做增量 `--incremental-basedir` 指向上次备份，(c) 清理: `find /backup -mtime +30 -delete`，(d) 保留最近 4 周全量 + 对应的增量。

4. `xtrabackup_slave_info` 文件包含 `CHANGE MASTER TO` 语句。恢复后用这个文件中的 binlog 位置信息，可以把恢复后的数据库重新设置为从库。
