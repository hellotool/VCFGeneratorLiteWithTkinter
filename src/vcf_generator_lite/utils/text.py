import re

_CLEAN_QUOTES_RE = re.compile(
    r'"'  # 左引号
    r"\s*"  # 引号后可选空白
    r'([^"\n]*)'  # 不匹配引号和换行符
    r"\s*"  # 引号前可选空白
    r'"',  # 右引号
)


def clean_quotes(text: str) -> str:
    return re.sub(_CLEAN_QUOTES_RE, r"\1", text)
