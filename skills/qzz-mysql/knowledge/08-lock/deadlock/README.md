# 死锁

> 两个事务互相持有对方想要的锁——谁也动不了，形成死循环。

## 为什么需要理解它

死锁不是因为代码写错了——即使全部操作都正确，并发环境下死锁也可能发生。不理解死锁，线上出了死锁只会重启；理解了，才知道怎么预防和处理。

## 它是什么

**死锁**：事务 A 持有了 row-1 的锁，等 row-2 的锁；事务 B 持有了 row-2 的锁，等 row-1 的锁。两个事务形成了一个环状的等待关系——永远无法自动解开。

```sql
事务 A：持有 row-1 的锁 → 等待 row-2 → 永远等不到
事务 B：持有 row-2 的锁 → 等待 row-1 → 永远等不到
              ↑____________________________↓
                    死锁环
```sql

## 怎么工作

### InnoDB 的死锁检测

InnoDB 默认开启死锁检测（`innodb_deadlock_detect = ON`）。当一个事务请求锁被阻塞时，InnoDB 检查是否形成了等待环。如果发现了环，就**回滚其中一个事务**（通常是修改行数最少的那个），让它释放锁，打破环。

### 死锁检测的代价

死锁检测的时间复杂度是 O(N²)——每进来一个等待的事务，都要检查它和所有已在等待的事务是否形成环。当并发量很高（比如 1000 个事务同时申请锁），死锁检测可能吃掉大量 CPU。

**解决方案**：
- 控制并发线程数：`innodb_thread_concurrency`
- 关闭死锁检测：`innodb_deadlock_detect = OFF`（依赖 `innodb_lock_wait_timeout` 超时自动释放，默认 50 秒）
- 应用层排队：中间件层把并发改成串行

### 如何避免死锁

1. **按相同顺序访问资源**——A 和 B 都先锁 row-1 再锁 row-2，就不会死锁
2. **事务尽量短**——减少锁的持有时间
3. **降低隔离级别**——RC 级别没有间隙锁，减少锁的范围
4. **加索引**——让锁的行数从几百行变成几行

## 怎么用

```sql
-- 查看死锁检测状态
SHOW VARIABLES LIKE 'innodb_deadlock_detect';

-- 设置锁等待超时（默认 50 秒，可以调低）
SET innodb_lock_wait_timeout = 10;

-- 查看最近一次死锁的详细信息
SHOW ENGINE INNODB STATUS\G
-- 找到 "LATEST DETECTED DEADLOCK" 部分

-- 构造死锁示例
-- 终端 A：
BEGIN;
UPDATE user SET age = 21 WHERE id = 1;  -- 持有 id=1 的锁
-- 终端 B：
BEGIN;
UPDATE user SET age = 22 WHERE id = 2;  -- 持有 id=2 的锁
-- 终端 A：
UPDATE user SET age = 23 WHERE id = 2;  -- 等 id=2 的锁（阻塞）
-- 终端 B：
UPDATE user SET age = 24 WHERE id = 1;  -- 等 id=1 的锁 → 死锁！一方被回滚
```sql

## 注意事项

1. **死锁不可怕，可怕的是没处理**——应用层必须处理死锁重试。`ERROR 1213: Deadlock found when trying to get lock; try restarting transaction`。
2. **死锁检测有 CPU 代价**——高并发场景下死锁检测本身可能是瓶颈。必要时关闭，依赖超时。
3. **间隙锁增加了死锁风险**——RR 隔离级别有间隙锁，死锁概率比 RC 高。

## 和什么有关

- [行级锁](../row-lock/) —— 死锁的是行锁
- [事务基础](../../07-transaction/what-is-transaction/) —— 死锁回滚不影响其他已提交事务
- [乐观锁与悲观锁](../optimistic-pessimistic/) —— 乐观锁是避免死锁的策略之一
