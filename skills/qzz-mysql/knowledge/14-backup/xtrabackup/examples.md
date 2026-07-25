# 代码示例

## 示例 1：生产环境备份脚本

```bash
#!/bin/bash
# XtraBackup 每日备份脚本：全量 + 增量

BACKUP_BASE="/backup/mysql"
DATE=$(date +%Y%m%d)
DAY_OF_WEEK=$(date +%u)  # 1=周一 ... 7=周日

if [ "$DAY_OF_WEEK" -eq 1 ]; then
    # 周一：全量备份
    TARGET_DIR="${BACKUP_BASE}/full_${DATE}"
    mkdir -p "$TARGET_DIR"
    xtrabackup --backup \
      --target-dir="$TARGET_DIR" \
      --user=backup --password=secret \
      --parallel=4 --compress
    echo "Full backup: $TARGET_DIR"
else
    # 周二~周日：增量备份（基于最近一次全量）
    LATEST_FULL=$(ls -d ${BACKUP_BASE}/full_* | tail -1)
    TARGET_DIR="${BACKUP_BASE}/inc_${DATE}"
    mkdir -p "$TARGET_DIR"
    xtrabackup --backup \
      --target-dir="$TARGET_DIR" \
      --incremental-basedir="$LATEST_FULL" \
      --user=backup --password=secret \
      --parallel=4
    echo "Incremental backup: $TARGET_DIR (based on $LATEST_FULL)"
fi

# 删除 30 天前的备份
find "$BACKUP_BASE" -type d -mtime +30 -exec rm -rf {} \;
```sql

## 示例 2：压缩备份节省空间

```bash
# 备份时压缩（qpress 算法）
xtrabackup --backup \
  --target-dir=/backup/full \
  --compress --compress-threads=4 \
  --user=root --password=secret

# 恢复前需要解压
xtrabackup --decompress --target-dir=/backup/full
# 然后正常 prepare
xtrabackup --prepare --target-dir=/backup/full
```sql

## 示例 3：在从库做备份

```bash
#!/bin/bash
# 在从库上做备份：先暂停复制 → 备份 → 恢复复制
# 好处：不影响主库性能，从库可以随时暂停

# 1. 暂停复制
mysql -u root -p -e "STOP SLAVE SQL_THREAD;"

# 2. 备份（包括 binlog 位置信息）
xtrabackup --backup \
  --target-dir=/backup/from_slave \
  --slave-info \  # 记录从库的主库 binlog 位置
  --user=root --password=secret

# 3. 恢复复制
mysql -u root -p -e "START SLAVE SQL_THREAD;"

echo "Backup completed on slave"
```sql

## 示例 4：验证备份是否可用

```bash
# 备份完成后验证备份完整性
xtrabackup --prepare --target-dir=/backup/full
# 如果 prepare 成功完成且没有任何错误输出 → 备份可用

# 定期恢复测试：用备份启动一个临时实例验证
mkdir /tmp/test_mysql
xtrabackup --copy-back --target-dir=/backup/full --datadir=/tmp/test_mysql
# 在临时实例上启动 MySQL 验证数据完整性
```
