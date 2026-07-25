# 代码示例

## 示例 1：完整的新手流程

```sql
-- 1. 看看有什么数据库
SHOW DATABASES;
-- 结果：information_schema, mysql, performance_schema, sys

-- 2. 创建自己的数据库
CREATE DATABASE IF NOT EXISTS mysql_practice CHARACTER SET utf8mb4;

-- 3. 进入自己的数据库
USE mysql_practice;

-- 4. 确认自己在这个库里
SELECT DATABASE();
-- 结果：mysql_practice

-- 5. 建表
CREATE TABLE IF NOT EXISTS user (
    id        INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name      VARCHAR(32)  NOT NULL DEFAULT '',
    city      VARCHAR(20)  NOT NULL DEFAULT '',
    age       TINYINT UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

-- 6. 看看表结构
DESC user;

-- 7. 插入数据
INSERT INTO user (name, city, age) VALUES
  ('张三', '北京', 22),
  ('李四', '上海', 25),
  ('王五', '深圳', 21);

-- 8. 查询数据
SELECT * FROM user;
```sql

## 示例 2：SHOW DATABASES 的输出

```sql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| mysql_practice     |  ← 你刚建的
| performance_schema |
| sys                |
+--------------------+
```sql

`mysql_practice` 出现了——这是你的第一个数据库。

## 示例 3：SELECT 加条件

```sql
-- 查所有
SELECT * FROM user;

-- 只查两列
SELECT name, city FROM user;

-- 加过滤条件
SELECT name, age FROM user WHERE city = '上海';

-- 按年龄排序
SELECT name, age FROM user ORDER BY age DESC;
```sql

| SQL | 做了什么 |
|-----|---------|
| `SELECT *` | 返回所有列 |
| `SELECT name, city` | 只返回姓名和城市 |
| `WHERE city = '上海'` | 只要城市是上海的行 |
| `ORDER BY age DESC` | 按年龄从大到小排 |
