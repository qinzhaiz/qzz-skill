# 面试题

## Q1：ProxySQL 和 MySQL Router 怎么选？

**考点**：工具选型。

**回答**：ProxySQL 功能全面——SQL 级路由、查询缓存、连接池、慢查询统计、在线配置修改。适合复杂路由需求。MySQL Router 轻量、配置简单，为 InnoDB Cluster 设计（也支持传统主从）。简单读写分离或官方技术栈选 MySQL Router，需要高级功能选 ProxySQL。

**加分点**：能说出 ProxySQL 的 6032/6033 端口设计和三层配置模型。能解释为什么功能越丰富复杂度越高——ProxySQL 需要专人维护。
