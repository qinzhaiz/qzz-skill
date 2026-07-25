# 常见错误

## 错误 1：期望 Change Buffer 优化所有写入

**症状**：数据库写入还是慢，怀疑 Change Buffer 没生效。

**原因**：Change Buffer 只对**非唯一二级索引**生效。如果表只有主键没有二级索引，或者所有二级索引都是唯一的，Change Buffer 完全不会触发。

**怎么修**：检查表的二级索引是否都是非唯一的。如果需要加速写入且业务允许，把不必要唯一的索引改为非唯一。但首先确认"慢"是否是由磁盘 IO 导致的（用 `SHOW ENGINE INNODB STATUS` 检查 IO 等待）。

## 错误 2：Change Buffer 设太大挤占 Buffer Pool

**症状**：查询突然变慢，Buffer Pool 命中率下降。

**原因**：`innodb_change_buffer_max_size` 设到了 50（占 Buffer Pool 50%）。大量内存被占用来暂存未合并的修改操作，数据缓存的可用空间减少。

**怎么修**：默认 25% 对大多数场景合适。SSD 下可以调低到 10-15%。关键要观察两项指标——Buffer Pool 命中率是否下降、Change Buffer 的使用量是否远小于上限（如果一直是 1-2% 就没必要设 25%）。
