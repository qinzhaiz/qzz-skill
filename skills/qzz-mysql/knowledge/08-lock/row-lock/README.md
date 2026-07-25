# 行级锁

> InnoDB 的默认锁粒度——只锁你操作的那几行，不锁整张表。

## 为什么需要它

表级锁太粗了：两个人想改同一张表的不同行，本来互不影响，表锁却让它们必须排队。行级锁解决的就是这个问题——**不同行的操作可以并行**，只有同一行的操作才需要等。

这也是 InnoDB 替代 MyISAM 成为默认引擎的核心原因之一：InnoDB 有行锁，MyISAM 只有表锁。

## 它是什么

InnoDB 的行级锁有四种类型：

| 锁类型 | 锁什么 | 作用 |
|--------|--------|------|
| **Record Lock** | 索引记录本身 | 防修改 |
| **Gap Lock** | 索引记录之间的间隙 | 防插入（解决幻读） |
| **Next-Key Lock** | Record Lock + 前面的 Gap Lock | RR 级别的默认算法，防幻读的主力 |
| **插入意向锁** | INSERT 前对间隙加的特殊锁 | 同一间隙可以同时有多个插入意向锁 |

**关键事实**：InnoDB 的行锁是通过索引实现的——锁的是索引项，不是数据行本身。如果没有索引可以用，行锁会退化为锁所有行。

## 怎么工作

### 两阶段锁协议（Two-Phase Locking）

InnoDB 遵循两阶段锁协议：
- **加锁阶段**：在需要时加锁（执行到哪加到哪）
- **释放阶段**：全部在事务 COMMIT/ROLLBACK 时统一释放

这意味着：**锁在事务提交后才释放，不是语句结束就释放**。所以要把最容易冲突的操作放在事务的最后，减少锁持有时间。

### Next-Key Lock 防幻读

```sql
表中数据：1, 5, 10（id 是主键索引）

Next-Key Lock 的范围：
(-∞, 1]  (1, 5]  (5, 10]  (10, +∞)
   ↑        ↑        ↑         ↑
 锁 ≤1   锁 (1,5]  锁 (5,10] 锁 (10,+∞)

SELECT * FROM user WHERE id = 5 FOR UPDATE;
→ 锁住 (1,5] + 阻止插入 id=2,3,4
```sql

左开右闭区间：锁住当前记录 + 它前面的空隙。其他事务既不能改 id=5，也不能在 1~5 之间插入新行。

### 为什么没有索引会出事

```sql
-- name 列没有索引
SELECT * FROM user WHERE name = 'zhangsan' FOR UPDATE;
-- 做全表扫描 → 扫描到的每一行都加锁 → 等于锁全表
```sql

InnoDB 锁的是扫描到的索引行，不是 WHERE 过滤后的结果行。没走索引 → 全表扫描 → 所有行都锁 → 退化成了表锁。

## 怎么用

```sql
-- 排他锁（X 锁）——我读的时候别人不能读也不能写
SELECT * FROM user WHERE id = 1 FOR UPDATE;

-- 共享锁（S 锁）——我读的时候别人也能读，但不能写
SELECT * FROM user WHERE id = 1 FOR SHARE;  -- MySQL 8.0
SELECT * FROM user WHERE id = 1 LOCK IN SHARE MODE;  -- 旧写法

-- INSERT / UPDATE / DELETE 自动加排他锁，不需要手动
UPDATE user SET age = 21 WHERE id = 1;  -- 自动加 X 锁
```sql

## 注意事项

1. **走索引才走行锁**。WHERE 条件没索引 → 全表扫描 → 锁所有行。这是最常见的性能事故。
2. **锁是加在索引上的**。如果表没有索引，InnoDB 用隐藏的 GEN_CLUST_INDEX，每一行都锁。
3. **间隙锁只在 RR 级别生效**。RC 级别没有间隙锁——这也是为什么 RC 不能防幻读。
4. **间隙锁之间不互斥**。两个事务可以同时持有同一个间隙的 Gap Lock（反正都是防插入）。

## 和什么有关

- [表级锁](../table-lock/) —— 粒度对比
- [聚簇索引](../../06-index/clustered-index/) —— 行锁通过索引实现
- [事务隔离](../../07-transaction/isolation/) —— RR 用 Next-Key Lock 防幻读
- [死锁](../deadlock/) —— 行锁互相等待导致
- [乐观锁与悲观锁](../optimistic-pessimistic/) —— FOR UPDATE 是悲观锁实现
