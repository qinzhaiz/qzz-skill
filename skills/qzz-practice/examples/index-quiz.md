# 使用示例

## 选择题

**用户**：给我出几道 MySQL 索引的题

**qzz-practice**：好的，从知识库 `knowledge/06-index/` 中出 3 道题，难度递增。

---

**第 1 题（基础）**

以下哪个索引结构是 MySQL InnoDB 默认使用的？

A. Hash 索引
B. B+Tree 索引
C. 倒排索引
D. 位图索引

请输入你的答案（A/B/C/D）：

---

**用户**：B

**qzz-practice**：✅ 正确！InnoDB 默认使用 B+Tree 索引。

**解析**：B+Tree 所有数据存在叶子节点，叶子节点之间用双向链表连接，天然支持范围查询和排序。Hash 索引虽然等值查询快，但不支持范围查询。MySQL 的 Memory 引擎支持 Hash 索引，但 InnoDB 默认是 B+Tree。

📖 详细内容见：`knowledge/06-index/btree/README.md`

---

**第 2 题（进阶）**

有表 `orders(id, user_id, status, created_at)`，索引为 `idx_user_status(user_id, status)`。

以下哪条 SQL **不能**用到这个联合索引？

A. `SELECT * FROM orders WHERE user_id = 100`
B. `SELECT * FROM orders WHERE user_id = 100 AND status = 'paid'`
C. `SELECT * FROM orders WHERE status = 'paid'`
D. `SELECT * FROM orders WHERE user_id = 100 ORDER BY status`

请输入你的答案（A/B/C/D）：

---

**用户**：C

**qzz-practice**：✅ 正确！

**解析**：联合索引 `(user_id, status)` 遵循最左前缀原则——只有查询条件中包含最左列（user_id）时才能使用该索引。

- A：用了 `user_id`，可以用索引 ✅
- B：用了 `user_id` 和 `status`，完全匹配 ✅
- C：跳过了 `user_id` 直接查 `status`，**不能**用索引 ❌
- D：用 `user_id` 过滤 + `status` 排序，可以避免 filesort ✅

📖 详细内容见：`knowledge/06-index/composite-index/README.md`

---

**第 3 题（实战）**

```sql
SELECT * FROM users WHERE name LIKE '%张%';
```

这条查询会不会用上 `idx_name` 索引？为什么？如果不会，有什么优化方案？

请输入你的答案：

---

**用户**：不会。因为 LIKE 以 % 开头，无法利用 B+Tree 的有序性做前缀匹配。可以用全文索引，或者改成 `LIKE '张%'` 就能用索引了。

**qzz-practice**：✅ 完全正确！

**解析**：B+Tree 索引依赖字符串的字典序做二分查找。`LIKE '%张%'` 前后都有通配符，无法确定从哪个位置开始扫描，只能全表扫描。

优化方案（按优先级）：
1. 如果业务允许，改为 `LIKE '张%'`——后缀匹配，能用索引
2. 使用 MySQL 全文索引（FULLTEXT）——适合大文本搜索
3. 使用 Elasticsearch 等外部搜索引擎——适合复杂搜索场景

📖 详细内容见：`knowledge/06-index/what-is-index/README.md`

---

🎯 **本轮成绩：3/3**

全部正确！索引基础已经掌握了。建议下一步学习 `knowledge/06-index/covering-index/`（覆盖索引）或 `knowledge/10-performance/explain/`（执行计划分析）。
