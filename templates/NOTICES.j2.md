<!-- markdownlint-disable no-duplicate-heading -->

# Third-Party Notices

[简体中文](./NOTICES.zh-CN.j2.md) |
**English**

This document lists the third-party open source components used by this project and their license information.

## Runtime Dependencies

Dependencies distributed with the application.

{% for dep in runtime -%}

### {{ dep.name }}

[{{ dep.license }}]({{ dep.url }})

{% for cr in dep.copyrights -%}

{{ cr }}

{% endfor -%}
{% endfor -%}

## Optional Runtime Dependencies

Dependencies used only in specific scenarios.

{% for dep in optional -%}

### {{ dep.name }}

[{{ dep.license }}]({{ dep.url }})

{% for cr in dep.copyrights -%}

{{ cr }}

{% endfor -%}
{% endfor -%}

## Development Dependencies

Dependencies required for development.

{% for dep in dev -%}

### {{ dep.name }}

[{{ dep.license }}]({{ dep.url }})

{% for cr in dep.copyrights -%}

{{ cr }}

{% endfor -%}
{% endfor -%}

## Internationalization Dependencies

{% for dep in l10n -%}

### {{ dep.name }}

[{{ dep.license }}]({{ dep.url }})

{% for cr in dep.copyrights -%}

{{ cr }}

{% endfor -%}
{% endfor -%}

## Documentation Dependencies

{% for dep in docs -%}

### {{ dep.name }}

[{{ dep.license }}]({{ dep.url }})

{% for cr in dep.copyrights -%}

{{ cr }}

{% endfor -%}
{% endfor -%}

## Build Dependencies

Dependencies for building executables and installers.

{% for dep in build -%}

### {{ dep.name }}

[{{ dep.license }}]({{ dep.url }})

{% for cr in dep.copyrights -%}

{{ cr }}

{% endfor -%}
{% endfor -%}
