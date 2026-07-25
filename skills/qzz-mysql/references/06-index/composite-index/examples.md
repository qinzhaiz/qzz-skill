# 代码示例

## 示例 1：最左前缀验证

```sql
CREATE INDEX idx_city_age ON user(city, age);

EXPLAIN SELECT * FROM user WHERE city = '北京';                    -- key: idx_city_age ✅
EXPLAIN SELECT * FROM user WHERE city = '北京' AND age > 20;       -- key: idx_city_age ✅
EXPLAIN SELECT * FROM user WHERE age > 20;                         -- key: NULL ❌
```

## 示例 2：中间断了

```sql
CREATE INDEX idx_a_b_c ON t(a, b, c);

EXPLAIN SELECT * FROM t WHERE a = 1 AND c = 3;
-- key: idx_a_b_c, key_len 只用到了 a 的长度 → c 没用上（中间 b 断了）
```

## 示例 3：范围条件之后失效

```sql
EXPLAIN SELECT * FROM user WHERE city = '北京' AND age > 20 AND status = 1;
-- 索引 idx_city_age：city（等值）✅ age（范围）✅ status ❌（范围之后）
```
