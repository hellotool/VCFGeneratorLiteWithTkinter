import re

import pytest

from vcf_generator_lite.core.contact_parser import parse_contact
from vcf_generator_lite.models.contact import Contact, MissingNumberError
from vcf_generator_lite.models.phone_format import PhoneRule

TEST_PHONE_RULES = [
    PhoneRule(length=11, regex=re.compile(r"^(?:\+86)?1[3456789]\d{9}$")),
]


FAKE_PHONES = [
    "18445522522",
    "13421322443",
    "16524812629",
    "18724657441",
    "15928176628",
    "15801124810",
    "17111469035",
    "13428242703",
    "13297276916",
    "15331568900",
]


class TestParseContact:
    # 正常情况测试
    def test_with_note(self):
        """测试包含备注的联系人信息"""
        result = parse_contact("张三 18445522522 工程师", rules=TEST_PHONE_RULES)
        assert result == Contact(phone="18445522522", name="张三", note="工程师")

    def test_without_note(self):
        """测试无备注的联系人信息"""
        result = parse_contact("张三 18445522522", rules=TEST_PHONE_RULES)
        assert result == Contact(phone="18445522522", name="张三")

    def test_without_name(self):
        """测试姓名为空的情况"""
        result = parse_contact("18445522522 工程师", rules=TEST_PHONE_RULES)
        assert result == Contact(phone="18445522522", note="工程师")

    def test_without_name_and_note(self):
        """测试姓名和备注都为空的情况"""
        result = parse_contact("18445522522", rules=TEST_PHONE_RULES)
        assert result == Contact(phone="18445522522")

    def test_name_with_spaces(self):
        """测试姓名包含空格的情况"""
        result = parse_contact("张    三 丰 18445522522   工程师", rules=TEST_PHONE_RULES)
        assert result == Contact(phone="18445522522", name="张 三 丰", note="工程师")

    def test_multiple_phones(self):
        """测试包含多个手机号的情况（应使用第一个有效手机号）"""
        result = parse_contact("张三 18445522522 13421322443 备用号码", rules=TEST_PHONE_RULES)
        assert result == Contact(phone="18445522522", name="张三", note="13421322443 备用号码")

    def test_tabs_to_spaces(self):
        """测试使用制表符转空格"""
        result = parse_contact("张三\t18445522522 工\t程\t师", rules=TEST_PHONE_RULES)
        assert result == Contact(phone="18445522522", name="张三", note="工 程 师")

    # 异常情况测试
    def test_missing_valid_phone(self):
        """测试缺少有效手机号的情况"""
        with pytest.raises(MissingNumberError):
            parse_contact("张三 1844 工程师", rules=TEST_PHONE_RULES)

    def test_missing_phone(self):
        """测试缺失电话号码的情况"""
        with pytest.raises(MissingNumberError):
            parse_contact("张三", rules=TEST_PHONE_RULES)


class TestParseContactDelimiter:
    """parse_contact delimiter 参数测试"""

    def test_delimiter_comma_full(self):
        """逗号分隔：姓名、手机号、备注齐全"""
        result = parse_contact("张三,18445522522,工程师", rules=TEST_PHONE_RULES, delimiter=",")
        assert result == Contact(phone="18445522522", name="张三", note="工程师")

    def test_delimiter_comma_no_note(self):
        """逗号分隔：仅姓名和手机号，无备注"""
        result = parse_contact("张三,18445522522", rules=TEST_PHONE_RULES, delimiter=",")
        assert result == Contact(phone="18445522522", name="张三")

    def test_delimiter_comma_no_name(self):
        """逗号分隔：仅手机号和备注，无姓名"""
        result = parse_contact("18445522522,工程师", rules=TEST_PHONE_RULES, delimiter=",")
        assert result == Contact(phone="18445522522", note="工程师")

    def test_delimiter_comma_phone_only(self):
        """逗号分隔：仅手机号"""
        result = parse_contact("18445522522", rules=TEST_PHONE_RULES, delimiter=",")
        assert result == Contact(phone="18445522522")

    def test_delimiter_pipe(self):
        """竖线分隔符"""
        result = parse_contact("李四|13421322443|设计师", rules=TEST_PHONE_RULES, delimiter="|")
        assert result == Contact(phone="13421322443", name="李四", note="设计师")

    def test_delimiter_tab(self):
        """制表符分隔（TSV 格式）"""
        result = parse_contact("王五\t16524812629\t产品经理", rules=TEST_PHONE_RULES, delimiter="\t")
        assert result == Contact(phone="16524812629", name="王五", note="产品经理")

    def test_delimiter_semicolon(self):
        """分号分隔符"""
        result = parse_contact("赵六;18724657441;测试工程师", rules=TEST_PHONE_RULES, delimiter=";")
        assert result == Contact(phone="18724657441", name="赵六", note="测试工程师")

    def test_delimiter_multi_char(self):
        """多字符分隔符"""
        result = parse_contact("陈七::15928176628::运营", rules=TEST_PHONE_RULES, delimiter="::")
        assert result == Contact(phone="15928176628", name="陈七", note="运营")

    # ── 空白处理行为（与 None 的对比） ──────────────────────────

    def test_delimiter_strips_surrounding_whitespace(self):
        """各字段两端空白应被 strip"""
        result = parse_contact("  张三  ,  18445522522  ,  工程师  ", rules=TEST_PHONE_RULES, delimiter=",")
        assert result == Contact(phone="18445522522", name="张三", note="工程师")

    def test_delimiter_empty_segments_ignored(self):
        """分隔后产生的空白段应被过滤"""
        result = parse_contact(",张三,18445522522,", rules=TEST_PHONE_RULES, delimiter=",")
        assert result == Contact(phone="18445522522", name="张三")

    def test_delimiter_whitespace_only_segments_ignored(self):
        """strip 后为空的段也应被过滤"""
        result = parse_contact("张三,  ,18445522522", rules=TEST_PHONE_RULES, delimiter=",")
        assert result == Contact(phone="18445522522", name="张三")

    def test_delimiter_preserves_spaces_within_field(self):
        """字段内部的空格应原样保留（不折叠）"""
        result = parse_contact("张 三,18445522522,高级 工程师", rules=TEST_PHONE_RULES, delimiter=",")
        assert result == Contact(phone="18445522522", name="张 三", note="高级 工程师")

    def test_delimiter_multiple_phones_uses_first(self):
        """存在多个手机号时，使用首个有效号码"""
        result = parse_contact("张三,18445522522,13297276916,备注", rules=TEST_PHONE_RULES, delimiter=",")
        assert result == Contact(phone="18445522522", name="张三", note="13297276916 备注")

    def test_delimiter_missing_phone_raises(self):
        """无有效手机号时抛出 MissingNumberError"""
        with pytest.raises(MissingNumberError):
            parse_contact("张三,工程师", rules=TEST_PHONE_RULES, delimiter=",")

    def test_delimiter_all_empty_after_strip_raises(self):
        """所有段 strip 后均为空时抛出 MissingNumberError"""
        with pytest.raises(MissingNumberError):
            parse_contact(",  ,", rules=TEST_PHONE_RULES, delimiter=",")
