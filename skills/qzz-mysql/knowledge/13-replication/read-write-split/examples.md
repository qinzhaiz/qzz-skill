# 代码示例

## 示例 1：应用层手动路由

**场景**：Spring 项目用 AbstractRoutingDataSource 实现读写分离。

```java
// Java 示例——应用层读写分离
public class DynamicDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        // 从 ThreadLocal 获取当前操作类型（READ 或 WRITE）
        return DataSourceContext.getDataSourceType();
    }
}

// Service 层标记
@Transactional
public void createOrder(Order order) {
    DataSourceContext.setWrite();       // 走主库
    orderMapper.insert(order);
    DataSourceContext.clear();
}

@Transactional(readOnly = true)
public List<Order> listOrders() {
    DataSourceContext.setRead();        // 走从库
    return orderMapper.selectAll();
}
```sql

## 示例 2：关键读操作走主库

**场景**：下单后跳转到订单详情——必须读到刚写入的数据。

```sql
-- 应用层逻辑
-- 1. 插入订单
INSERT INTO orders (id, user_id, amount) VALUES (123, 1, 99.00);
-- 标记：接下来同一用户的查询走主库（例如在 Redis 设置 5 秒标记）
-- SETEX order:123:force_master 5 1

-- 2. 查询订单详情（应用检测到标记，走主库）
SELECT * FROM orders WHERE id = 123;  -- 主库

-- 3. 5 秒后标记过期，后续查询恢复正常（走从库）
SELECT * FROM orders WHERE id = 123;  -- 从库（数据已同步）
```sql

## 示例 3：监控从库延迟并自动摘除

```sql
-- 定期检查每个从库的延迟
SELECT @@server_uuid AS instance, 
       Seconds_Behind_Master 
FROM performance_schema.replication_applier_status 
       BY THREAD_ID;

-- 如果 Seconds_Behind_Master > 3（超过 3 秒延迟）
-- → 从负载均衡池中暂时移除该从库
-- → 等待 Seconds_Behind_Master < 1 后重新加入
```sql

## 示例 4：事务中的读写分离

```sql
-- ❌ 错误：事务中混用主从（可能读到不一致数据）
BEGIN;
INSERT INTO orders VALUES (...);           -- 主库
SELECT * FROM user WHERE id = 1;           -- 如果走从库，可能读到旧数据
COMMIT;

-- ✅ 正确：整个事务走主库
BEGIN;    -- 标记：这个连接走主库
INSERT INTO orders VALUES (...);           -- 主库
SELECT * FROM user WHERE id = 1;           -- 主库
COMMIT;   -- 恢复：后续查询可以走从库
```
