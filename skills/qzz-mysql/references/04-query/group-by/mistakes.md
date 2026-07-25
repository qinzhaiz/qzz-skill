# 常见错误

## 错误 1：SELECT 里放了非聚合列但不在 GROUP BY 中

**症状**：`ERROR 1055: ... isn't in GROUP BY`

**原因**：MySQL 8.0 默认 ONLY_FULL_GROUP_BY 模式——非聚合列必须出现在 GROUP BY 里。

**怎么修**：把 SELECT 里的非聚合列加入 GROUP BY，或者用 `ANY_VALUE(col)` 告诉 MySQL "随便取一个值就行"。

## 错误 2：用 HAVING 替代 WHERE

**症状**：`SELECT * FROM user GROUP BY city HAVING age > 20`——把所有过滤都放 HAVING 里。

**原因**：不明白 HAVING 的执行时机。WHERE 能用索引——HAVING 在分组之后才执行，不能用索引，且要等所有分组都算完才过滤。性能差很多。

**怎么修**：能用 WHERE 过滤的先在行级滤掉，HAVING 只用来过滤聚合结果。
