# 练习

## 基础练习

1. 在终端 A 开启事务执行 `SELECT * FROM user LIMIT 1` 但不提交，然后在终端 B 执行 `ALTER TABLE user ADD COLUMN test INT`。观察 B 是否被阻塞。

2. 使用 `SHOW PROCESSLIST` 查看被阻塞的会话状态是什么。

## 进阶练习

1. 模拟"整表不可用"场景：A 开长事务 → B 执行 ALTER → C 执行 SELECT。用 `sys.schema_table_lock_waits` 查看等待链。

2. mysqldump 备份时为什么要用 `--single-transaction` 而不是 `--lock-all-tables`？写一段说明。

## 答案

1. B 被阻塞——A 的 SELECT 在事务中持有 MDL 读锁不释放，B 的 ALTER 需要 MDL 写锁，必须等 A 提交。

2. `SHOW PROCESSLIST` 显示状态为 `Waiting for table metadata lock`。

3. C 被阻塞——因为 MDL 队列是公平的，B 的 MDL 写锁排在前面，C 的 MDL 读锁虽然和 A 不互斥但排在 B 后面，必须等 B 完成。

4. `--single-transaction` 利用 InnoDB 的 MVCC 得到一致性快照，不打全局锁也不打断读写。`--lock-all-tables` 会让整个备份期间数据库只读。
