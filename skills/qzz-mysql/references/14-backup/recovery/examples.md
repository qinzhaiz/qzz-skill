# 代码示例

## 示例 1：误删表恢复流程

**场景**：运维误执行了 `DROP TABLE orders`，需要恢复。

```bash
# 1. 立即锁定表写入（防止更多数据变更加大恢复难度）
# 或从库断开复制，保护现有 binlog

# 2. 找到最近一次全量备份
ls -la /backup/mysql/

# 3. 找到包含 DROP TABLE 的 binlog 文件和位置
mysqlbinlog --start-datetime="2026-07-27 14:00:00" \
  /var/log/mysql/mysql-bin.000050 | grep -A5 "DROP TABLE"

# 假设发现 DROP TABLE 在 position 12345678

# 4. 恢复全量备份到临时库
mysql -u root -p -e "CREATE DATABASE recovery_tmp"
mysql -u root -p recovery_tmp < /backup/mysql/full_20260727.sql

# 5. 回放 binlog 到 DROP 前一刻
mysqlbinlog --stop-position=12345677 \
  /var/log/mysql/mysql-bin.000050 | mysql -u root -p recovery_tmp

# 6. 导出 orders 表并导入回主库
mysqldump -u root -p recovery_tmp orders | mysql -u root -p production_db

# 7. 验证数据正确后，清理临时库
mysql -u root -p -e "DROP DATABASE recovery_tmp"
```

## 示例 2：时间点恢复（PITR）

**场景**：应用 bug 在 15:30:00 开始写错了数据，需要恢复到 15:29:59。

```bash
# 1. 恢复全量备份
xtrabackup --prepare --target-dir=/backup/full_20260727
systemctl stop mysql
rm -rf /var/lib/mysql/*
xtrabackup --copy-back --target-dir=/backup/full_20260727
chown -R mysql:mysql /var/lib/mysql
systemctl start mysql

# 2. 找到需要回放的 binlog 文件（从全量备份之后）
# 全量备份中的 xtrabackup_binlog_info 记录了 binlog 位置
cat /backup/full_20260727/xtrabackup_binlog_info
# mysql-bin.000048  123456

# 3. 回放 binlog 到指定时间点
mysqlbinlog --start-position=123456 \
            --stop-datetime="2026-07-27 15:29:59" \
            /var/log/mysql/mysql-bin.000048 \
            /var/log/mysql/mysql-bin.000049 \
            /var/log/mysql/mysql-bin.000050 | mysql -u root -p

# 4. 验证数据是否正确
```

## 示例 3：用 binlog 验证恢复范围

```bash
# 查看 binlog 中包含哪些数据库和时间范围
mysqlbinlog --no-defaults mysql-bin.000048 | head -50

# 过滤特定数据库的变更
mysqlbinlog --database=mydb mysql-bin.000048 | less

# 查看指定时间段的 binlog（先确认恢复范围是否正确）
mysqlbinlog --start-datetime="2026-07-27 00:00:00" \
            --stop-datetime="2026-07-27 15:30:00" \
            mysql-bin.000048 | grep -E "(INSERT|UPDATE|DELETE)"
```

## 示例 4：恢复完整性校验

```bash
#!/bin/bash
# 每月自动恢复测试脚本

BACKUP_DIR="/backup/mysql/full_current"
TEST_DATA="/tmp/recovery_test"

# 恢复备份
xtrabackup --prepare --target-dir="$BACKUP_DIR"
rm -rf "$TEST_DATA"
mkdir -p "$TEST_DATA"
xtrabackup --copy-back --target-dir="$BACKUP_DIR" --datadir="$TEST_DATA"

# 启动测试实例
mysqld --datadir="$TEST_DATA" --port=3307 --socket=/tmp/mysql_test.sock &

# 等待启动
sleep 10

# 检查每张表的行数是否和预期一致
mysql -S /tmp/mysql_test.sock -e "
  SELECT TABLE_NAME, TABLE_ROWS
  FROM information_schema.TABLES
  WHERE TABLE_SCHEMA NOT IN ('information_schema','mysql','performance_schema','sys');
" > /tmp/recovery_report.txt

# 发送验证报告
mail -s "Monthly Recovery Test Report" dba@example.com < /tmp/recovery_report.txt

# 清理
mysqladmin -S /tmp/mysql_test.sock shutdown
rm -rf "$TEST_DATA"
```
