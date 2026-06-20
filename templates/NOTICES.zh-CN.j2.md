<!-- markdownlint-disable no-duplicate-heading -->

# 第三方声明

**简体中文** |
[English](./NOTICES.j2.md)

本文档列出了本项目使用的第三方开源组件及其许可证信息。

## 运行时依赖

随应用分发的依赖。

{% for dep in runtime -%}

### {{ dep.name }}

[{{ dep.license }}]({{ dep.url }})

{% for cr in dep.copyrights -%}

{{ cr }}

{% endfor -%}
{% endfor -%}

## 可选运行时依赖

仅在特定场景下使用的依赖。

{% for dep in optional -%}

### {{ dep.name }}

[{{ dep.license }}]({{ dep.url }})

{% for cr in dep.copyrights -%}

{{ cr }}

{% endfor -%}
{% endfor -%}

## 开发时依赖

开发、测试、文档生成、国际化工具等所需依赖。

{% for dep in dev -%}

### {{ dep.name }}

[{{ dep.license }}]({{ dep.url }})

{% for cr in dep.copyrights -%}

{{ cr }}

{% endfor -%}
{% endfor -%}

## 构建依赖

用于构建可执行文件和安装程序的依赖。

{% for dep in build -%}

### {{ dep.name }}

[{{ dep.license }}]({{ dep.url }})

{% for cr in dep.copyrights -%}

{{ cr }}

{% endfor -%}
{% endfor -%}
