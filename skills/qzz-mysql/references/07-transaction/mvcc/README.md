# MVCC

> MVCC（多版本并发控制）让读不阻塞写，写不阻塞读。InnoDB 通过维护数据的多个"历史版本"实现这一点。

## 为什么需要它

最简单的事务隔离方式是加锁——读的时候锁住行，不让别人写。但你的应用可能 99% 是读操作，加锁意味着所有读都互相排队——不可接受。

MVCC 的解决方案：**每行数据保留多个版本。** 读操作去看"过去的版本"，不需要等写锁释放。写操作去创建"新的版本"，不需要等读锁释放。读写完全解耦。

## 三个核心组件

### 1. 隐藏列

InnoDB 的每行数据有几个你 CREATE TABLE 时看不到的隐藏列：

| 隐藏列 | 大小 | 作用 |
|--------|------|------|
| `DB_TRX_ID` | 6B | 最后修改这行的事务 ID |
| `DB_ROLL_PTR` | 7B | 指向 undo log 中的旧版本（回滚指针） |
| `DB_ROW_ID` | 6B | 当没主键时，InnoDB 用它做隐式主键 |

### 2. undo log 版本链

每次修改一行数据，InnoDB 不会直接覆盖——它会先把旧版本写入 undo log，然后更新当前行。`DB_ROLL_PTR` 指向旧版本，旧版本再指向更旧的版本——形成一条**版本链**。

```
当前行(TRX_ID=100) → undo:TRX_ID=80 → undo:TRX_ID=60 → ...
```

### 3. ReadView

当事务执行 SELECT 时，InnoDB 创建一个 **ReadView**（读视图）——记录"此时此刻哪些事务正在活跃（未提交）"。ReadView 决定了这条数据对当前事务"可见还是不可见"。

**可见性判断的逻辑**：

- 这行是我自己改的 → 可见
- 这行是在我创建 ReadView 之前提交的 → 可见
- 这行是在我创建 ReadView 之后提交的 → 不可见，沿版本链往前找

## RC 和 RR 的区别

关键在于 **ReadView 的创建时机**：

| 隔离级别 | ReadView 创建时机 | 效果 |
|---------|------------------|------|
| READ COMMITTED | **每次** SELECT 都创建新的 | 每次都能看到已提交的最新数据 → 不可重复读 |
| REPEATABLE READ | 事务**第一次** SELECT 时创建，整个事务复用 | 事务内不管查多少次都看到相同数据 → 可重复读 |

这就是为什么 RR 能防"不可重复读"——同一事务内 ReadView 不变，看到的版本也不变。而 RC 每次重建 ReadView，新提交的修改"突然"就可见了。

## MVCC 的快照读 vs 当前读

```sql
-- 快照读：读 MVCC 版本（不加锁）
SELECT * FROM user WHERE id = 1;

-- 当前读：读最新数据（加锁）
SELECT * FROM user WHERE id = 1 FOR UPDATE;    -- 排他锁
SELECT * FROM user WHERE id = 1 LOCK IN SHARE MODE;  -- 共享锁
UPDATE user SET age = 20 WHERE id = 1;  -- 自动当前读 + 排他锁
```

**快照读**走 MVCC——看到的是事务开始时的版本。**当前读**不走 MVCC——读的是最新提交的数据，且加锁。

## 注意事项

- **MVCC 不适用于 SERIALIZABLE。** 串行化级别下所有读都是当前读 + 锁。
- **长事务 = undo log 膨胀。** 长事务的 ReadView 一直存在，导致旧版本无法被清理——undo log 越积越大。
- **MVCC 解释不了幻读。** RR 级别的幻读是通过 Next-Key Lock 解决的，不是 MVCC。

## 和什么有关

- [隔离级别](../isolation/) — MVCC 是实现 RC 和 RR 的核心机制
- [08-lock/row-lock/](../../08-lock/row-lock/) — Next-Key Lock 补上了 MVCC 不能防的幻读
- [09-execution/redo-undo-log/](../../09-execution/redo-undo-log/) — undo log 的详细机制
