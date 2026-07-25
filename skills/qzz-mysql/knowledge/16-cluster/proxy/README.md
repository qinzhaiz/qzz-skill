# 数据库代理

> 应用不需要知道有几台数据库、谁是主谁是从——代理帮你搞定读写分离、负载均衡、故障切换。

## 为什么需要它

没有代理时，应用代码需要知道每台数据库的 IP、区分读写、处理从库宕机后的摘除和恢复。有了代理，应用只需连代理的一个地址，代理负责路由、负载均衡、故障切换。

## 它是什么

数据库代理是应用和 MySQL 之间的中间层。主流的 MySQL 代理：

| 方案 | 特点 | 适用场景 |
|------|------|---------|
| **ProxySQL** | SQL 级路由、查询缓存、连接池、统计 | 复杂需求、需要精细控制 |
| **MySQL Router** | MySQL 官方，轻量，配合 InnoDB Cluster | InnoDB Cluster 或简单读写分离 |
| **HAProxy** | 通用 TCP 代理，不解析 SQL | 简单 TCP 层转发 |

## 怎么工作

```sql
应用 → 代理 :6033
         ├── 写请求 → 主库
         │     └── 主库宕机 → 自动切到新主库
         └── 读请求 → 从库1 / 从库2（负载均衡）
               └── 从库延迟过高 → 自动摘除
```sql

ProxySQL 端口：**6032**（管理）、**6033**（数据）。

## 怎么用

```sql
-- ProxySQL 管理端配置（6032 端口）
INSERT INTO mysql_servers VALUES
(10, '192.168.1.1', 3306),  -- 写组
(20, '192.168.1.2', 3306),  -- 读组
(20, '192.168.1.3', 3306);  -- 读组

INSERT INTO mysql_query_rules VALUES
(1, '^SELECT.*FOR UPDATE', 10, 1),  -- FOR UPDATE 走主库
(2, '^SELECT', 20, 1),              -- 普通 SELECT 走从库
(3, '.*', 10, 1);                    -- 其他走主库

-- 应用配置（立即生效 + 持久化）
LOAD MYSQL SERVERS TO RUNTIME; SAVE MYSQL SERVERS TO DISK;
LOAD MYSQL QUERY RULES TO RUNTIME; SAVE MYSQL QUERY RULES TO DISK;
```

```bash
# MySQL Router（配合 InnoDB Cluster）
mysqlrouter --bootstrap root@node1:3306 --user=mysqlrouter
# 自动生成配置：6446 读写端口, 6447 只读端口
```sql

## 注意事项

1. **代理本身是高可用瓶颈**——部署至少 2 实例 + keepalived VIP 或 DNS 轮询。
2. **改完配置记得持久化**——ProxySQL 有三层：RUNTIME → MEMORY → DISK。`SAVE ... TO DISK` 才能重启不丢。
3. **规则按 rule_id 顺序匹配**——第一条匹配的规则决定路由目标。

## 和什么有关

- [读写分离](../../13-replication/read-write-split/) —— 代理实现读写分离
- [高可用架构](../high-availability/) —— 代理 + HA 组合
- [分库分表](../sharding/) —— 更大规模需要分库分表中间件
