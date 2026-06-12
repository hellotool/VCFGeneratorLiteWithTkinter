import pytest

from vcf_generator_lite.core.vcf_generator import serialize_to_vcard, utf8_to_qp
from vcf_generator_lite.models.contact import Contact


class TestSerializeToVCard:
    """测试联系人序列化为 vCard 格式"""

    def test_contact_withonly_phone(self):
        """测试仅包含手机号码的联系人序列化"""
        contact = Contact(phone="13800138000")
        result = serialize_to_vcard(contact).splitlines()

        assert "BEGIN:VCARD" in result
        assert "END:VCARD" in result
        assert "TEL;CELL:13800138000" in result
        assert not any(line.startswith("FN;") for line in result)
        assert not any(line.startswith("NOTE;") for line in result)

    def test_contact_with_name(self):
        """测试包含姓名的联系人序列化"""
        contact = Contact(phone="13800138000", name="张三")
        result = serialize_to_vcard(contact).splitlines()

        assert "BEGIN:VCARD" in result
        assert "END:VCARD" in result
        assert "TEL;CELL:13800138000" in result
        assert any(line.startswith("FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:") for line in result)
        assert not any(line.startswith("NOTE;") for line in result)

    def test_contact_with_note(self):
        """测试包含备注的联系人序列化"""
        contact = Contact(phone="13800138000", note="工程师")
        result = serialize_to_vcard(contact).splitlines()
        assert "BEGIN:VCARD" in result
        assert "END:VCARD" in result
        assert "TEL;CELL:13800138000" in result
        assert not any(line.startswith("FN;") for line in result)
        assert any(line.startswith("NOTE;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:") for line in result)

    def test_contact_with_name_note(self):
        """测试包含姓名和备注的联系人序列化"""
        contact = Contact(phone="13800138000", name="张三", note="工程师")
        result = serialize_to_vcard(contact).splitlines()
        assert "BEGIN:VCARD" in result
        assert "END:VCARD" in result
        assert "TEL;CELL:13800138000" in result
        assert any(line.startswith("FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:") for line in result)
        assert any(line.startswith("NOTE;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:") for line in result)


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
