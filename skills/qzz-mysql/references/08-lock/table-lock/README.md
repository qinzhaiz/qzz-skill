# 表级锁

> 锁住整张表——粒度最大、并发度最低、实现最简单的锁。

## 为什么需要它

有些操作影响的是整张表（比如改表结构、全表备份），这时候一行一行加锁太慢也不合理。表级锁就是为这种场景设计的：一把锁，整张表都不能动。

## 它是什么

MySQL 有三种表级锁：

| 类型 | 加锁方式 | 用途 |
|------|---------|------|
| **全局锁** | `FLUSH TABLES WITH READ LOCK` | 全库只读（备份） |
| **表锁** | `LOCK TABLES ... READ/WRITE` | 手动锁定表（MyISAM 常用） |
| **MDL** | 自动加锁，不需要手动操作 | 防 DML 和 DDL 互相干扰 |

全局锁让整个数据库变成只读；表锁是手动锁定指定表；**MDL（元数据锁）**是 MySQL 5.5 引入的、最常遇到的表级锁——你执行增删改查时会自动加 MDL 读锁，改表结构时会自动加 MDL 写锁。

## 怎么工作

### MDL 的互斥规则

```
MDL 读锁 ← → MDL 读锁   ✅ 不互斥（多个人同时读写一张表）
MDL 读锁 ← → MDL 写锁   ❌ 互斥（有人在读写，不能改表结构）
MDL 写锁 ← → MDL 写锁   ❌ 互斥（不能同时改表结构）
```

### 为什么 MDL 会"堵死"整张表

这是一个经典的线上故障场景：

1. 一个长事务持有 MDL 读锁（迟迟不提交）
2. DBA 执行 `ALTER TABLE`，申请 MDL 写锁 → **阻塞**（等读锁释放）
3. 后面所有的 SELECT/INSERT/UPDATE 也需要 MDL 读锁 → **也被阻塞**（排在写锁后面排队）
4. 整张表不可用

**根本原因**：MDL 的等待队列是公平队列——先到先服务。写锁虽然互斥，但比后来的读锁先到，后来的读锁必须排队。

## 怎么用

```sql
-- 全局锁（全库只读，备份时用）
FLUSH TABLES WITH READ LOCK;
UNLOCK TABLES;

-- 手动表锁（InnoDB 一般不这么用）
LOCK TABLES user READ;         -- 其他会话可读不可写
LOCK TABLES user WRITE;        -- 其他会话不可读不可写
UNLOCK TABLES;

-- MDL 是自动的——你只需要关注"有没有长事务"
SELECT trx_id, trx_started,
  TIME_TO_SEC(TIMEDIFF(NOW(), trx_started)) AS seconds_running
FROM information_schema.innodb_trx
ORDER BY trx_started;
```

## 注意事项

1. **MDL 是自动的，你感觉不到它的存在——出问题时才发现**。线上改表结构前，先 `SELECT` 查有没有长事务。
2. **手动表锁在 InnoDB 很少用**——InnoDB 有行锁，粒度更小。LOCK TABLES 主要用在 MyISAM。
3. **全局锁在 InnoDB 可以用 mysqldump 的 `--single-transaction` 替代**——不打全局锁，靠 MVCC 得到一致性快照。

## 和什么有关

- [行级锁](../row-lock/) —— InnoDB 默认用行锁而非表锁
- [事务基础](../../07-transaction/what-is-transaction/) —— 长事务是 MDL 问题的根源
- [事务隔离](../../07-transaction/isolation/) —— MVCC 让备份不用锁全库
