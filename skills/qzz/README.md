# qzz — 学习工具箱入口

qzz 技能群的编排入口。根据用户意图自动分流到对应子技能。

## 子技能

| 技能 | 用途 |
|------|------|
| `qzz-explain` | 讲解技术概念（速览 / 深讲 / 纠错） |
| `qzz-roadmap` | 生成结构化学习路线 |
| `qzz-mysql` | MySQL 知识库（17 章） |
| `qzz-practice` | 交互式练习（编程题 / 选择题 / 填空题） |

## 使用方式

直接向 Claude 提问，qzz 自动判断意图并分流。例如：

- "解释一下 MySQL 的覆盖索引" → `qzz-explain`
- "我想系统学 Go" → `qzz-roadmap`
- "给我出几道 MySQL 索引的题" → `qzz-practice`
