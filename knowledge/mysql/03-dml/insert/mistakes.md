# 常见错误

## 错误 1：VALUES 数量和列数不匹配

**症状**：`ERROR 1136 (21S01): Column count doesn't match value count`

**原因**：列名列表写了 3 列，VALUES 给了 4 个值（或反之）。

**怎么修**：逐个数——列名几个，VALUES 几个，数量和顺序都得对齐。

## 错误 2：不写列名

**症状**：代码过几天表加了一列，原来跑得好好的 INSERT 突然报错。

**原因**：`INSERT INTO t VALUES(...)` 依赖列的物理顺序。加一列、改一列可能导致 VALUES 顺序对不上。

**怎么修**：永远写列名列表——`INSERT INTO t (col1, col2) VALUES(...)`。多打几个字，省无数 bug。

## 错误 3：字符串没加引号

**症状**：`ERROR 1054 (42S22): Unknown column '张三' in 'field list'`

**原因**：`INSERT INTO user (name) VALUES (张三)`——MySQL 认为 `张三` 是列名。

**怎么修**：字符串必须用单引号包裹：`VALUES ('张三')`。不加引号 = 列名 = 报错。
