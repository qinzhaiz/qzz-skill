# 面试题

## Q1：INNER JOIN、LEFT JOIN、RIGHT JOIN 的区别？用一张图说清楚。

**考点**：面试必问，工作必用。

**回答**：INNER JOIN 取交集——两表都匹配的行。LEFT JOIN 左表全保留——右表没匹配的填 NULL。RIGHT JOIN 和 LEFT JOIN 方向相反——实际基本不用，统一用 LEFT JOIN 更清晰。

**加分**：画出 Venn 图解释，或者说出"LEFT JOIN 就是 A + A∩B"。

## Q2：JOIN 的 ON 和 WHERE 条件有什么区别？

**考点**：考察对 JOIN 执行顺序的理解。

**回答**：ON 定义"怎么连"——在连接过程中过滤。WHERE 过滤连接后的结果。区别在 OUTER JOIN（LEFT/RIGHT）上最明显：ON 条件不满足时右表行被丢弃但左表保留（NULL）；WHERE 条件直接过滤掉整行。

**加分**：能举一个 LEFT JOIN 中 ON 和 WHERE 结果不同的具体例子。
