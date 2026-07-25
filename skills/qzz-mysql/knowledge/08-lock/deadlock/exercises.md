# 练习

## 基础练习

1. 两个终端模拟经典死锁：A 先锁 id=1 再锁 id=2，B 先锁 id=2 再锁 id=1。哪个事务被回滚？

2. 用 `SHOW ENGINE INNODB STATUS` 查看死锁详情。从输出中找到死锁涉及的两个事务、它们持有的锁和等待的锁。

## 进阶练习

1. 写一个简单的死锁重试逻辑（用 Python/Java/伪代码）：捕获死锁异常后重试，最多 3 次。

2. 对比：`innodb_deadlock_detect = ON` + `innodb_lock_wait_timeout = 50` vs `innodb_deadlock_detect = OFF` + `innodb_lock_wait_timeout = 3`。各自的适用场景？

## 答案

1. 被回滚的是修改行数少的那个（通常是被回滚时已经修改更少的那个）。InnoDB 选择"代价最小"的事务作为牺牲品。

2. 在输出中找到 `LATEST DETECTED DEADLOCK` 部分，可以看到 `(1) TRANSACTION` 和 `(2) TRANSACTION` 的详细信息，以及 `WE ROLL BACK TRANSACTION (2)` 表示谁被回滚了。

3. 伪代码：
```sql
for (int retry = 0; retry < 3; retry++) {
    try {
        db.execute("BEGIN");
        db.execute("UPDATE ...");
        db.execute("COMMIT");
        break;
    } catch (DeadlockException e) {
        db.execute("ROLLBACK");
        sleep(50 * (retry + 1));  // 指数退避
    }
}
```sql

4. 默认模式（检测 ON）适合大多数场景——即时发现死锁，代价是 CPU 开销。关闭检测、缩短超时适合极高并发场景——死锁检测 O(N²) 吃掉 CPU 不如让它快速超时。但需要业务层做好重试。
