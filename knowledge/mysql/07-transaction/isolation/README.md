# 隔离级别

> 四个隔离级别决定了一个事务能"看到"其他事务的什么数据。隔离越高越安全，但并发越低。

## 四种隔离级别

| 级别 | 脏读 | 不可重复读 | 幻读 | InnoDB 怎么实现的 |
|------|------|-----------|------|------------------|
| **READ UNCOMMITTED** (读未提交) | ✅ 有 | ✅ 有 | ✅ 有 | 无隔离 |
| **READ COMMITTED** (读已提交) | ❌ | ✅ 有 | ✅ 有 | 每次 SELECT 新建 ReadView |
| **REPEATABLE READ** (可重复读，**默认**) | ❌ | ❌ | ⚠️ 大部分解决 | 事务第一次快照读时创建 ReadView + Next-Key Lock |
| **SERIALIZABLE** (串行化) | ❌ | ❌ | ❌ | 读加共享锁 |

## 三种并发问题

| 问题 | 含义 | 举例 |
|------|------|------|
| **脏读** | 读到别人未提交的数据 | A 改了余额未提交，B 看到了改后的值——A 回滚了，B 读的是假数据 |
| **不可重复读** | 同一事务内两次读同一行，值变了 | 第一次查 age=20，中间别人改了并提交，第二次查 age=21 |
| **幻读** | 同一事务内两次查同一范围，行数变了 | 第一次查 10 行，中间别人插入了一行并提交，第二次查 11 行 |

## 查看和设置

```sql
-- 查看当前级别
SELECT @@transaction_isolation;           -- MySQL 8.0
SELECT @@tx_isolation;                    -- MySQL 5.7

-- 设置
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## 为什么 REPEATABLE READ 是默认

RR 防止了脏读和不可重复读，InnoDB 通过 Next-Key Lock 又防止了大部分幻读。性能比 SERIALIZABLE 好得多，一致性比 READ COMMITTED 好。这是 InnoDB 团队精心选择的平衡点。

## 注意事项

- **RR 和 RC 是最常用的两个级别。** 99% 场景在它们之间选。RU 太不安全，SERIALIZABLE 太慢。
- **改隔离级别前确认业务容错。** 从 RR 改到 RC——不可重复读成为可能，你的业务代码准备好了吗？

## 和什么有关

- [ACID](../acid/) — 隔离性是 ACID 的 I
- [MVCC](../mvcc/) — RC 和 RR 都靠 MVCC 实现
- [08-lock/](../../08-lock/) — Next-Key Lock 是怎么防止幻读的
