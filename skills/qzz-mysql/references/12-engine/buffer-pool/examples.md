# 代码示例

## 示例 1：Buffer Pool 命中率监控

```sql
-- 查看命中率
SELECT
  ROUND((1 - pr.reads / pr.requests) * 100, 2) AS hit_rate_pct
FROM (
  SELECT
    VARIABLE_VALUE AS reads
  FROM performance_schema.global_status
  WHERE VARIABLE_NAME = 'Innodb_buffer_pool_reads'
) AS misses,
(
  SELECT
    VARIABLE_VALUE AS requests
  FROM performance_schema.global_status
  WHERE VARIABLE_NAME = 'Innodb_buffer_pool_read_requests'
) AS pr;
-- 如果 < 99%，考虑加大 innodb_buffer_pool_size
```

## 示例 2：Buffer Pool 使用率分析

```sql
-- 查看 Buffer Pool 页面使用情况
SELECT
  'total' AS page_type,
  COUNT(*) AS pages,
  COUNT(*) * 16 / 1024 AS size_mb
FROM information_schema.innodb_buffer_page
UNION ALL
SELECT
  page_type,
  COUNT(*),
  COUNT(*) * 16 / 1024
FROM information_schema.innodb_buffer_page
GROUP BY page_type
ORDER BY pages DESC;
```

**常见的 page_type**：
- `INDEX`：索引页（大部分）
- `UNDO_LOG`：undo log 页
- `INODE`：Inode 信息
- `IBUF_BITMAP`：Change Buffer 位图
- `SYSTEM`：系统页

## 示例 3：预读效率监控

```sql
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read_ahead%';
```

```text
+---------------------------------------+-------+
| Variable_name                         | Value |
+---------------------------------------+-------+
| Innodb_buffer_pool_read_ahead_rnd     | 0     |  ← 随机预读次数（几乎不用）
| Innodb_buffer_pool_read_ahead         | 12345 |  ← 线性预读次数
| Innodb_buffer_pool_read_ahead_evicted | 2345  |  ← 预读后被淘汰的页（预读浪费了）
+---------------------------------------+-------+
```

**解读**：如果 `_evicted` 接近 `_ahead` 的值，说明预读加载的大部分页都没用上就被淘汰了，白白消耗 IO。考虑关闭预读或降低预读阈值。

## 示例 4：查看 Buffer Pool 实例

```sql
-- 查看 Buffer Pool 实例数
SHOW VARIABLES LIKE 'innodb_buffer_pool_instances';

-- 查看每个实例的统计
SELECT * FROM information_schema.innodb_buffer_pool_stats;
-- pool_id: 实例 ID
-- pool_size: 实例大小（页数）
-- free_buffers: 空闲缓冲数
-- database_pages: 数据页数
-- old_database_pages: LRU 冷端的页数
-- pages_made_young: 从冷端升到热端的次数
-- pages_not_made_young: 试图升级但被阻止的次数（全表扫描的页）
```
