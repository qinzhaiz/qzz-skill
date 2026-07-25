# 代码示例

## 示例 1：MySQL Shell 管理 InnoDB Cluster

```bash
mysqlsh --uri root@node1:3306

# 创建集群
dba.createCluster('prod_cluster')

# 查看状态
dba.getCluster().status()
```

```text
{
    "clusterName": "prod_cluster",
    "defaultReplicaSet": {
        "primary": "node1:3306",
        "status": "OK",
        "statusText": "Cluster is ONLINE and can tolerate up to ONE failure.",
        "topology": {
            "node1:3306": {"mode": "R/W", "role": "HA"},
            "node2:3306": {"mode": "R/O", "role": "HA"},
            "node3:3306": {"mode": "R/O", "role": "HA"}
        }
    }
}
```sql

## 示例 2：Group Replication 监控

```sql
-- 组成员状态
SELECT MEMBER_ID, MEMBER_HOST, MEMBER_STATE, MEMBER_ROLE
FROM performance_schema.replication_group_members;

-- 组复制统计
SELECT * FROM performance_schema.global_status
WHERE VARIABLE_NAME LIKE 'group_replication%';

-- 当前节点是主还是从（主库 read_only=OFF）
SELECT IF(@@read_only = 0, 'PRIMARY', 'SECONDARY') AS role;
```sql

## 示例 3：MHA 配置

```bash
# 检查复制状态
masterha_check_repl --conf=/etc/mha/app1.cnf

# 启动 Manager
nohup masterha_manager --conf=/etc/mha/app1.cnf &

# 手动在线切换（维护时用）
masterha_master_switch --conf=/etc/mha/app1.cnf \
  --master_state=alive --new_master_host=192.168.1.2
```
