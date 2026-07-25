# XtraBackup 物理备份

> Percona 出品的 MySQL 热备份工具——直接复制数据文件，不停机、不锁表、速度快。

## 为什么需要它

mysqldump 备份 10GB 数据库还行，备份 500GB 数据库呢？逐行读取再生成 INSERT 语句——备份要几小时，恢复可能更久。XtraBackup 直接复制 InnoDB 的数据文件（.ibd），备份速度接近磁盘读取速度，恢复速度接近磁盘写入速度。

## 它是什么

XtraBackup 是 Percona 开发的**物理热备份**工具。它直接复制 InnoDB 的数据文件，同时监控 redo log 的变化，保证备份的一致性——整个过程不锁表、不影响业务读写。

```
mysqldump：逐行读数据 → 转成 SQL → 写入文件（慢，但灵活）
XtraBackup：直接拷文件 + redo log 保证一致性（快，但要求 InnoDB）
```

## 怎么工作

### 备份过程

1. **开始备份**：记录当前的 LSN（Log Sequence Number，redo log 的位置标记）
2. **拷贝数据文件**：多线程复制 .ibd 文件到备份目录
3. **监控 redo log**：复制过程中数据库还在写入——XtraBackup 持续读取 redo log，记录备份期间产生的变更
4. **结束备份**：停止拷贝，把备份期间累积的 redo log 也写入备份
5. **Prepare（准备阶段）**：对备份应用 redo log（相当于崩溃恢复），使备份数据达到一致状态，可以安全恢复

### 增量备份

XtraBackup 支持增量备份——只备份自上次备份以来变更的页（基于 LSN）。全量 + 增量 + 增量的策略能大幅减少备份时间和空间。

```
周一：全量备份（100GB）
周二：增量备份（只备份 1GB 变更）
周三：增量备份（只备份 1.2GB 变更）
...
```

恢复时：先恢复全量 → 依次应用增量 → 最后 apply redo log。

## 怎么用

```bash
# === 安装 ===
# Ubuntu/Debian:
apt-get install percona-xtrabackup-80

# CentOS/RHEL:
yum install percona-xtrabackup-80

# === 全量备份 ===
xtrabackup --backup \
  --target-dir=/backup/full \
  --user=root --password=your_password

# === 准备备份（恢复前必须执行，相当于崩溃恢复） ===
xtrabackup --prepare --target-dir=/backup/full

# === 恢复（MySQL 必须停止） ===
# 先停 MySQL，清空数据目录
systemctl stop mysql
rm -rf /var/lib/mysql/*
# 恢复全量备份
xtrabackup --copy-back --target-dir=/backup/full
# 修改文件权限
chown -R mysql:mysql /var/lib/mysql
# 启动 MySQL
systemctl start mysql

# === 增量备份 ===
# 1. 先做全量备份
xtrabackup --backup --target-dir=/backup/full

# 2. 隔天做增量（基于全量）
xtrabackup --backup \
  --target-dir=/backup/inc1 \
  --incremental-basedir=/backup/full

# 3. 再做一次增量（基于上次增量）
xtrabackup --backup \
  --target-dir=/backup/inc2 \
  --incremental-basedir=/backup/inc1

# === 恢复增量备份链 ===
# 先 prepare 全量（不加 apply-log-only）
xtrabackup --prepare --apply-log-only --target-dir=/backup/full
# 应用第一个增量
xtrabackup --prepare --apply-log-only --target-dir=/backup/full \
  --incremental-dir=/backup/inc1
# 应用第二个增量
xtrabackup --prepare --apply-log-only --target-dir=/backup/full \
  --incremental-dir=/backup/inc2
# 最后一步 prepare（不加 apply-log-only，完成最终恢复）
xtrabackup --prepare --target-dir=/backup/full
# 然后 copy-back
```

## 注意事项

1. **恢复前必须 prepare**——刚备份完的数据文件不是一致状态（备份期间有并发写入），必须执行 `--prepare` 才能用于恢复。
2. **恢复时必须停 MySQL**——`--copy-back` 要求 MySQL 没有在运行，因为要覆盖数据文件。
3. **XtraBackup 只备份 InnoDB 表**——如果有 MyISAM 表，备份期间 MyISAM 表会短暂锁表。XtraBackup 会提示。
4. **需要足够的磁盘 IO**——备份是密集的读操作，在生产主库上运行可能会影响性能。建议在从库做。

## 和什么有关

- [mysqldump 逻辑备份](../mysqldump/) —— 两种备份方案的选择
- [数据恢复](../recovery/) —— 备份后的恢复策略
- [InnoDB 架构](../../12-engine/innodb-architecture/) —— redo log 和 LSN 的原理
