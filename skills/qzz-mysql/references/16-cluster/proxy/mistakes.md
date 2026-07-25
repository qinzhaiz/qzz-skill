# 常见错误

## 错误 1：只部署一个代理实例

**症状**：ProxySQL 进程 crash，所有应用连不上数据库——代理变成单点故障。

**原因**：虽然代理解决了数据库的 HA，但自己没做冗余。

**怎么修**：至少 2 个实例 + keepalived VIP 或 DNS 轮询。MySQL Router 配合 InnoDB Cluster 自带高可用。

## 错误 2：改配置忘持久化

**症状**：ProxySQL 配置改好后一切正常。机器重启后配置恢复出厂设置。

**原因**：ProxySQL 三层配置——RUNTIME、MEMORY、DISK。`LOAD ... TO RUNTIME` 只加载到内存，需 `SAVE ... TO DISK` 才持久化。

**怎么修**：每次改配置执行：`LOAD ... TO RUNTIME; SAVE ... TO DISK;`
