# 代码示例

## 示例 1：MDL 阻塞演示

**场景**：长事务不提交，导致 DDL 和后续 DML 全部阻塞。

```sql
-- 终端 A：开启事务，查询 user 表（加上 MDL 读锁，事务提交才释放）
BEGIN;
SELECT * FROM user WHERE id = 1;
-- 还没 COMMIT，MDL 读锁一直持有

-- 终端 B：尝试加字段（需要 MDL 写锁，阻塞等待 A 释放）
ALTER TABLE user ADD COLUMN phone VARCHAR(20);
-- ← 卡住，等待中

-- 终端 C：查询 user 表（需要 MDL 读锁，排在写锁后面，也卡住）
SELECT * FROM user LIMIT 1;
-- ← 也卡住！虽然读写不互斥，但队列前面的写锁把它堵了

-- 终端 A：提交事务
COMMIT;
-- B 和 C 都恢复执行
```

## 示例 2：手动表锁

**场景**：LOCK TABLES 的影响范围。

```sql
-- 终端 A
LOCK TABLES user READ;    -- 获取 user 表读锁
SELECT * FROM user;       -- ✅ 自己可以读
INSERT INTO user (name) VALUES ('test');  -- ❌ 自己也不能写

-- 终端 B
SELECT * FROM user;       -- ✅ 别人可以读
INSERT INTO user (name) VALUES ('test');  -- ❌ 别人不能写（阻塞）

-- 终端 A：释放
UNLOCK TABLES;
-- 终端 B 的 INSERT 恢复执行
```

## 示例 3：查看 MDL 锁等待

**场景**：诊断 MDL 阻塞问题。

```sql
-- MySQL 8.0 用 sys.schema_table_lock_waits 查看谁在等谁
SELECT waiting_pid,
       waiting_query,
       blocking_pid,
       blocking_query
FROM sys.schema_table_lock_waits;
```
