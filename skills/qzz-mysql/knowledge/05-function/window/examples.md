# 代码示例

## 示例 1：排名

```sql
SELECT name, department, salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,
  RANK()       OVER (ORDER BY salary DESC) AS rk,
  DENSE_RANK() OVER (ORDER BY salary DESC) AS dr
FROM employee;
```sql

## 示例 2：分组内排名

```sql
SELECT name, department, salary,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employee;
```sql

## 示例 3：前后对比

```sql
SELECT date, amount,
  LAG(amount, 1) OVER (ORDER BY date)  AS prev_amount,
  LEAD(amount, 1) OVER (ORDER BY date) AS next_amount
FROM daily_sales;
```sql

## 示例 4：累计求和

```sql
SELECT date, amount,
  SUM(amount) OVER (ORDER BY date) AS running_total
FROM daily_sales;
```
