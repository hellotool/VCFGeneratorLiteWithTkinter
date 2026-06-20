import re
from io import StringIO
from typing import NamedTuple

from vcf_generator_lite.core.vcf_generator import VCFGeneratorTask
from vcf_generator_lite.models.phone_detector import PhoneRule


TEST_PHONE_RULES = [
    PhoneRule(length=11, regex=re.compile(r"^(?:\+86)?1[3456789]\d{9}$")),
]


class Progress(NamedTuple):
    processed: int
    total: int
    determinate: bool


class TestVCFGeneratorIntegration:
    """VCF 生成器的集成测试"""

    # 测试数据
    VALID_INPUT_LIST = [
        "李    四    13445467890",
        " 王五\t13554678907",
        "赵六\t13645436748 ",
    ]

    INVALID_INPUT_LIST = [
        "孙七\t1234567890",  # 电话号码太短
        '周八\t"13789012345"',  # 电话号码包含引号
        "吴九\t13 789012345",  # 电话号码包含空格
        "郑十\t1389012345a",  # 电话号码包含字母
    ]

    IGNORED_INPUT_LIST = [
        "   ",
        "",
        "\t",
    ]

    @property
    def input_content(self):
        input_list = self.IGNORED_INPUT_LIST + self.INVALID_INPUT_LIST + self.IGNORED_INPUT_LIST + self.VALID_INPUT_LIST
        return "\n".join(input_list)

    @property
    def valid_count(self):
        return len(self.VALID_INPUT_LIST)

    @property
    def invalid_count(self):
        return len(self.INVALID_INPUT_LIST)

    def test_vcard_file_generator_full_integration(self):
        """完整的 VCF 生成器集成测试"""
        progress_history: list[Progress] = []
        result_io = StringIO()

        generator = VCFGeneratorTask(
            input_io=self.input_content,
            output_io=result_io,
            phone_rules=TEST_PHONE_RULES,
            progress_listener=lambda processed, total, determinate: progress_history.append(
                Progress(processed=processed, total=total, determinate=determinate)
            ),
        )
        generator.start()
        generator.join(timeout=10.0)

        assert not generator.is_alive()
        assert len(progress_history) > 0
        assert progress_history[-1].processed == progress_history[-1].total == self.valid_count + self.invalid_count
        assert progress_history[-1].determinate is True

        assert generator.result is not None
        assert generator.result.exception is None

        assert generator.result.saved_count == self.valid_count
        assert len(generator.result.invalid_items) == self.invalid_count

        invalid_items_raw = [item.raw_content for item in generator.result.invalid_items]
        assert invalid_items_raw == self.INVALID_INPUT_LIST

        result_list = [item for item in result_io.getvalue().split("\n\n") if item.strip() != ""]
        assert len(result_list) == self.valid_count

        for result_item in result_list:
            assert result_item.startswith("BEGIN:VCARD\n")
            assert result_item.endswith("\nEND:VCARD")
            assert "TEL;CELL:" in result_item
            assert "FN;" in result_item

    def test_empty_input(self):
        """测试空输入"""
        progress_history: list[Progress] = []
        result_io = StringIO()

        generator = VCFGeneratorTask(
            input_io="",
            output_io=result_io,
            phone_rules=TEST_PHONE_RULES,
            progress_listener=lambda processed, total, determinate: progress_history.append(
                Progress(processed=processed, total=total, determinate=determinate)
            ),
        )
        generator.start()
        generator.join(timeout=10.0)

        assert not generator.is_alive()
        assert progress_history[-1].processed == progress_history[-1].total == 0
        assert progress_history[-1].determinate is True

        assert generator.result is not None
        assert generator.result.exception is None
        assert generator.result.saved_count == 0
        assert len(generator.result.invalid_items) == 0
        assert result_io.getvalue() == ""

    def test__new_line_end_input(self):
        """测试末尾为换行符的输入"""
        progress_history: list[Progress] = []
        result_io = StringIO()

        generator = VCFGeneratorTask(
            input_io="\n".join(self.VALID_INPUT_LIST) + "\n",
            output_io=result_io,
            phone_rules=TEST_PHONE_RULES,
            progress_listener=lambda processed, total, determinate: progress_history.append(
                Progress(processed=processed, total=total, determinate=determinate)
            ),
        )
        generator.start()
        generator.join(timeout=10.0)

        assert not generator.is_alive()
        assert progress_history[-1].processed == progress_history[-1].total == self.valid_count
        assert progress_history[-1].determinate is True

        assert generator.result is not None
        assert generator.result.exception is None
        assert generator.result.saved_count == self.valid_count
        assert len(generator.result.invalid_items) == 0

    def test_only_invalid_input(self):
        """测试只有无效输入的情况"""
        progress_history: list[Progress] = []
        result_io = StringIO()
        invalid_content = "\n".join(self.INVALID_INPUT_LIST)

        generator = VCFGeneratorTask(
            input_io=invalid_content,
            output_io=result_io,
            phone_rules=TEST_PHONE_RULES,
            progress_listener=lambda processed, total, determinate: progress_history.append(
                Progress(processed=processed, total=total, determinate=determinate)
            ),
        )
        generator.start()
        generator.join(timeout=10.0)

        assert not generator.is_alive()
        assert progress_history[-1].processed == progress_history[-1].total == self.invalid_count
        assert progress_history[-1].determinate is True

        assert generator.result is not None
        assert generator.result.exception is None
        assert generator.result.saved_count == 0
        assert len(generator.result.invalid_items) == self.invalid_count

        assert result_io.getvalue() == ""
