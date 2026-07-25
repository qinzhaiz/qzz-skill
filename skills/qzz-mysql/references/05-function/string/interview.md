# 面试题

## Q1：CHAR_LENGTH 和 LENGTH 的区别？

**考点**：字符集基础。

**回答**：CHAR_LENGTH 返回字符数——'你好' = 2。LENGTH 返回字节数——'你好' 在 UTF-8 下 = 6。如果用错了，中文相关的长度判断会出 bug。

## Q2：CONCAT 和 CONCAT_WS 的区别？

**考点**：细节——处理 NULL 的行为。

**回答**：CONCAT 任何一个参数为 NULL 则结果为 NULL。CONCAT_WS 跳过 NULL 值，用第一个参数做分隔符拼接。处理可能含 NULL 的列时用 CONCAT_WS。
