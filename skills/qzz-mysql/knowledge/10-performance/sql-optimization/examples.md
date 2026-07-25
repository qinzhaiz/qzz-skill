# 代码示例

## 示例 1：ORDER BY 优化

**场景**：查询某个用户的订单，按时间倒序。

```sql
-- 建表
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    amount DECIMAL(10,2),
    created_at DATETIME NOT NULL,
    INDEX idx_uid_time (user_id, created_at)
);

-- ❌ 慢：WHERE 用 user_id，ORDER BY 用 id
EXPLAIN SELECT * FROM orders
WHERE user_id = 100 ORDER BY id DESC LIMIT 10;
-- Extra: Using filesort（排序不能利用 idx_uid_time）

-- ✅ 快：WHERE 和 ORDER BY 用同一个索引
EXPLAIN SELECT * FROM orders
WHERE user_id = 100 ORDER BY created_at DESC LIMIT 10;
-- Extra: 没有 Using filesort！
```sql

## 示例 2：LIMIT 大偏移量优化

**场景**：翻页到第 100 万条。

```sql
-- ❌ 慢：大偏移量
SELECT * FROM orders ORDER BY id LIMIT 1000000, 20;
-- 耗时：3.5 秒（扫描 1000020 行）

-- ✅ 方案 1：基于主键的"下一页"（推荐！）
-- 前端记住当前页最大的 id，下一页从这个 id 开始
SELECT * FROM orders WHERE id > 1000000 ORDER BY id LIMIT 20;
-- 耗时：0.001 秒

-- ✅ 方案 2：覆盖索引 + JOIN（必须跳页时）
SELECT o.* FROM orders o
JOIN (SELECT id FROM orders ORDER BY id LIMIT 1000000, 20) tmp
ON o.id = tmp.id;
-- 子查询只用索引（覆盖索引不回表），找到 20 个 id 后再 JOIN 取完整行
```sql

## 示例 3：分批删除

**场景**：删除半年前的数据，不能一次锁太久。

```sql
-- ❌ 一次删除（可能锁很久）
DELETE FROM logs WHERE created_at < '2024-01-01';

-- ✅ 分批删除
DELIMITER $$
CREATE PROCEDURE batch_delete_logs()
BEGIN
    DECLARE rows_affected INT DEFAULT 1;
    WHILE rows_affected > 0 DO
        DELETE FROM logs
        WHERE created_at < '2024-01-01'
        LIMIT 1000;
        SET rows_affected = ROW_COUNT();
        DO SLEEP(0.5);  -- 每批间隔 0.5 秒，给其他事务机会
    END WHILE;
END$$
DELIMITER ;

CALL batch_delete_logs();
```sql

## 示例 4：索引失效场景速查

```sql
-- 假设有索引 idx_phone (phone)，phone 是 VARCHAR

-- ✅ 正确：字符串和字符串比
EXPLAIN SELECT * FROM user WHERE phone = '13800000000';
-- type: ref, key: idx_phone

-- ❌ 错误：隐式转换——数字和 VARCHAR 比
EXPLAIN SELECT * FROM user WHERE phone = 13800000000;
-- type: ALL（全表扫！索引失效了）

-- ❌ 错误：函数包裹索引列
EXPLAIN SELECT * FROM orders WHERE YEAR(created_at) = 2024;
-- type: ALL

-- ✅ 正确：用范围条件
EXPLAIN SELECT * FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
-- type: range, key: idx_created_at
```
