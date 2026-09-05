import re

import pytest

from vcf_generator_lite.core.contact_parser import parse_contact
from vcf_generator_lite.models.contact import Contact, MissingNumberError
from vcf_generator_lite.models.phone_detector import PhoneRule


@pytest.fixture
def phone_rules():
    """默认的电话号码匹配规则"""
    return [
        PhoneRule(length=11, regex=re.compile(r"^(?:\+86)?1[3456789]\d{9}$")),
    ]


class TestParseContact:
    """parse_contact 基础功能测试（默认空格/制表符分隔）"""

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("张三 18445522522 工程师", Contact(phone="18445522522", name="张三", note="工程师")),
            ("张三 18445522522", Contact(phone="18445522522", name="张三")),
            ("18445522522 工程师", Contact(phone="18445522522", note="工程师")),
            ("18445522522", Contact(phone="18445522522")),
            ("张    三 丰 18445522522   工程师", Contact(phone="18445522522", name="张 三 丰", note="工程师")),
            (
                "张三 18445522522 13421322443 备用号码",
                Contact(phone="18445522522", name="张三", note="13421322443 备用号码"),
            ),
            ("张三\t18445522522 工\t程\t师", Contact(phone="18445522522", name="张三", note="工 程 师")),
        ],
    )
    def test_parse_contact_success(self, phone_rules, input_text, expected):
        """测试正常解析场景"""
        result = parse_contact(input_text, rules=phone_rules)
        assert result == expected

    @pytest.mark.parametrize(
        "input_text",
        [
            "张三 1844 工程师",  # 无效手机号
            "张三",  # 缺少手机号
        ],
    )
    def test_parse_contact_missing_valid_phone(self, phone_rules, input_text):
        """测试缺少有效手机号的情况"""
        with pytest.raises(MissingNumberError):
            parse_contact(input_text, rules=phone_rules)


class TestParseContactDelimiter:
    """parse_contact 自定义分隔符测试"""

    @pytest.mark.parametrize(
        "input_text,delimiter,expected",
        [
            # 逗号分隔的各种场景
            ("张三,18445522522,工程师", ",", Contact(phone="18445522522", name="张三", note="工程师")),
            ("张三,18445522522", ",", Contact(phone="18445522522", name="张三")),
            ("18445522522,工程师", ",", Contact(phone="18445522522", note="工程师")),
            ("18445522522", ",", Contact(phone="18445522522")),
            # 不同分隔符
            ("李四|13421322443|设计师", "|", Contact(phone="13421322443", name="李四", note="设计师")),
            ("王五\t16524812629\t产品经理", "\t", Contact(phone="16524812629", name="王五", note="产品经理")),
            ("赵六;18724657441;测试工程师", ";", Contact(phone="18724657441", name="赵六", note="测试工程师")),
            ("陈七::15928176628::运营", "::", Contact(phone="15928176628", name="陈七", note="运营")),
            # 空白处理
            ("  张三  ,  18445522522  ,  工程师  ", ",", Contact(phone="18445522522", name="张三", note="工程师")),
            (",张三,18445522522,", ",", Contact(phone="18445522522", name="张三")),
            ("张三,  ,18445522522", ",", Contact(phone="18445522522", name="张三")),
            ("张 三,18445522522,高级 工程师", ",", Contact(phone="18445522522", name="张 三", note="高级 工程师")),
            # 多手机号处理
            (
                "张三,18445522522,13297276916,备注",
                ",",
                Contact(phone="18445522522", name="张三", note="13297276916 备注"),  # TODO: 使用原始符号作为间隔
            ),
        ],
    )
    def test_parse_contact_with_delimiter_success(self, phone_rules, input_text, delimiter, expected):
        """测试自定义分隔符的正常解析场景"""
        result = parse_contact(input_text, rules=phone_rules, delimiter=delimiter)
        assert result == expected

    @pytest.mark.parametrize(
        "input_text,delimiter",
        [
            ("张三,工程师", ","),  # 缺少手机号
            (",  ,", ","),  # 所有段为空
        ],
    )
    def test_parse_contact_with_delimiter_missing_phone(self, phone_rules, input_text, delimiter):
        """测试自定义分隔符时缺少有效手机号的情况"""
        with pytest.raises(MissingNumberError):
            parse_contact(input_text, rules=phone_rules, delimiter=delimiter)
