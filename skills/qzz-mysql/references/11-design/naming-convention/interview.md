# 面试题

## Q1：为什么建表时推荐用 utf8mb4 而不是 utf8？

**考点**：考查是否踩过字符集的坑。

**回答**：MySQL 的 `utf8` 只支持 1-3 字节的 UTF-8 字符，最大码位是 U+FFFF。但 Unicode 中很多字符（包括 emoji、一些生僻汉字）需要 4 个字节。如果你用 utf8 建表，遇到 emoji 会报 `Incorrect string value`。`utf8mb4`（multi-byte 4）才是完整的 UTF-8 实现。所以建表时统一用 `utf8mb4` 和 `utf8mb4_unicode_ci`。

**加分点**：能说出 `utf8mb4_general_ci` 和 `utf8mb4_unicode_ci` 的区别——general 排序速度快但不够精确（如德语的 ß 排序），unicode 遵循 Unicode 标准排序规则。能提到 `utf8mb4_0900_ai_ci` 是 MySQL 8.0 的默认排序规则。

## Q2：MySQL 在 Windows 和 Linux 上行为有什么不同？

**考点**：考查跨平台经验。

**回答**：最大的坑是**表名大小写敏感**。Windows 上 MySQL 默认不区分大小写（`user` = `USER`），Linux 上区分。如果在 Windows 开发时混用了大小写（`User`、`USER`），部署到 Linux 上可能报 `Table not found`。解决方案：全小写 + 下划线命名，从源头避免问题。

**加分点**：能提到 `lower_case_table_names` 参数——设为 1 时强制全小写存储，跨平台兼容。MySQL 8.0 初始化后不可更改此参数。
