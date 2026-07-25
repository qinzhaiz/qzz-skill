# 面试题

## Q1：utf8 和 utf8mb4 的区别？

**考点**：编码是数据库的基本功。这个问题高频出现。

**回答**：MySQL 里的 `utf8` 不是标准 UTF-8——最多只支持 3 字节，不能存 emoji 和部分生僻汉字（如 "𠮷"）。`utf8mb4` 才是完整的 UTF-8，支持 1-4 字节。建库建表永远用 `utf8mb4`。

**加分**：能说出具体场景——"电商项目里用户昵称可能含 emoji，用 utf8 存会报错 `Incorrect string value`，用 utf8mb4 就正常。MySQL 8.0 已经把默认改成 utf8mb4 了，但显式写出来是好习惯。"

## Q2：DATABASE 和 SCHEMA 有什么区别？

**考点**：考察对术语的精确理解。

**回答**：在 MySQL 里，`DATABASE` 和 `SCHEMA` 是**同义词**——`CREATE DATABASE` 和 `CREATE SCHEMA` 效果完全一样。在其他数据库（如 Oracle）里，SCHEMA 是 DATABASE 内部的一层逻辑分组，含义不同。面对 MySQL 时混用可以，面试时说清楚"MySQL 里它们等价"就好。

**加分**：能说出 MySQL 和 Oracle/PostgreSQL 在这个术语上的差异。
