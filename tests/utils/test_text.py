import pytest
from vcf_generator_lite.utils.text import clean_quotes


@pytest.mark.parametrize(
    ("input_text", "expected"),
    [
        ('"hello"', "hello"),
        ("hello", "hello"),
        ("", ""),
        ('""', ""),
        ('"  hello"', "hello"),
        ('"hello  "', "hello  "),
        ('"say "hello" to me"', "say helloto me"),
        ('"a" and "b"', "a and b"),
        ('"hello', '"hello'),
        ('hello"', 'hello"'),
        ('"line1\nline2"', '"line1\nline2"'),
        ('"  line1\nline2"', '"  line1\nline2"'),
        ("just some text", "just some text"),
        # 多行文本测试
        ('"hello"\n"world"', "hello\nworld"),
        ('"hello\nworld"', '"hello\nworld"'),
        ('"hello"\n"line1\nline2"', 'hello\n"line1\nline2"'),
        ('"  hello  "\n"  world  "', "hello  \nworld  "),
    ],
)
def test_clean_quotes(input_text, expected):
    assert clean_quotes(input_text) == expected
