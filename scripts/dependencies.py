from dataclasses import dataclass, field


@dataclass
class Dependency:
    name: str
    license: str
    url: str
    copyrights: list[str] = field(default_factory=list)


RUNTIME: list[Dependency] = [
    Dependency(
        name="CPython",
        license="PSF License",
        url="https://docs.python.org/3/license.html",
        copyrights=[
            "Copyright © 2001 Python Software Foundation. All rights reserved.",
            "Copyright © 2000 BeOpen.com. All rights reserved.",
            "Copyright © 1995-2001 Corporation for National Research Initiatives. All rights reserved.",
            "Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.",
        ],
    ),
    Dependency(
        name="ttk-text",
        license="MIT License",
        url="https://github.com/hellotool/ttk-text/blob/v0.3.3/LICENSE",
        copyrights=["Copyright (c) 2025-2026 Jesse205"],
    ),
]

OPTIONAL: list[Dependency] = [
    Dependency(
        name="colorlog",
        license="MIT License",
        url="https://github.com/borntyping/python-colorlog/blob/main/LICENSE",
        copyrights=["Copyright (c) 2012-2021 Sam Clements <sam@borntyping.co.uk>"],
    ),
]

DEV: list[Dependency] = [
    Dependency(
        name="poethepoet",
        license="MIT License",
        url="https://github.com/nat-n/poethepoet/blob/main/LICENSE",
        copyrights=["Copyright (c) 2020 Nat Noordanus"],
    ),
    Dependency(
        name="pyright",
        license="MIT License",
        url="https://github.com/microsoft/pyright/blob/main/LICENSE",
        copyrights=["Copyright (c) Microsoft Corporation. All rights reserved."],
    ),
    Dependency(
        name="ruff",
        license="MIT License",
        url="https://github.com/astral-sh/ruff/blob/main/LICENSE",
        copyrights=["Copyright (c) 2022 Charles Marsh"],
    ),
    Dependency(
        name="pytest",
        license="MIT License",
        url="https://github.com/pytest-dev/pytest/blob/main/LICENSE",
        copyrights=["Copyright (c) 2004 Holger Krekel and others"],
    ),
]

L10N: list[Dependency] = [
    Dependency(
        name="babel",
        license="BSD 3-Clause License",
        url="https://github.com/python-babel/babel/blob/master/LICENSE",
        copyrights=["Copyright (c) 2013-2026 by the Babel Team"],
    ),
]

DOCS: list[Dependency] = [
    Dependency(
        name="jinja2",
        license="BSD 3-Clause License",
        url="https://github.com/pallets/jinja/blob/main/LICENSE.txt",
        copyrights=["Copyright 2007 Pallets"],
    ),
]

BUILD: list[Dependency] = [
    Dependency(
        name="packaging",
        license="Apache 2.0 or BSD 2-Clause Dual License",
        url="https://github.com/pypa/packaging/blob/main/LICENSE",
        copyrights=["Copyright (c) Donald Stufft and individual contributors. All rights reserved."],
    ),
    Dependency(
        name="pyinstaller",
        license="GPL 2.0+ License (with Bootloader Exception)",
        url="https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt",
        copyrights=[
            "Copyright (c) 2010-2023, PyInstaller Development Team",
            "Copyright (c) 2005-2009, Giovanni Bajo",
            "Based on previous work under copyright (c) 2002 McMillan Enterprises, Inc.",
        ],
    ),
    Dependency(
        name="requests",
        license="Apache 2.0 License",
        url="https://github.com/psf/requests/blob/main/LICENSE",
        copyrights=["Copyright 2019 Kenneth Reitz"],
    ),
]
