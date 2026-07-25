# 常见错误

## 错误 1：忘了 WHERE

**症状**：执行 `UPDATE user SET city = '深圳';` 后整张表全变深圳。

**原因**：UPDATE 没有 WHERE = "改所有行"。

**怎么修**：先 SELECT 验证 WHERE 条件，再改成 UPDATE。个人开发用事务包起来——`BEGIN; UPDATE ...;` 确认结果无误再 `COMMIT;`，改错了 `ROLLBACK;`。

## 错误 2：WHERE 条件太宽

**症状**：`UPDATE user SET status = 0 WHERE city = '北京'` 发现改了几万行——比你预期的多多了。

**原因**：低估了 WHERE 条件匹配的行数。

**怎么修**：先 `SELECT COUNT(*) FROM user WHERE city = '北京';` 看看多少行会被影响。大表加 LIMIT 分批执行。

## 错误 3：UPDATE 不带 WHERE 然后发现没有事务保护

**症状**：改错了，想回退，发现没有开启事务。

**原因**：MySQL 默认 autocommit——每条语句自动提交，没法回滚。

**怎么修**：改重要数据用 `BEGIN;` 开启事务，确认结果后 `COMMIT;` 或 `ROLLBACK;`。后面学到 [07-transaction/](../../07-transaction/) 会详细讲。
