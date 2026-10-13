import sys

import pytest

from vcf_generator_lite import bootstrap


class TestRequireTkinter:
    """校验绑定缺失时的归因与提示"""

    def test_passes_when_binding_available(self):
        pytest.importorskip("tkinter")

        bootstrap.require_tkinter()

    def test_exits_with_tkinter_wording_when_binding_missing(self, monkeypatch, capsys):
        monkeypatch.setitem(sys.modules, "tkinter", None)

        with pytest.raises(SystemExit) as exit_info:
            bootstrap.require_tkinter()

        assert exit_info.value.code == 1
        error = capsys.readouterr().err
        assert "Tkinter is not available" in error
        assert "Please install Tcl/Tk" not in error

    @pytest.mark.parametrize(
        ("platform_name", "expected_hint"),
        [("win32", True), ("linux", False)],
    )
    def test_windows_hint_depends_on_platform(self, monkeypatch, capsys, platform_name, expected_hint):
        monkeypatch.setitem(sys.modules, "tkinter", None)
        monkeypatch.setattr(sys, "platform", platform_name)

        with pytest.raises(SystemExit):
            bootstrap.require_tkinter()

        error = capsys.readouterr().err
        assert ("'tcl/tk and IDLE' in the Python installer" in error) is expected_hint
