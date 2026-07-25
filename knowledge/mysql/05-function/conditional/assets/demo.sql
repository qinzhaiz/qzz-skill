-- demo.sql：CASE WHEN / IF / IFNULL / COALESCE / NULLIF
-- 需要先有 user 表（参考 01-basic/first-query/assets/demo.sql）

-- CASE WHEN：年龄段分组
SELECT name, age,
  CASE
    WHEN age < 18 THEN '未成年'
    WHEN age < 30 THEN '青年'
    WHEN age < 60 THEN '中年'
    ELSE '老年'
  END AS age_group
FROM user;

-- IF 函数
SELECT name, IF(age >= 22, '22岁以上', '22岁以下') FROM user;

-- IFNULL 兜底
SELECT name, IFNULL(mobile, '未填写') FROM user;

-- 行转列：按城市统计各年龄段人数
SELECT city,
  SUM(CASE WHEN age < 25 THEN 1 ELSE 0 END) AS young,
  SUM(CASE WHEN age >= 25 THEN 1 ELSE 0 END) AS senior
FROM user GROUP BY city;
