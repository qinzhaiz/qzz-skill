# 代码示例

## 示例 1：基本查询

```sql
-- 查所有
SELECT * FROM user;

-- 查指定列
SELECT name, city, age FROM user;

-- 去重
SELECT DISTINCT city FROM user;

-- 别名
SELECT name AS 姓名, age AS 年龄 FROM user;
```

## 示例 2：LIMIT 限制行数

```sql
-- 前 3 行
SELECT * FROM user LIMIT 3;

-- 跳过前 2 行，取 3 行（第 3-5 行）
SELECT * FROM user LIMIT 3 OFFSET 2;

-- 等价写法
SELECT * FROM user LIMIT 2, 3;
```

## 示例 3：空结果

```sql
SELECT * FROM user WHERE city = '月球';
-- Empty set (0.00 sec)
```

空结果不是报错——就是没有符合条件的行。这很正常，代码里要处理这种情况。
