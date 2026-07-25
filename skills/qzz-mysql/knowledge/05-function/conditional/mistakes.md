# 常见错误

## 错误 1：把 IFNULL 当空串处理

**症状**：`IFNULL(phone, '未填写')` 在 phone 为空串 `''` 时返回 `''`。

**原因**：IFNULL 只处理 NULL——空串不是 NULL。

**怎么修**：同时判断 NULL 和空串：`CASE WHEN phone IS NULL OR phone = '' THEN '未填写' ELSE phone END`。

## 错误 2：CASE WHEN 条件顺序写反

**症状**：`CASE WHEN age < 60 THEN ... WHEN age < 30 THEN ...`——永远走不到第二个分支。

**原因**：CASE 按顺序判断——第一次命中就跳过后面。宽条件（<60）放前面会吞掉窄条件（<30）。

**怎么修**：严格条件放前面——`WHEN age < 30` 在 `WHEN age < 60` 之前。

## 错误 3：NULLIF 方向搞反

**症状**：以为 `NULLIF(a, b)` 是"如果 a 为空就返回 b"。

**原因**：NULLIF 是"如果 a 等于 b，返回 NULL；否则返回 a"。

**怎么修**：记清楚：NULLIF(expr1, expr2) = 相等则 NULL。
