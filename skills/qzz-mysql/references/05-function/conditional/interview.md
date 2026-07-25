# 面试题

## Q1：IFNULL 和 COALESCE 的区别？

**考点**：NULL 处理是基本功。

**回答**：IFNULL 只接受两个参数——第一个是 NULL 就用第二个替代。COALESCE 接受多个参数——从左到右返回第一个非 NULL 的值。`IFNULL(a, b)` = `COALESCE(a, b)`，但 `COALESCE(a, b, c, d)` 无法用 IFNULL 一行写完。

## Q2：CASE WHEN 和 IF 函数的选择？

**考点**：代码可读性。

**回答**：简单的 T/F 判断用 IF——`IF(age >= 18, '成年', '未成年')`。多分支判断用 CASE WHEN——更清晰。IF 嵌套超过一层就换 CASE。
