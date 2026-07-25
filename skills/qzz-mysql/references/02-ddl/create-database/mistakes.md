# 常见错误

## 错误 1：忘了 USE 就直接操作

**症状**：`ERROR 1046 (3D000): No database selected`

**原因**：没有选库就试图建表或查数据。MySQL 不知道你的操作目标。

**怎么修**：先 `USE 库名;` 再操作。好的习惯是连上 MySQL 后第一条就是 USE。

## 错误 2：库名是敏感词或含特殊字符

**症状**：`ERROR 1064 (42000): You have an error in your SQL syntax`

**原因**：用了保留字（如 `database`、`table`、`select`）当库名，或者名字里有空格、横线。

**怎么修**：库名只用小写字母、数字、下划线。`my_project` ✅　`my-project` ❌　`select` ❌（保留字）

## 错误 3：不加 IF NOT EXISTS

**症状**：脚本跑了第二次就报错 `Can't create database 'xxx'; database exists`

**原因**：第一次建了，第二次再跑同样的 SQL 就报错。

**怎么修**：用 `CREATE DATABASE IF NOT EXISTS` 替代裸的 `CREATE DATABASE`。这在建表脚本里很重要——你希望脚本可以反复跑而不报错。
