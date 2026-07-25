# 事务是什么

> 事务是把一组 SQL 打包成一个原子操作——要么全成功，要么全回滚。

## 为什么需要它

经典场景：转账。张三给李四转 100 块。

```sql
UPDATE account SET balance = balance - 100 WHERE name = '张三';
UPDATE account SET balance = balance + 100 WHERE name = '李四';
```

如果第一条执行成功，第二条失败了——张三扣了钱，李四没收到。钱凭空消失了。

事务能保证：**两条 SQL 要么都成功，要么都不做。** 第二条失败 → 第一条自动回滚 → 张三的钱还在。

## 怎么用

### 基本操作

```sql
BEGIN;                          -- 开始事务
UPDATE account SET balance = balance - 100 WHERE name = '张三';
UPDATE account SET balance = balance + 100 WHERE name = '李四';
COMMIT;                         -- 提交，确认修改

-- 或者发现有问题
ROLLBACK;                       -- 回滚，撤销所有修改
```

### 和自动提交的关系

MySQL 默认 `autocommit = ON`——每条 SQL 都是独立的事务，执行完自动提交。你用 `BEGIN` 开启显式事务后，autocommit 暂时关闭，直到 COMMIT/ROLLBACK。

```sql
-- autocommit ON 时，这两条是独立的事务
UPDATE user SET city = '北京' WHERE id = 1;  -- 自动提交
UPDATE user SET city = '上海' WHERE id = 2;  -- 自动提交

-- 显式事务——两条在一个事务里
BEGIN;
UPDATE user SET city = '北京' WHERE id = 1;
UPDATE user SET city = '上海' WHERE id = 2;
COMMIT;
```

## Savepoint：事务内的"检查点"

```sql
BEGIN;
UPDATE account SET balance = balance - 100 WHERE name = '张三';
SAVEPOINT after_debit;                              -- 设检查点
UPDATE account SET balance = balance + 100 WHERE name = '李四';
-- 发现转错人了？不回滚整个事务，只回滚到检查点
ROLLBACK TO SAVEPOINT after_debit;
-- 张三的钱扣了，但李四没收——可以重新转给正确的人
COMMIT;
```

## 注意事项

- **InnoDB 支持事务，MyISAM 不支持。** 如果一个表需要事务，确认它的引擎是 InnoDB。
- **COMMIT 之后无法 ROLLBACK。** 提交了就是永久生效。
- **事务里不要加外部 HTTP 调用。** 事务持有锁——等 HTTP 响应可能几十秒，锁一直不释放，其他事务全被阻塞。

## 和什么有关

- [ACID](../acid/) — 事务的四个核心特性
- [隔离级别](../isolation/) — 并发事务之间怎么隔离
- [MVCC](../mvcc/) — InnoDB 怎么实现事务的隔离性
