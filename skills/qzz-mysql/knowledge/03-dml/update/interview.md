# 面试题

## Q1：UPDATE 为什么一定要加 WHERE？

**考点**：最基础的安全意识——很多生产事故就是这么来的。

**回答**：不加 WHERE 的 UPDATE 会修改**所有行**。生产库上执行一条 `UPDATE orders SET status = 'cancelled'` 不带 WHERE，整个订单表全变成取消状态——神仙难救。正确流程是：先用 SELECT 确认 WHERE 条件匹配的行是你要改的，再套上事务保护，最后执行 UPDATE。

**加分**：提到"安全模式"——MySQL Workbench 默认开启 safe update mode，`UPDATE ... WHERE` 必须包含主键条件，否则拒绝执行。直接在命令行跑没有这个保护，所以更需要注意。

## Q2：大批量 UPDATE 怎么做更安全？

**考点**：生产环境经验。

**回答**：不要一次 UPDATE 几百万行——会长时间持有行锁，阻塞其他写入。正确做法：用 LIMIT 分批执行，每批 1000-10000 行，循环跑直到 affected rows 为 0。或者用 pt-online-schema-change 这类工具在线变更。

**加分**：提到在事务里分批执行——"每 1000 行一个事务，commit 后再处理下一批。这样即使中途出问题，也只影响当前的一小批。"
