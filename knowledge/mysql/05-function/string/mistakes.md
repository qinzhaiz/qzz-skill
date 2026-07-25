# 常见错误

## 错误 1：CONCAT 结果为 NULL

**症状**：拼接的列中有一个值是 NULL，整个拼接结果变成 NULL。

**原因**：CONCAT 中任何参数为 NULL → 结果为 NULL。

**怎么修**：用 CONCAT_WS（跳过 NULL），或 IFNULL(col, '') 兜底。

## 错误 2：LENGTH 和 CHAR_LENGTH 混淆

**症状**：用 LENGTH 判断字符串"多长"，中文长度总是英文的 3 倍。

**原因**：LENGTH 返回字节数（UTF-8 下 1 汉字=3 字节），CHAR_LENGTH 返回字符数。

**怎么修**：判断"几个字"用 CHAR_LENGTH。判断"占多少空间"用 LENGTH。

## 错误 3：在 WHERE 里对列用字符串函数导致索引失效

**症状**：`WHERE UPPER(name) = 'ZHANGSAN'` 不能走索引。

**原因**：对列用函数 → 索引失效。

**怎么修**：存入时就统一大小写，查询时直接比较，不走函数。
