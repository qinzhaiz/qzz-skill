# 代码示例

## 示例 1：对比表锁 vs 行锁

**场景**：并发写入时 MyISAM 和 InnoDB 的差异。

```sql
-- MyISAM 表
CREATE TABLE test_myisam (
    id INT PRIMARY KEY,
    val INT
) ENGINE=MyISAM;

INSERT INTO test_myisam VALUES (1, 100), (2, 200);

-- 终端 A
UPDATE test_myisam SET val = 101 WHERE id = 1;
-- 终端 B
UPDATE test_myisam SET val = 202 WHERE id = 2;  -- ❌ 阻塞！等 A 完成
-- MyISAM 写锁是表级锁，不管是否同一行

-- InnoDB 表
CREATE TABLE test_innodb (
    id INT PRIMARY KEY,
    val INT
) ENGINE=InnoDB;

INSERT INTO test_innodb VALUES (1, 100), (2, 200);

-- 终端 A
UPDATE test_innodb SET val = 101 WHERE id = 1;
-- 终端 B
UPDATE test_innodb SET val = 202 WHERE id = 2;  -- ✅ 不阻塞！行级锁
```sql

## 示例 2：崩溃恢复对比

```sql
-- MyISAM：崩溃后需要手动修复
CHECK TABLE test_myisam;
-- 发现损坏后：
REPAIR TABLE test_myisam;
-- 修复过程可能很慢，且可能丢数据

-- InnoDB：崩溃后自动恢复
-- 不需要手动操作，MySQL 启动时自动重放 redo log
-- 查看 redo log 状态确认恢复完成
SHOW ENGINE INNODB STATUS\G
```sql

## 示例 3：MyISAM vs InnoDB 的 COUNT(*) 性能

```sql
-- MyISAM
SELECT COUNT(*) FROM large_myisam_table;
-- 结果：瞬间返回（O(1)，读取存储的 count 值）

-- InnoDB
SELECT COUNT(*) FROM large_innodb_table;
-- 结果：需要几秒（O(N)，全索引扫描）
-- 因为 MVCC，不同事务可能看到不同行数，不能缓存一个"正确"值
```sql

**结论**：MyISAM 的 COUNT(*) 更快，但为此放弃事务、行锁、崩溃恢复，不值。

## 示例 4：查看系统中还在用 MyISAM 的表

```sql
-- 查哪些表还是 MyISAM（应该全部改成 InnoDB）
SELECT TABLE_SCHEMA, TABLE_NAME, ENGINE
FROM information_schema.TABLES
WHERE ENGINE = 'MyISAM'
  AND TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');

-- 批量生成 ALTER 语句
SELECT CONCAT('ALTER TABLE ', TABLE_SCHEMA, '.', TABLE_NAME, ' ENGINE=InnoDB;')
FROM information_schema.TABLES
WHERE ENGINE = 'MyISAM'
  AND TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');
```
