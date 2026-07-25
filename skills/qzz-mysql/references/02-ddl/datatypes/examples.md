# 代码示例

## 示例 1：选错类型的后果

```sql
-- 表 A：用 FLOAT 存金额
CREATE TABLE test_float (price FLOAT);
INSERT INTO test_float VALUES (0.1), (0.2);

SELECT SUM(price) FROM test_float;
-- 期望：0.3
-- 实际：0.30000000447034836
```

浮点数不能精确表示十进制小数。金额用 `DECIMAL(10,2)`。

## 示例 2：VARCHAR 长度超限

```sql
CREATE TABLE test_len (name VARCHAR(5));
INSERT INTO test_len VALUES ('MySQL');
-- ERROR 1406 (22001): Data too long for column 'name'
```

`MySQL` 五个字符刚好卡在边界——但如果内容有中文，一个汉字占一个字符位，`VARCHAR(5)` 能存 5 个汉字。

## 示例 3：DATETIME vs TIMESTAMP

```sql
CREATE TABLE test_time (
    dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO test_time VALUES ();

SELECT * FROM test_time;
-- dt 和 ts 都是当前时间，看起来一样

-- 但试试这个：
INSERT INTO test_time (dt) VALUES ('2039-01-01');
-- ✅ 正常插入

INSERT INTO test_time (ts) VALUES ('2039-01-01');
-- ❌ 报错：timestamp 只支持到 2038-01-19
```
