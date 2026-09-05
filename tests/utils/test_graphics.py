from unittest.mock import MagicMock

import pytest

from vcf_generator_lite.utils.graphics import FPixelPadding, parse_ttk_padding


class TestFPixelPadding:
    """测试 FPixelPadding 数据类"""

    def test_default_initialization(self):
        """测试默认初始化，四边均为 0"""
        p = FPixelPadding()
        assert p.left == 0
        assert p.top == 0
        assert p.right == 0
        assert p.bottom == 0

    def test_custom_initialization(self):
        """测试自定义初始化"""
        p = FPixelPadding(left=1, top=2, right=3, bottom=4)
        assert p.left == 1
        assert p.top == 2
        assert p.right == 3
        assert p.bottom == 4

    def test_add(self):
        """测试 __add__ 合并四周边距"""
        a = FPixelPadding(1, 2, 3, 4)
        b = FPixelPadding(5, 6, 7, 8)
        result = a + b
        assert result == FPixelPadding(6, 8, 10, 12)

    def test_sub(self):
        """测试 __sub__ 减去四周边距"""
        a = FPixelPadding(10, 9, 8, 7)
        b = FPixelPadding(1, 2, 3, 4)
        result = a - b
        assert result == FPixelPadding(9, 7, 5, 3)

    def test_to_tuple(self):
        """测试 to_tuple 返回正确的四元组"""
        p = FPixelPadding(1, 2, 3, 4)
        assert p.to_tuple() == (1, 2, 3, 4)

    def test_to_pady(self):
        """测试 to_pady 返回 (top, bottom)"""
        p = FPixelPadding(1, 2, 3, 4)
        assert p.to_pady() == (2, 4)

    def test_is_frozen(self):
        """测试 FPixelPadding 是不可变数据类"""
        p = FPixelPadding(1, 2, 3, 4)
        with pytest.raises(Exception):
            p.left = 99  # type: ignore[misc]

    def test_equality(self):
        """测试相同值的实例相等"""
        assert FPixelPadding(1, 2, 3, 4) == FPixelPadding(1, 2, 3, 4)

    def test_inequality(self):
        """测试不同值的实例不相等"""
        assert FPixelPadding(1, 2, 3, 4) != FPixelPadding(4, 3, 2, 1)


class TestParseTtkPadding:
    """测试 parse_ttk_padding 函数"""

    @staticmethod
    def _make_master(return_value: float | None = None):
        """创建一个 mock master，其 winfo_fpixels 方法返回指定值或原值"""
        master = MagicMock()
        if return_value is not None:
            master.winfo_fpixels.return_value = return_value
        else:

            def _winfo_fpixels(value: str | int | float) -> float:
                return float(value)

            master.winfo_fpixels.side_effect = _winfo_fpixels
        return master

    def test_single_int_value(self):
        """测试单个 int 值，四边相同"""
        master = self._make_master()
        result = parse_ttk_padding(master, 5)
        assert result == FPixelPadding(5, 5, 5, 5)

    def test_single_float_value(self):
        """测试单个 float 值，四边相同"""
        master = self._make_master()
        result = parse_ttk_padding(master, 2.5)
        assert result == FPixelPadding(2.5, 2.5, 2.5, 2.5)

    def test_string_one_value(self):
        """测试字符串 1 个值，四边相同"""
        master = self._make_master()
        result = parse_ttk_padding(master, "10")
        assert result == FPixelPadding(10, 10, 10, 10)

    def test_string_two_values(self):
        """测试字符串 2 个值，(left, top)，right 回退到 left，bottom 回退到 top"""
        master = self._make_master()
        result = parse_ttk_padding(master, "2 4")
        assert result == FPixelPadding(2, 4, 2, 4)

    def test_string_three_values(self):
        """测试字符串 3 个值，(left, top, right)，bottom 回退到 top"""
        master = self._make_master()
        result = parse_ttk_padding(master, "1 2 3")
        assert result == FPixelPadding(1, 2, 3, 2)

    def test_string_four_values(self):
        """测试字符串 4 个值，(left, top, right, bottom)"""
        master = self._make_master()
        result = parse_ttk_padding(master, "1 2 3 4")
        assert result == FPixelPadding(1, 2, 3, 4)

    def test_tuple_input(self):
        """测试 tuple 输入，(left, top, right, bottom)"""
        master = self._make_master()
        result = parse_ttk_padding(master, (1, 2, 3, 4))
        assert result == FPixelPadding(1, 2, 3, 4)

    def test_uses_winfo_fpixels_for_conversion(self):
        """测试调用 master.winfo_fpixels 进行像素转换"""
        master = self._make_master(return_value=7.5)
        result = parse_ttk_padding(master, "1 2")
        assert result == FPixelPadding(7.5, 7.5, 7.5, 7.5)
        assert master.winfo_fpixels.call_count == 2

    def test_empty_string_returns_zero_padding(self):
        """测试空字符串返回全零 padding"""
        master = self._make_master()
        result = parse_ttk_padding(master, "")
        assert result == FPixelPadding(0, 0, 0, 0)
