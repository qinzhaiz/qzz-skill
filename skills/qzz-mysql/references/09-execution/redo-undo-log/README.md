# redo log 和 undo log

> 两个名字很像但功能完全相反的日志——一个保证你能提交，一个保证你能回滚。

## 为什么需要它

假设你执行了 `UPDATE account SET balance = balance - 100 WHERE id = 1`。数据库在内存中改完了数据，还没来得及写入磁盘，突然断电了。重启后这个修改还在吗？

这个问题需要两个答案：
- **持久性**：如果事务已经 COMMIT，断电后也必须恢复——这是 **redo log** 的责任
- **回滚/一致性读**：如果事务还没 COMMIT，断电后必须回滚——这是 **undo log** 的责任

| 特性 | redo log | undo log |
|------|----------|----------|
| **所属层** | InnoDB 引擎 | InnoDB 引擎 |
| **格式** | 物理日志——记录"在哪个页面哪个位置做了什么修改" | 逻辑日志——记录"逆向操作"（INSERT → DELETE） |
| **写入方式** | 循环写（固定大小，写满后覆盖旧记录） | 非循环写（通过 purge 线程清理） |
| **作用** | 崩溃恢复（crash-safe） | 事务回滚 + MVCC（构建历史版本） |
| **关键参数** | `innodb_flush_log_at_trx_commit` | `innodb_undo_tablespaces` |

## 怎么工作

### redo log 和 WAL

redo log 的核心思想是 WAL（Write-Ahead Logging）：**对数据页的修改先记日志，等系统空闲时再慢慢把内存中的数据页刷到磁盘。**

```
用户执行 UPDATE
      ↓
修改 Buffer Pool 中的缓存页（脏页）
      ↓
写 redo log（顺序写，极快）
      ↓
返回客户端 "OK"（事务提交完成）
      ↓
[后台线程异步把脏页刷到磁盘]
```

为什么这样设计？因为**顺序写日志比随机写数据页快得多**。redo log 是 append-only 的顺序写，数据页是随机写。顺序写比随机写快 1-2 个数量级。

### undo log 和 MVCC

undo log 记录每次修改的"反操作"：INSERT 记录一笔 DELETE，UPDATE 记录旧值。两个作用：

1. **事务回滚**：ROLLBACK 时逆向执行 undo log 中的操作，恢复原数据
2. **MVCC 快照读**：事务需要读到数据的历史版本时，通过 undo log 中的版本链回溯

### 脏页和 checkpoint

- **脏页**：内存中已修改但还没写入磁盘的数据页
- **checkpoint**：记录 redo log 中哪些修改已经写回了磁盘，这些位置的 redo log 可以安全覆盖

崩溃恢复的流程：启动时从 checkpoint 位置开始，重放 redo log 中的所有记录——不管事务有没有提交都先恢复（redo log 只保证数据页恢复），恢复完成后再用 undo log 回滚未提交的事务。

## 怎么用

```sql
-- 查看 redo log 配置
SHOW VARIABLES LIKE 'innodb_log_file_size';       -- 单个 redo log 文件大小
SHOW VARIABLES LIKE 'innodb_log_files_in_group';   -- redo log 文件个数

-- 最重要的参数：控制 redo log 刷盘策略
SHOW VARIABLES LIKE 'innodb_flush_log_at_trx_commit';
-- 0: 每秒刷（可能丢 1 秒数据，最不安全）
-- 1: 每次提交都刷（默认，最安全）
-- 2: 每次提交写 OS 缓存，每秒刷（折中）

-- 查看脏页比例和 InnoDB 状态
SHOW ENGINE INNODB STATUS\G

-- 查看 undo 表空间
SELECT * FROM information_schema.innodb_tablespaces
WHERE name LIKE 'undo%';
```

## 注意事项

1. **redo log 写满的后果**：redo log 是固定大小的循环写。如果写满时脏页还没刷到磁盘，InnoDB 会暂停所有写操作，全力刷脏页——表现为数据库突然卡住。
2. **`innodb_flush_log_at_trx_commit` 不能随便改成 0**：虽然写入性能提升，但崩溃可能丢失最后 1 秒的数据。金融场景用 1。
3. **undo log 不会被自动清理**：长事务持有旧的 undo log（MVCC 需要），导致 undo log 持续膨胀。
4. **binlog 和 redo log 不是一回事**：redo log 是 InnoDB 的（物理日志，循环写），binlog 是 Server 层的（逻辑日志，追加写）。两者缺一不可——崩溃恢复靠 redo log，主从复制和数据恢复靠 binlog。

## 和什么有关

- [事务 ACID](../../07-transaction/acid/) —— redo log 保证持久性，undo log 保证原子性
- [MVCC](../../07-transaction/mvcc/) —— undo log 构建版本链
- [两阶段提交](../two-phase-commit/) —— redo log 和 binlog 如何协调
