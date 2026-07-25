# 代码示例

## 示例 1：ProxySQL 监控

```sql
-- 查看后端 MySQL 连接池状态
SELECT hostgroup_id, hostname, port, status
FROM stats.stats_mysql_connection_pool
ORDER BY hostgroup_id;

-- 查看查询统计（类似慢查询聚合）
SELECT digest, digest_text, count_star, sum_time, avg_time
FROM stats.stats_mysql_query_digest
ORDER BY sum_time DESC LIMIT 10;
```

## 示例 2：MySQL Router 配置

```bash
# 安装并引导配置
apt-get install mysql-router
mysqlrouter --bootstrap root@node1:3306 --directory /etc/mysqlrouter

# 引导后自动生成配置，启动 Router：
systemctl start mysqlrouter

# 应用连接：
# 写：mysql -h 127.0.0.1 -P 6446 -u app -p
# 读：mysql -h 127.0.0.1 -P 6447 -u app -p
```

## 示例 3：ProxySQL 故障切换

```sql
-- ProxySQL 定期 ping 检测后端
-- 主库宕机后，自动标记 OFFLINE_HARD
-- 写请求自动路由到备用主库（需提前配置写组多个成员）

SELECT hostname, port, status FROM stats.stats_mysql_connection_pool
WHERE hostgroup_id = 10;
-- status: OFFLINE_HARD（已自动摘除故障节点）
```
