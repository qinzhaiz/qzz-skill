# 练习

## 基础练习

1. 写出三个 `innodb_flush_log_at_trx_commit` 取值（0/1/2）各自的含义，并说明什么场景分别适用。

2. Buffer Pool 的脏页什么时候被刷到磁盘？列出可能触发的条件。

## 进阶练习

1. 用 `SHOW ENGINE INNODB STATUS` 观察 "LOG" 部分。解读 `Log sequence number`、`Log flushed up to`、`Last checkpoint at` 三个值的含义。

2. 设计一个实验：开启大事务（UPDATE 100 万行但不提交），同时在其他会话多次更新同一行。观察 `History list length` 的变化。提交大事务后再次观察。

## 答案

1. 0=每秒刷（高性能，丢1s数据），1=每次提交都刷（最安全，默认），2=每次提交写OS缓存+每秒刷（折中，MySQL崩溃不丢，OS崩溃丢1s）。金融场景用1，日志/埋点用2，测试环境可以0。

2. 脏页刷盘触发条件：(1) redo log 写满需要覆盖时强制刷，(2) Buffer Pool 空间不足需要淘汰脏页，(3) MySQL 正常关闭，(4) checkpoint 定时触发。

3. `Log sequence number`（LSN）= 当前 redo log 已写入的总量。`Log flushed up to` = 已经刷到磁盘的位置。`Last checkpoint at` = 最后一次 checkpoint 的位置。LSN - checkpoint = 崩溃恢复需要重放的 redo log 量。

4. 长事务期间 History list length 持续增长（undo log 版本堆积），提交后 purge 线程清理，数值下降。
