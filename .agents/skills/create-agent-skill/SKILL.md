---
name: create-agent-skill
description: Guides the correct creation of Agent Skills in this project. Use when creating new skills for this project to ensure compliance with Agent Skills standard and project conventions.
---

# 项目技能创建指南

本项目使用 [Agent Skills](https://agentskills.io) 标准，所有技能必须放在 `.agents/skills/` 目录下，而不是 `.trae/skills/` 目录。

## 项目约定

- **技能目录**：`.agents/skills/{skill-name}/`
- **技能文件**：`.agents/skills/{skill-name}/SKILL.md`
- **禁止目录**：不要使用 `.trae/skills/` 目录

## Agent Skills 标准

### 目录结构
```
skill-name/
├── SKILL.md          # （必须）
├── scripts/          # （可选）可执行脚本
├── references/       # （可选）参考文档
└── assets/           # （可选）模板和资源
```

### SKILL.md 格式

```markdown
---
name: skill-name
description: Describes what the skill does and when to use it.
---

# 技能标题

## 描述
...
```

### 字段要求

**name 字段：**
- 1-64 字符
- 仅小写字母、数字和连字符
- 不能以连字符开头或结尾
- 不能有连续的连字符
- 必须与目录名一致

**description 字段：**
- 1-1024 字符
- 必须描述技能做什么以及何时使用
- 包含相关关键词便于识别

## 创建新技能的步骤

1. 在 `.agents/skills/` 下创建目录，目录名为技能名称
2. 在目录中创建 `SKILL.md` 文件
3. 按照标准格式填写 YAML frontmatter 和内容
4. 确保 name 字段与目录名一致
5. 不要在 `.trae/skills/` 下创建任何技能

## 相关链接

- [Agent Skills 规范](https://agentskills.io/specification)
- [Trae 技能文档](https://docs.trae.cn/ide/skills)
