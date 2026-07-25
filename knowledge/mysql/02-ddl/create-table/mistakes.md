# 常见错误

## 错误 1：不设主键

**症状**：建表时没写 `PRIMARY KEY (id)`，表也能建成功，但后续查询越来越慢。

**原因**：InnoDB 按主键的顺序存数据。你不设主键，MySQL 会自动生成一个隐藏的 6 字节 ROW_ID——但你查不到它，也无法用它优化查询。数据实际是乱序存储的。

**怎么修**：每张表必须显式设主键。通常用一个自增的 INT 列。后面学到 [06-index/btree/](../../06-index/btree/) 会明白为什么主键顺序对性能如此关键。

## 错误 2：表名或列名用了关键字

**症状**：`ERROR 1064 (42000): You have an error in your SQL syntax`

**原因**：用了 `order`、`group`、`select` 等 SQL 保留字当表名或列名。

**怎么修**：表名和列名避开保留字。实在避不开，用反引号包裹：`` `order` ``。但干净的命名比反引号更省事。

## 错误 3：忘了 ENGINE 和 CHARSET

**症状**：建表没写 `ENGINE=InnoDB DEFAULT CHARSET=utf8mb4`，后来发现表是 MyISAM 或者编码是 latin1。

**原因**：依赖服务器默认配置，但运维可能改过默认值。

**怎么修**：建表时显式写 `ENGINE=InnoDB DEFAULT CHARSET=utf8mb4`。多一行字，省无数麻烦。
