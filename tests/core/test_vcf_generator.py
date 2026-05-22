import pytest

from vcf_generator_lite.core.vcf_generator import serialize_to_vcard, utf8_to_qp
from vcf_generator_lite.models.contact import Contact


class TestSerializeToVCard:
    """测试联系人序列化为 vCard 格式"""

    def test_basic_contact_serialization(self):
        """测试基本联系人序列化"""
        contact = Contact(phone="13800138000", name="张三")
        result = serialize_to_vcard(contact)

        assert "BEGIN:VCARD" in result
        assert "END:VCARD" in result
        assert "TEL;CELL:13800138000" in result
        assert "FN;" in result  # vCard 2.1 中 FN 字段包含分号和参数

    def test_contact_with_note(self):
        """测试包含备注的联系人序列化"""
        contact = Contact(phone="13800138000", name="张三", note="工程师")
        result = serialize_to_vcard(contact)

        assert "NOTE;" in result  # vCard 2.1 中 NOTE 字段包含分号和参数

    def test_contact_without_name(self):
        """测试没有姓名的联系人序列化"""
        contact = Contact(phone="13800138000", name=None)
        result = serialize_to_vcard(contact)

        assert "BEGIN:VCARD" in result
        assert "END:VCARD" in result
        assert "TEL;CELL:13800138000" in result
        assert "FN;" not in result  # 不应该包含 FN 字段

    def test_contact_without_note(self):
        """测试没有备注的联系人序列化"""
        contact = Contact(phone="13800138000", name="张三", note=None)
        result = serialize_to_vcard(contact)

        assert "BEGIN:VCARD" in result
        assert "END:VCARD" in result
        assert "TEL;CELL:13800138000" in result
        assert "FN;" in result
        assert "NOTE;" not in result  # 不应该包含 NOTE 字段

    def test_contact_without_name_and_note(self):
        """测试既没有姓名也没有备注的联系人序列化"""
        contact = Contact(phone="13800138000", name=None, note=None)
        result = serialize_to_vcard(contact)

        lines = result.split("\n")
        assert len(lines) == 4  # BEGIN, VERSION, TEL, END
        assert lines[0] == "BEGIN:VCARD"
        assert lines[1] == "VERSION:2.1"
        assert lines[2] == "TEL;CELL:13800138000"
        assert lines[3] == "END:VCARD"

    def test_contact_with_special_characters_in_name(self):
        """测试姓名包含特殊字符的联系人序列化"""
        contact = Contact(phone="13800138000", name="张三 & 李四")
        result = serialize_to_vcard(contact)

        assert "FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:" in result
        assert "TEL;CELL:13800138000" in result

    def test_contact_with_special_characters_in_note(self):
        """测试备注包含特殊字符的联系人序列化"""
        contact = Contact(phone="13800138000", name="张三", note="工程师 & 开发者")
        result = serialize_to_vcard(contact)

        assert "NOTE;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:" in result
        assert "TEL;CELL:13800138000" in result


class TestUtf8ToQp:
    """测试 UTF-8 到 Quoted-Printable 编码的转换"""

    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("张三", "=E5=BC=A0=E4=B8=89"),
            ("John Doe", "John Doe"),
            ("John 张三", "John =E5=BC=A0=E4=B8=89"),
            ("", ""),
            ("Hello & World!", "Hello & World!"),
        ],
    )
    def test_utf8_to_qp(self, input_str, expected):
        assert utf8_to_qp(input_str) == expected
