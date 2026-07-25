# 常见错误

## 错误 1：忘了 WHERE

**症状**：`DELETE FROM orders;` 执行后整张表清空。

**原因**：和 UPDATE 一样的坑——没有 WHERE = 删所有行。

**怎么修**：DELETE 之前先用 SELECT 验证。生产环境开启事务保护——`BEGIN; DELETE ...;` 确认结果后 `COMMIT;`。

## 错误 2：DELETE 和 TRUNCATE 混用

**症状**：用 TRUNCATE 清表后发现自增 id 从 1 开始了，外键约束行为也不一样。

**原因**：TRUNCATE 是 DDL（表级操作），DELETE 是 DML（行级操作）。机制完全不同。

**怎么修**：清全部数据用 TRUNCATE（快），删部分数据用 DELETE + WHERE。不要在 DELETE 后期待 TRUNCATE 的行为，反之亦然。

## 错误 3：在生产环境删错了数据

**症状**：WHERE 条件写错了——`DELETE FROM user WHERE id = 1` 写成了 `DELETE FROM user WHERE id > 1`。

**原因**：手误。

**怎么修**：DELETE 前先 SELECT 同样的 WHERE 条件。重要操作在事务里执行。数据库做好定期备份——最后一道防线。没有备份 + 没有事务 + DELETE 错 = 数据永久损失。
