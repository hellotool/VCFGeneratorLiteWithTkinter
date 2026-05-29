import re

_CLEAN_QUOTES_RE = re.compile(
    r'"'  # 左引号
    r"\s*"  # 引号后可选空白
    r'([^"]*)'  # 去引号后的内容
    r"\s*"  # 引号前可选空白
    r'"',  # 右引号
    re.DOTALL,
)


def clean_quotes(text: str) -> str:
    return re.sub(_CLEAN_QUOTES_RE, r"\1", text)
