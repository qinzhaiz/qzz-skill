# 字符串函数

> 在 SQL 里直接处理字符串——拼接、截取、替换、去空格。

## 常用函数速查

| 函数 | 作用 | 示例 |
|------|------|------|
| CONCAT(a, b, ...) | 拼接 | `CONCAT('Hello', ' ', 'World')` → `Hello World` |
| CONCAT_WS(sep, a, b) | 指定分隔符拼接 | `CONCAT_WS('-', '2025', '07', '25')` → `2025-07-25` |
| SUBSTRING(s, start, len) | 截取（**从 1 开始**） | `SUBSTRING('MySQL', 1, 2)` → `My` |
| REPLACE(s, from, to) | 替换 | `REPLACE('Hello', 'l', 'x')` → `Hexxo` |
| TRIM(s) | 去首尾空格 | `TRIM('  hi  ')` → `hi` |
| UPPER(s) / LOWER(s) | 大小写转换 | `UPPER('sql')` → `SQL` |
| LENGTH(s) | **字节**长度 | `LENGTH('你好')` → `6` |
| CHAR_LENGTH(s) | **字符**长度 | `CHAR_LENGTH('你好')` → `2` |
| LEFT(s, n) / RIGHT(s, n) | 取左/右 n 个字符 | `LEFT('MySQL', 2)` → `My` |

## 实际用法

```sql
-- 拼全名
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM user;

-- 取手机号后 4 位
SELECT RIGHT(mobile, 4) FROM user;

-- 清理空白
SELECT TRIM(input) FROM form_data;

-- 按字符数找长名字
SELECT name FROM user WHERE CHAR_LENGTH(name) > 3;
```

## LENGTH vs CHAR_LENGTH

这是新手最容易混的一对。UTF-8 下，一个汉字 = 3 字节，一个英文 = 1 字节：

```sql
SELECT LENGTH('你好MySQL');      -- 11（2×3 + 5×1）
SELECT CHAR_LENGTH('你好MySQL'); -- 7（2 + 5 个字符）
```

**想按"几个字"判断长度用 CHAR_LENGTH，想算"占多少空间"用 LENGTH。**

## 注意事项

- **CONCAT 中任何参数为 NULL → 结果为 NULL。** 用 `CONCAT_WS` 或 `IFNULL(col, '')` 兜底。
- **SUBSTRING 的索引从 1 开始，不是 0。**
- **字符串函数大多数无法使用索引。** `WHERE UPPER(name) = 'ZHANGSAN'` 不能走索引。更好的做法是存入时就统一大小写。

## 和什么有关

- [04-query/where/](../../04-query/where/) — 字符串函数在 WHERE 条件里要小心索引失效
- [日期函数](../date/) — 另一类常用函数
