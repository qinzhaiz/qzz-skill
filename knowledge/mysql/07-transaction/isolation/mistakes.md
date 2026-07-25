# 常见错误

## 错误 1：以为 RR 能完全防止幻读

**症状**：RR 级别下 SELECT 快照读不会出现幻读——但如果在事务中穿插了当前读（FOR UPDATE / UPDATE），就能看到其他事务提交的新行。

**原因**：MVCC 快照读不受幻读影响——但当前读直接读最新数据。InnoDB 用 Next-Key Lock 防当前读的幻读。

**怎么修**：理解快照读和当前读的区别。需要防幻读的场景用 Next-Key Lock 或 SERIALIZABLE。

## 错误 2：用 SERIALIZABLE 解决所有并发问题

**症状**：把隔离级别设为 SERIALIZABLE，"安全第一"。

**原因**：SERIALIZABLE 相当于所有读都加共享锁——并发性能降到地板。

**怎么修**：RR 是最实用的默认值。只有特殊场景（金融结算等对一致性要求极高）才考虑 SERIALIZABLE。大部分场景 RR + Next-Key Lock 就够了。
