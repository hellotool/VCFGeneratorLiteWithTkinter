import importlib.metadata
import tomllib
from pathlib import Path
from typing import TypedDict

from jinja2 import Environment, FileSystemLoader, select_autoescape

PATH_LEGAL = Path("docs", "legal").resolve()
PATH_OS_NOTICE_DATA = Path("os-notices.toml").resolve()
PATH_OS_NORICES = PATH_LEGAL.joinpath("os-notices.md")

FILE_OS_NOTICES_TEMPLATE = "os-notices.template.md"

Notice = TypedDict(
    "Notice",
    {
        "name": str,
        "dependency": str,
        "repository": str,
        "license": str,
        "license-url": str,
        "copyrights": list[str],
    },
)


class NoticesConfig(TypedDict):
    template: str
    output: str
    notices: list[Notice]


def format_url(url: str, notice: Notice) -> str:
    if "dependency" not in notice:
        return url
    return url.format(version=importlib.metadata.version(notice["dependency"]))


def generate_notices(config: NoticesConfig):
    return [
        {
            **notice,
            "license_url": format_url(url=notice["license-url"], notice=notice),
        }
        for notice in config["notices"]
    ]


def generate():
    with PATH_OS_NOTICE_DATA.open("rb") as f:
        config = NoticesConfig(**tomllib.load(f))
    env = Environment(
        loader=FileSystemLoader(PATH_LEGAL),
        autoescape=select_autoescape(disabled_extensions=("md",)),
        keep_trailing_newline=True,
    )

    template = env.get_template(FILE_OS_NOTICES_TEMPLATE)
    notices = generate_notices(config)
    output = template.render(notices=notices)
    PATH_OS_NORICES.parent.mkdir(parents=True, exist_ok=True)
    PATH_OS_NORICES.write_text(output, encoding="utf-8")
