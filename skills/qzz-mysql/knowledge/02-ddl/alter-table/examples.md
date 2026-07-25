# 代码示例

## 示例 1：给 user 表加一列

```sql
-- 先看现状
DESC user;

-- 加一列
ALTER TABLE user ADD COLUMN email VARCHAR(100) NOT NULL DEFAULT '' COMMENT '邮箱' AFTER name;

-- 确认
DESC user;
```sql

## 示例 2：改列类型（只能往宽了改）

```sql
CREATE TABLE test (name VARCHAR(10));
INSERT INTO test VALUES ('MySQL');

-- 把列往宽了改——OK
ALTER TABLE test MODIFY COLUMN name VARCHAR(100);
-- ✅ 成功

-- 往窄了改——危险
ALTER TABLE test MODIFY COLUMN name VARCHAR(3);
-- ❌ Data too long——'MySQL' 是 5 个字符，塞不进 VARCHAR(3)
```sql

## 示例 3：一次改多个

```sql
ALTER TABLE user
  ADD COLUMN phone VARCHAR(20) NOT NULL DEFAULT '' AFTER email,
  ADD COLUMN status TINYINT NOT NULL DEFAULT 1 AFTER phone,
  MODIFY COLUMN name VARCHAR(64) NOT NULL DEFAULT '';
```sql

三条操作一次完成。循环改三次会触发三次表结构重建——一次改完只用重建一次。

## 示例 4：改表名

```sql
-- 改表名
RENAME TABLE user TO users;

-- 改回来
RENAME TABLE users TO user;
```sql

数据完全不受影响。RENAME 几乎是 ALTER 操作里最安全、最快的——只改元数据，不碰数据。
