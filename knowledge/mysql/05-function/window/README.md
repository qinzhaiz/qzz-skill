# 窗口函数

> 窗口函数在不折叠行的情况下做跨行计算。GROUP BY 把多行压成一行，窗口函数保留每一行。

MySQL 8.0 才开始支持——这是 5.7 升级到 8.0 的最大动力之一。

## 为什么需要它

你要查"每个部门的员工薪资排名"。用 GROUP BY？不行——GROUP BY 把每个部门压成一行，你拿不到每个员工的排名。用子查询？能写但又长又慢。

窗口函数一句话搞定：

```sql
SELECT department, name, salary,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rk
FROM employee;
```

## 核心函数

| 函数 | 作用 |
|------|------|
| ROW_NUMBER() | 1, 2, 3, 4……（并列也递增） |
| RANK() | 1, 2, 2, 4……（并列跳号） |
| DENSE_RANK() | 1, 2, 2, 3……（并列不跳号） |
| LAG(col, n) | 往前看 n 行的值 |
| LEAD(col, n) | 往后看 n 行的值 |
| SUM/AVG/COUNT OVER | 累计求和、移动平均 |

## 关键概念

```sql
SELECT
  department, name, salary,
  SUM(salary) OVER (PARTITION BY department ORDER BY id) AS running_total
FROM employee;
```

| 关键字 | 作用 |
|--------|------|
| `PARTITION BY` | 按什么分组（类似 GROUP BY，但不合并行） |
| `ORDER BY` | 在窗口内按什么顺序计算 |
| `ROWS/RANGE` | 窗口范围：前 N 行到后 N 行 |

## 实际例子

```sql
-- 每个部门薪资排名
SELECT *, RANK() OVER (PARTITION BY dept ORDER BY salary DESC) FROM emp;

-- 每条记录的前一条和后一条
SELECT *, LAG(amount, 1) OVER (ORDER BY id), LEAD(amount, 1) OVER (ORDER BY id) FROM orders;

-- 移动平均（最近 3 天）
SELECT date, amount,
  AVG(amount) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
FROM sales;
```

## 注意事项

- **窗口函数需要 MySQL 8.0+。** 5.7 用不了——这是升级 8.0 最实际的动力。
- **不能用在 WHERE 里。** 窗口函数在 SELECT 和 ORDER BY 之后执行。要过滤的话用子查询包装。
- **ROW_NUMBER vs RANK vs DENSE_RANK——面试高频。** 搞清楚并列时的行为差异。

## 和什么有关

- [04-query/group-by/](../../04-query/group-by/) — GROUP BY 折叠行，窗口函数保留行
- [04-query/order-limit/](../../04-query/order-limit/) — ORDER BY 在窗口里的用法
