# 代码示例

## 示例 1：生产环境完整备份脚本

```bash
#!/bin/bash
# MySQL 每日备份脚本

BACKUP_DIR="/backup/mysql"
DB_USER="root"
DB_PASS="your_password"
DB_NAME="mydb"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 执行备份
mysqldump --single-transaction \
          --routines \
          --triggers \
          --events \
          --master-data=2 \
          -u "$DB_USER" \
          -p"$DB_PASS" \
          "$DB_NAME" | gzip > "$BACKUP_FILE"

# 删除 7 天前的备份
find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
```

## 示例 2：用 mysqldump 搭建主从复制

```bash
# 从主库导出（记录 binlog 位置）
mysqldump --single-transaction \
          --master-data=2 \
          --all-databases \
          -u root -p > master_dump.sql

# 文件头部自动包含注释：
# -- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000012', MASTER_LOG_POS=123456;

# 导入到从库
mysql -u root -p < master_dump.sql

# 从库配置主库连接（利用导出文件中的位点）
CHANGE MASTER TO
  MASTER_HOST = '主库IP',
  MASTER_USER = 'repl',
  MASTER_PASSWORD = 'password',
  MASTER_LOG_FILE = 'mysql-bin.000012',
  MASTER_LOG_POS = 123456;

START SLAVE;
```

## 示例 3：部分表备份与恢复

```bash
# 只备份 user 和 orders 表
mysqldump -u root -p mydb user orders > partial_backup.sql

# 恢复时可以选择性恢复
mysql -u root -p mydb < partial_backup.sql

# 或者交互式恢复：只恢复 user 表、跳过 orders 表（手动编辑 SQL 文件）
```

## 示例 4：压缩备份对比

```bash
# 不压缩：10GB 数据库 → 约 6GB SQL 文件
mysqldump --single-transaction -u root -p mydb > backup.sql

# gzip 压缩：10GB 数据库 → 约 1GB 压缩文件
mysqldump --single-transaction -u root -p mydb | gzip > backup.sql.gz

# 恢复压缩文件（不需要先解压）
gunzip < backup.sql.gz | mysql -u root -p mydb
```
