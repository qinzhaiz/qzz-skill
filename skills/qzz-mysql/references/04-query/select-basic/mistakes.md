# 常见错误

## 错误 1：代码里用 SELECT *

**症状**：`SELECT * FROM user` 写在 Java/Python 代码里，后来表加了几个大字段（如 TEXT），接口突然变得很慢。

**原因**：`*` 查了所有列，包括你不需要的大字段。浪费网络传输和内存。

**怎么修**：代码里永远写清列名——`SELECT id, name, city FROM user`。加字段时不会影响已有查询。

## 错误 2：以为 DISTINCT 是整行去重

**症状**：`SELECT DISTINCT name, age FROM user`——返回了比预期多的行。

**原因**：DISTINCT 对**整个 SELECT 列表**去重，不是只对某列——(name, age) 的组合唯一。

## 错误 3：空结果当异常处理

**症状**：查询没结果就 `throw Exception("用户不存在")`。

**原因**：SQL 返回空结果 = 正常情况，应该返回空数组或 null，不应该抛异常。
