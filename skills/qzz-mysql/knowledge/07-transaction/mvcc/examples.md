# 代码示例

## 示例 1：快照读 vs 当前读

```sql
-- 快照读（MVCC）：看到事务开始时的版本
SELECT * FROM user WHERE id = 1;

-- 当前读（不走 MVCC）：看到最新提交的版本，且加锁
SELECT * FROM user WHERE id = 1 FOR UPDATE;
SELECT * FROM user WHERE id = 1 LOCK IN SHARE MODE;
```sql

## 示例 2：RR 下的 MVCC 行为

```sql
-- 终端 A
BEGIN;
SELECT age FROM user WHERE id = 1;  -- age = 20

-- 终端 B：修改并提交
UPDATE user SET age = 21 WHERE id = 1;
COMMIT;

-- 终端 A（同一事务）
SELECT age FROM user WHERE id = 1;  -- age = 20（MVCC 快照）
SELECT age FROM user WHERE id = 1 FOR UPDATE;  -- age = 21（当前读！）
```sql

## 示例 3：查看长事务

```sql
SELECT trx_id, trx_started,
  TIME_TO_SEC(TIMEDIFF(NOW(), trx_started)) AS seconds_running
FROM information_schema.innodb_trx
WHERE TIME_TO_SEC(TIMEDIFF(NOW(), trx_started)) > 60;
```
