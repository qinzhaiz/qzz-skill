# 面试题

first-query 属于入门操作，不直接出现在面试中。但以下基础问题可能被顺带问到。

## Q1：utf8 和 utf8mb4 有什么区别？

**考点**：看你对字符编码有没有基本认识。这是个高频小问题。

**回答**：MySQL 里的 `utf8` 不是真正的 UTF-8——它最多存 3 字节字符，不能存 emoji 和部分生僻汉字。`utf8mb4` 才是完整的 UTF-8（最多 4 字节）。建库建表永远用 `utf8mb4`。

**加分**：能举出具体例子——"你在 MySQL 里用 utf8 存 '你好' 没问题，但存 '😀' 会报错 Incorrect string value。用 utf8mb4 就正常。"

## Q2：连上 MySQL 先做什么？

**考点**：看你的操作习惯是不是规范。

**回答**：先 `SELECT VERSION()` 确认版本——不同版本语法可能有差异。然后 `SHOW DATABASES` 看看有哪些库。再 `USE 自己的库` 进入工作环境。最后 `SELECT DATABASE()` 确认选对库了。

**加分**：提到会检查字符集——`SHOW CREATE DATABASE 库名;` 确认是 utf8mb4。工作中因为默认字符集不是 utf8mb4 导致中文乱码的坑很常见。
