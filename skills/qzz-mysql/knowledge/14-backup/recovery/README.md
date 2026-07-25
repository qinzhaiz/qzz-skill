# 数据恢复

> 备份的真正价值不在于"有备份"，而在于"能恢复"。恢复不成功 = 没有备份。

## 为什么需要它

备份每天跑，但从来没人试过能不能恢复——直到真的出事了。磁盘坏了、误删了表、跑错脚本把数据写坏了——这时候才发现备份恢复有几个小时的数据缺口，或者备份文件本身就是坏的。

数据恢复是把备份"变回"数据的过程。理解各种恢复方式，才能在出问题时知道"最快能把数据恢复到什么时候"。

## 它是什么

数据恢复有几种常见方式：

| 方式 | 能恢复到什么时候 | 恢复速度 | 需要什么 |
|------|----------------|---------|---------|
| **全量恢复** | 备份那一刻 | 取决于备份大小 | 全量备份文件 |
| **全量 + 增量恢复** | 最后一次增量备份 | 全量恢复 + 逐个应用增量 | 全量 + 所有增量链 |
| **全量 + binlog** | 任意时间点（精确到秒） | 全量恢复 + 回放 binlog | 全量 + 从全量之后的完整 binlog |
| **闪回（binlog 解析）** | 回滚误操作 | 解析 + 逆向执行 | binlog |

**关键概念**：
- **RPO**（Recovery Point Objective）：最多丢多少数据。全量备份 RPO = 上次备份到现在的时间。全量+binlog RPO = 几乎为 0。
- **RTO**（Recovery Time Objective）：恢复需要多长时间。决定用哪种方式、分配多少硬件资源。

## 怎么工作

### 全量备份 + binlog 时间点恢复

```sql
时间线：
  周日 03:00        周一 15:30        周一 15:31
  [全量备份] ─────→ [误删数据] ───→ [发现误删]
                    ↑
              需要恢复到这一刻之前
              
恢复步骤：
1. 恢复周日的全量备份（数据回到周日 03:00）
2. 回放从全量到误删前一刻的所有 binlog
3. 数据恢复到周一 15:29:59
```

```bash
# 1. 恢复全量备份
mysql < full_backup.sql

# 2. 回放 binlog 到误删前一刻
mysqlbinlog --stop-datetime="2026-07-27 15:29:59" \
  mysql-bin.000012 mysql-bin.000013 | mysql

# 或指定位置
mysqlbinlog --stop-position=1234567 mysql-bin.000012 | mysql
```sql

### 闪回误操作

如果只是误删了几行或一张表，不需要恢复整个数据库——用 binlog 逆向操作：

```bash
# 用 mysqlbinlog 解析 binlog，找到误删语句
mysqlbinlog --start-datetime="2026-07-27 15:00:00" \
  --stop-datetime="2026-07-27 15:30:00" \
  mysql-bin.000012 > ops.sql

# 手动检查 ops.sql 中找到 DELETE/DROP
# 方案 1：从备份恢复这张表到另一个库，然后复制回来
# 方案 2：用工具自动生成反向 SQL
```sql

## 怎么用

```bash
# === 查看 binlog 内容 ===
mysqlbinlog --no-defaults mysql-bin.000012 | less

# === 按时间恢复 ===
mysqlbinlog --start-datetime="2026-07-20 00:00:00" \
            --stop-datetime="2026-07-27 15:29:59" \
            mysql-bin.000012 mysql-bin.000013 | mysql -u root -p

# === 按位置恢复 ===
# 先找到误操作的 binlog position
mysqlbinlog mysql-bin.000012 > binlog.txt
# 在文件中搜索 DELETE/DROP，找到 position
mysqlbinlog --start-position=123 --stop-position=456789 \
  mysql-bin.000012 | mysql

# === 恢复部分表 ===
# 从全量备份中提取单表
mysql -u root -p mydb < user_backup.sql  # 假设只备份了 user 表

# 工具化闪回（需要第三方工具）
# 1. MyFlash（美团开源）: 自动生成反向 SQL
# 2. binlog2sql: 解析 binlog 生成回滚 SQL
```sql

## 注意事项

1. **备份必须定期验证恢复**——备份脚本跑了不等于备份能用。至少每月一次在测试环境做恢复演练。
2. **binlog 必须保留足够长时间**——没有 binlog，只能恢复到全量备份那一刻。`expire_logs_days` 至少设置为全量备份周期的 2 倍。
3. **恢复时必须保证 binlog 不丢失**——如果 binlog 文件被删了或损坏了，时间点恢复就无法完成。
4. **大数据库恢复要预估时间**——100GB 全量 + 7 天 binlog，恢复可能需要数小时。做好 RTO 估算和预案。

## 和什么有关

- [mysqldump 逻辑备份](../mysqldump/) —— 全量备份的来源
- [XtraBackup 物理备份](../xtrabackup/) —— 更快的物理恢复
- [主从复制](../../13-replication/master-slave/) —— binlog 的生成和传输
