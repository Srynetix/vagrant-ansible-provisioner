import pytest

from vagrant_ansible_provisioner.utils import (
    bail,
    exec_and_quit,
    exec_or_bail,
    yes_no_prompt,
)


def test_bail(capsys):
    try:
        bail()
    except SystemExit:
        captured = capsys.readouterr()
        assert captured.err == "❌ Abort.\n"


def test_exec_or_bail_success(mock_and_trace_calls, capsys):
    os_system_calls = mock_and_trace_calls("subprocess.call", return_value=0)

    exec_or_bail("custom-command", verbose=True)

    captured = capsys.readouterr()
    assert os_system_calls == [(["custom-command"], {})]
    assert captured.out == "⚙️  Executing command 'custom-command' ...\n\n"


def test_exec_or_bail_error(mock_and_trace_calls, capsys):
    os_system_calls = mock_and_trace_calls("subprocess.call", return_value=1)

    with pytest.raises(SystemExit):
        exec_or_bail("custom-command", verbose=True)

    captured = capsys.readouterr()
    assert os_system_calls == [(["custom-command"], {})]
    assert captured.out == "⚙️  Executing command 'custom-command' ...\n\n"


def test_exec_and_quit_success(mock_and_trace_calls, capsys):
    os_system_calls = mock_and_trace_calls("subprocess.call", return_value=0)

    with pytest.raises(SystemExit, match=r"^0$"):
        exec_and_quit("This is a test.", "custom-command", verbose=True)

    captured = capsys.readouterr()
    assert os_system_calls == [(["custom-command"], {})]
    assert captured.out == "\n".join(
        ("⚙️  This is a test.", "⚙️  Executing command 'custom-command' ...\n", "✅ Success.\n")
    )


def test_exec_and_quit_error(mock_and_trace_calls, capsys):
    os_system_calls = mock_and_trace_calls("subprocess.call", return_value=1)

    with pytest.raises(SystemExit, match=r"^1$"):
        exec_and_quit("This is a test.", "custom-command", verbose=True)

    captured = capsys.readouterr()
    assert os_system_calls == [(["custom-command"], {})]
    assert captured.out == "\n".join(
        (
            "⚙️  This is a test.",
            "⚙️  Executing command 'custom-command' ...\n\n",
        )
    )
    assert captured.err == "❌ Abort.\n"


def test_yes_no_prompt_yes(mock_and_trace_calls):
    input_calls = mock_and_trace_calls("builtins.input", return_value="Y")

    answer = yes_no_prompt("Question?")

    assert answer is True
    assert input_calls == [("? Question? (y/n) ", {})]


def test_yes_no_prompt_no(mock_and_trace_calls):
    input_calls = mock_and_trace_calls("builtins.input", return_value="N")

    answer = yes_no_prompt("Question?")

    assert answer is False
    assert input_calls == [("? Question? (y/n) ", {})]
