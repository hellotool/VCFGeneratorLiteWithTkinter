from collections.abc import Iterator
from types import SimpleNamespace, TracebackType
from typing import cast, override
from tkinter import Event, Misc, TclError, Tk, Toplevel
from tkinter.ttk import Frame

import pytest

from vcf_generator_lite.ui.windows.main_window.layout import MainLayout
from vcf_generator_lite.ui.windows.main_window.states import GenerationState


class RecordingListener(MainLayout.Listener):
    """记录布局回调的假监听器。"""

    def __init__(self) -> None:
        self.calls: list[str] = []

    @override
    def on_generate(self, event: Event | None = None) -> None:
        self.calls.append("generate")

    @override
    def on_stop_generation(self, event: Event | None = None) -> None:
        self.calls.append("stop")


def _raise_callback_exception(exc: type[BaseException], val: BaseException, tb: TracebackType | None = None) -> None:
    """让绑定回调中的异常直接抛出，避免测试静默吞掉失败。"""
    raise val


def _refresh(misc: Misc, times: int = 3) -> None:
    """推进事件循环，让窗口的映射与焦点状态落到实现上。"""
    for _ in range(times):
        misc.update()


def _submit_sequence(window: Misc) -> str:
    """取当前窗口系统下输入框内的提交组合键。"""
    toplevel = window.winfo_toplevel()
    return "<Command-Return>" if toplevel._windowingsystem == "aqua" else "<Control-Return>"


def _is_missing_display(error: TclError) -> bool:
    """判定是否真的缺少图形显示；其余 ``TclError`` 属于环境故障，必须抛出而不是跳过。"""
    message = str(error).lower()
    return "no display name" in message or "couldn't connect to display" in message


def _press_focused(window: Misc, widget: Misc, sequence: str) -> None:
    """把焦点交给 widget 后向它发送一次按键，并确认真的拿到过焦点。"""
    window.focus_force()
    widget.focus_force()
    _refresh(window, 2)
    focused = window.focus_get()
    assert focused is not None, f"焦点未落到 {widget}"
    assert str(focused) == str(widget), f"焦点落到 {focused}"
    focused.event_generate(sequence)
    _refresh(window, 2)


@pytest.fixture(scope="session")
def root() -> Iterator[Tk]:
    """测试会话共用的根窗口：创建后立即 ``withdraw``，只作为被测 Toplevel 的宿主。"""
    try:
        tk_root = Tk()
    except TclError as exc:
        if not _is_missing_display(exc):
            raise
        pytest.skip("当前环境没有可用的图形显示")
    tk_root.report_callback_exception = _raise_callback_exception
    tk_root.withdraw()
    yield tk_root
    tk_root.destroy()


@pytest.fixture()
def window(root: Tk) -> Iterator[Toplevel]:
    """每个用例一个独立 Toplevel，用例结束整体销毁，绑定不会留在共享根窗口上。"""
    top = Toplevel(root)
    top.geometry("480x360+-32000+-32000")
    _refresh(top)
    yield top
    top.destroy()
    _refresh(root)


@pytest.fixture()
def listener() -> RecordingListener:
    return RecordingListener()


@pytest.fixture()
def layout(window: Toplevel, listener: RecordingListener) -> MainLayout:
    main_layout = MainLayout(window, listener)
    _refresh(window)
    return main_layout


class TestInputAreaKeys:
    """校验输入框区域里 Enter 与提交组合键的分工。"""

    def test_combo_submits_without_inserting_newline(
        self,
        window: Toplevel,
        layout: MainLayout,
        listener: RecordingListener,
    ):
        layout.content_text.delete("1.0", "end")
        layout.content_text.insert("1.0", "a\nb")

        _press_focused(window, layout.content_text, _submit_sequence(window))

        assert listener.calls == ["generate"]
        assert layout.get_text_content() == "a\nb"

    def test_plain_enter_in_text_inserts_newline_only(
        self, window: Toplevel, layout: MainLayout, listener: RecordingListener
    ):
        layout.content_text.delete("1.0", "end")
        layout.content_text.insert("1.0", "a\nb")

        _press_focused(window, layout.content_text, "<Return>")

        assert listener.calls == []
        assert layout.get_text_content() == "a\nb\n"

    def test_enter_on_scrollbar_is_not_submitted(
        self, window: Toplevel, layout: MainLayout, listener: RecordingListener
    ):
        vbar = layout.content_text.vbar
        assert vbar is not None

        _press_focused(window, vbar, "<Return>")

        assert listener.calls == []

    def test_enter_on_window_submits(self, window: Toplevel, layout: MainLayout, listener: RecordingListener):
        """焦点落在窗口本身时 Enter 提交——祖先路径不该被判据吞掉。"""
        _press_focused(window, window, "<Return>")

        assert listener.calls == ["generate"]

    def test_enter_on_button_submits(self, window: Toplevel, layout: MainLayout, listener: RecordingListener):
        _press_focused(window, layout.generate_or_stop_button, "<Return>")

        assert listener.calls == ["generate"]

    def test_guard_passes_ancestor_and_same_prefix_but_not_descendant(
        self, layout: MainLayout, listener: RecordingListener
    ):
        """钉住判据的三类路径：祖先与同前缀兄弟放行，子控件拦下。"""
        text_frame = layout.content_text.frame
        container = text_frame.master
        assert container is not None
        near_miss = Frame(container, name=f"{str(text_frame).rpartition('.')[2]}near")
        descendant = Frame(text_frame)
        assert str(near_miss) == str(text_frame) + "near"
        assert str(descendant).startswith(str(text_frame) + ".")
        try:
            layout.on_return(cast(Event, SimpleNamespace(widget=container)))
            assert listener.calls == ["generate"]

            listener.calls.clear()
            layout.on_return(cast(Event, SimpleNamespace(widget=near_miss)))
            assert listener.calls == ["generate"]

            listener.calls.clear()
            layout.on_return(cast(Event, SimpleNamespace(widget=descendant)))
            assert listener.calls == []
        finally:
            near_miss.destroy()
            descendant.destroy()


class TestSubmitFollowsUiState:
    """校验提交动作的分发与按钮显示同源。"""

    @pytest.mark.parametrize(
        ("state", "expected_call"),
        [
            (GenerationState.IDLE, "generate"),
            (GenerationState.GENERATING, "stop"),
            (GenerationState.STOPPING, "stop"),
        ],
    )
    def test_combo_dispatches_by_ui_state(
        self,
        window: Toplevel,
        layout: MainLayout,
        listener: RecordingListener,
        state: GenerationState,
        expected_call: str,
    ):
        layout.set_generating(state)

        _press_focused(window, layout.content_text, _submit_sequence(window))

        assert listener.calls == [expected_call]

    def test_button_click_dispatches_by_ui_state(self, layout: MainLayout, listener: RecordingListener):
        layout.set_generating(GenerationState.GENERATING)

        layout.generate_or_stop_button.invoke()

        assert listener.calls == ["stop"]
