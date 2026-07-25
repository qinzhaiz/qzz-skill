# 代码示例

## 示例 1：分片规则示例

```sql
-- 假设 4 个数据库，每个库 4 张表（共 16 个分片）
-- 分片算法：user_id % 4 决定数据库，user_id / 4 % 4 决定表

-- 路由计算：
-- user_id = 100：100 % 4 = 0 → ds0, 100 / 4 % 4 = 1 → orders_1
-- user_id = 101：101 % 4 = 1 → ds1, 101 / 4 % 4 = 1 → orders_1
-- user_id = 102：102 % 4 = 2 → ds2, 102 / 4 % 4 = 1 → orders_1

-- 带分片键：精确路由到一个分片
SELECT * FROM orders WHERE user_id = 100;
-- 路由到 ds0.orders_1

-- 不带分片键：广播到所有分片（慢！）
SELECT * FROM orders WHERE status = 'paid';
-- 需要查 4 库 × 4 表 = 16 个分片，再合并结果
```

## 示例 2：ShardingSphere-JDBC 配置（Java）

```yaml
# application-sharding.yml
spring:
  shardingsphere:
    datasource:
      names: ds0, ds1
      ds0:
        type: com.zaxxer.hikari.HikariDataSource
        driver-class-name: com.mysql.cj.jdbc.Driver
        jdbc-url: jdbc:mysql://10.0.0.1:3306/order_db
      ds1:
        type: com.zaxxer.hikari.HikariDataSource
        jdbc-url: jdbc:mysql://10.0.0.2:3306/order_db
    rules:
      sharding:
        tables:
          t_order:
            actual-data-nodes: ds$->{0..1}.t_order_$->{0..3}
            database-strategy:
              standard:
                sharding-column: user_id
                sharding-algorithm-name: db-inline
            table-strategy:
              standard:
                sharding-column: user_id
                sharding-algorithm-name: tbl-inline
        sharding-algorithms:
          db-inline:
            type: INLINE
            props:
              algorithm-expression: ds$->{user_id % 2}
          tbl-inline:
            type: INLINE
            props:
              algorithm-expression: t_order_$->{user_id % 4}
    props:
      sql-show: true  # 开发环境打印实际 SQL
```

## 示例 3：广播 vs 精确路由

```sql
-- ShardingSphere 执行日志示例

-- ✅ 带分片键：精确路由
-- Logic SQL: SELECT * FROM t_order WHERE user_id = 100 AND order_id = 1
-- Actual SQL: ds0 ::: SELECT * FROM t_order_0 WHERE user_id = 100 AND order_id = 1

-- ❌ 不带分片键：全路由
-- Logic SQL: SELECT * FROM t_order WHERE order_id = 1
-- Actual SQL: ds0 ::: SELECT * FROM t_order_0 WHERE order_id = 1
-- Actual SQL: ds0 ::: SELECT * FROM t_order_1 WHERE order_id = 1
-- Actual SQL: ds0 ::: SELECT * FROM t_order_2 WHERE order_id = 1
-- Actual SQL: ds0 ::: SELECT * FROM t_order_3 WHERE order_id = 1
-- Actual SQL: ds1 ::: SELECT * FROM t_order_0 WHERE order_id = 1
-- ... 8 条 SQL！
```
