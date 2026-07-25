# 练习

## 基础练习

1. 在你的开发机上编译 MySQL 8.0 Debug 版本。启动后用 `mysql -u root` 连接成功。

2. 用 GDB 附加到 mysqld 进程，在 `dispatch_command` 函数打断点，执行一条 SELECT 触发断点，查看调用栈。

## 进阶练习

1. 在 GDB 中对 `row_search_mvcc` 打断点，执行一条 SELECT 并在断点处观察：当前扫描的索引名、B+Tree 游标位置、ReadView 的成员变量。

2. 编译 Release 版本，用 sysbench 做简单的性能测试，对比 Debug 版本和 Release 版本的 TPS 差异。

## 答案

1. 关键步骤：安装依赖 → cmake 配置 → make -j → make install → mysqld --initialize-insecure → mysqld 启动。常见问题：Boost 下载失败（手动下载）、内存不足（减少并行度）、端口冲突（用 --port=3307）。

2. 断点触发后 `bt` 查看调用栈：`dispatch_command` → `mysql_parse` → `mysql_execute_command` → ... → 最终到 InnoDB 的索引读取函数。

3. 在 GDB 中 `p prebuilt->index->name` 查看索引名，`p prebuilt->read_view->m_ids` 查看活跃事务，`p pcur->rec` 查看当前记录指针。

4. Release 版本比 Debug 版本快 3-10 倍。Debug 版禁用了编译器优化（-O0），增加了大量断言和检查代码。学习用 Debug，性能测试用 Release。
