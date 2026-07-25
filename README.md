# qzz-skill

> 面向学习者的中文 AI Skills 工具箱。把技术概念和领域学习交给 Agent，获得结构化的讲解和可执行的学习路线。

**支持：Claude Code 以及其他支持 Skills 的 Agent。**

[快速开始](#快速开始) · [安装](#安装) · [能力一览](#能力一览) · [知识库](#知识库) · [项目结构](#项目结构)

## qzz-skill 解决什么问题

你不用先判断自己需要什么——把想学的东西、卡住的概念直接抛出来，它会选择合适的方式回应。

| 真实处境 | 你会得到 |
| --- | --- |
| 看了五篇文章都没搞懂一个概念 | 从设计动机出发的阶梯式讲解，找到让你"click"的那个类比 |
| 想学一个领域，不知道从哪开始 | 依赖图驱动的学习路线，先学什么后学什么一目了然 |
| 反复卡在同一个概念上 | 定位误解根源，精准修正，不重讲你已经懂的部分 |
| 学完就忘，每次都要重新查 | 讲解可以保存到本地知识库，下次直接查阅 |
| 不知道学到什么程度算"会了" | 每个阶段有可验证的自查标准 |

## 快速开始

安装完成后，直接在 Agent 中输入：

```text
什么是 MySQL 的覆盖索引？
```

qzz-explain 会判断你的需求深度，给出速览或深讲。听完后觉得还不够：

```text
我想深入理解它背后的 B+Tree 结构
```

或者你准备开始学一个领域：

```text
我想系统学 MySQL，给我一个学习路线
```

已经知道需求时，可以直接用具体 Skill：

```text
/qzz-explain 事务隔离级别是怎么实现的
/qzz-roadmap Go 语言
```

## 能力一览

| 工作目标 | 入口 | 你会得到 |
| --- | --- | --- |
| 快速了解一个概念是什么 | `qzz-explain`（速览） | 一段话 + 一个类比 + 一段代码 |
| 真正理解一个概念的来龙去脉 | `qzz-explain`（深讲） | 痛苦→设计→机制→边界→连接 |
| 修正对一个概念的误解 | `qzz-explain`（纠错） | 定位误解根源 + 精准修正 |
| 规划一个领域的学习顺序 | `qzz-roadmap` | 分阶段路线 + 依赖全景图 + 最快启动路径 |
| 查漏补缺，确认学到什么程度 | `qzz-roadmap` | 每阶段的验证标准 |

## 两个 Skill 怎样配合

```text
"我想学 MySQL"
      ↓
qzz-roadmap：画出五阶段路线，标出依赖关系
      ↓
"第二阶段里的 B+Tree 是什么？"
      ↓
qzz-explain：深讲 B+Tree，从"为什么需要它"讲到"它怎么工作的"
      ↓
"保存这次讲解"
      ↓
写入 knowledge/mysql/06-index/btree/README.md，下次直接查
```

## 安装

### Claude Code

```bash
git clone https://github.com/qinzhaiz/qzz-skill.git
cp -r qzz-skill/skills/* ~/.claude/skills/
```

仅当前项目使用的话，复制到项目的 `.claude/skills/` 即可。

### 豆包、WorkBuddy、Codex 与其他支持 Skills 的 Agent

```bash
npx -y skills add qinzhaiz/qzz-skill -g --all
```

### 更新

```bash
cd qzz-skill && git pull
cp -r skills/* ~/.claude/skills/
```

## 知识库

`knowledge/mysql/` 提供结构化的 MySQL 学习资源，17 章 71 个概念，从零基础到阅读源码。

```text
knowledge/mysql/
├── 01-basic/           基础知识（4 个概念）
├── 02-ddl/             DDL 数据定义（5）
├── 03-dml/             DML 数据操作（3）
├── 04-query/           查询（8）
├── 05-function/        函数（6）
├── 06-index/           索引（6）
├── 07-transaction/     事务（4）
├── 08-lock/            锁（4）
├── 09-execution/       执行流程（4）
├── 10-performance/     性能优化（4）
├── 11-design/          数据库设计（4）
├── 12-engine/          存储引擎（4）
├── 13-replication/     主从复制（3）
├── 14-backup/          备份恢复（3）
├── 15-security/        安全（3）
├── 16-cluster/         集群（3）
├── 17-source/          源码（3）
├── glossary.md         术语速查表
├── roadmap.md          学习路线
└── README.md            知识库入口
```

每个概念包含 7 个文件：正文（README.md）、元数据、代码示例、练习、常见错误、面试题、参考资料。

详见 `knowledge/mysql/README.md`。

## 项目结构

```text
qzz-skill/
├── skills/                  # 技能定义（SKILL.md + README.md）
├── knowledge/mysql/         # MySQL 结构化知识库（17 章 71 概念）
├── shared/templates/        # 概念模板（7 文件标准结构）
├── tools/                   # PDF 转换等辅助工具
└── docs/                    # 项目文档
```

## 作者

[@qinzhaiz](https://github.com/qinzhaiz)

## 许可证

本项目采用 [CC BY-NC 4.0](LICENSE) 许可证。

- 个人使用、学习、研究与非商业项目可以直接使用
- 公开发布衍生作品时，请注明来源
- 商业用途需要单独授权
