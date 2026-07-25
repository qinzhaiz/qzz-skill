# 练习

## 基础练习

1. 用 Docker 搭建 ProxySQL + 1 主 2 从。配置读写分离规则，验证 SELECT 走从库、INSERT 走主库。

2. 查看 `stats.stats_mysql_query_digest`，理解 ProxySQL 的查询统计分析。

## 进阶练习

1. 配置两个 ProxySQL 实例 + keepalived VIP 实现代理层高可用。

2. 对比 ProxySQL 和 MySQL Router：什么场景选哪个？

## 答案

1. 核心三步：mysql_servers + mysql_query_rules + mysql_users。验证方法：执行 SELECT/INSERT 后查 stats 表确认流量分布。

2. stats_mysql_query_digest 按 SQL 模式聚合（不是单条），可发现高频慢查询模式。

3. 两个 ProxySQL + keepalived 浮动 VIP。应用连 VIP，主实例宕机 VIP 漂移到备实例。需要同步配置（SAVE TO DISK 保证持久化）。

4. ProxySQL：功能全面（SQL 级路由、查询缓存、统计），适合复杂需求。MySQL Router：轻量、配合 InnoDB Cluster 开箱即用，适合官方技术栈。
