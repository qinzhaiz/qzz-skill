# 代码示例

## 示例 1：建一个标准库

```sql
CREATE DATABASE IF NOT EXISTS campus_trade
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
```

执行成功后，你会有一个叫 `campus_trade` 的空库。

## 示例 2：查看已有数据库

```sql
SHOW DATABASES;
```

输出：

```
+--------------------+
| Database           |
+--------------------+
| campus_trade       |  ← 你刚建的
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```

## 示例 3：查看建库语句

```sql
SHOW CREATE DATABASE campus_trade;
```

这条命令告诉你当初建库时用了什么参数。迁移数据库或排查字符集问题时非常有用。输出类似：

```
+--------------+--------------------------------------------------------------------+
| Database     | Create Database                                                    |
+--------------+--------------------------------------------------------------------+
| campus_trade | CREATE DATABASE `campus_trade` CHARACTER SET utf8mb4 COLLATE ...   |
+--------------+--------------------------------------------------------------------+
```

## 示例 4：完整的建→用→删流程

```sql
-- 建
CREATE DATABASE IF NOT EXISTS test_db CHARACTER SET utf8mb4;
-- 进
USE test_db;
-- 确认
SELECT DATABASE();
-- 玩完了，删
DROP DATABASE IF EXISTS test_db;
```

删完之后 `SHOW DATABASES;` 确认 test_db 不见了。
