# 面试题

## Q1：如何从源码编译和调试 MySQL？

**考点**：动手能力——是否真的编译过。

**回答**：先安装依赖（build-essential、cmake、libssl-dev 等），用 CMake 配置 Debug 模式（`CMAKE_BUILD_TYPE=Debug` + `WITH_DEBUG=1`），make 编译，初始化数据目录后启动。调试用 GDB 附加 mysqld 进程，在感兴趣的源码位置打断点，执行 SQL 触发断点后观察变量和调用栈。

**加分点**：能说出关键 CMake 选项（`CMAKE_BUILD_TYPE`、`WITH_DEBUG`、`CMAKE_INSTALL_PREFIX`）。能解释编译时间和内存需求。

## Q2：Debug 版和 Release 版有什么区别？

**考点**：理解编译优化。

**回答**：(1) Debug 版禁用编译器优化（-O0），Release 版用 -O2 或 -O3 优化；(2) Debug 版包含大量运行时断言（assert）和调试检查代码，Release 版跳过这些；(3) Debug 版输出更多日志信息；(4) 性能差距 3-10 倍。Debug 用于学习和问题排查，Release 用于生产部署和性能测试。

**加分点**：能说出 AddressSanitizer（`WITH_ASAN`）的作用——检测内存越界、use-after-free、内存泄漏等内存错误。
