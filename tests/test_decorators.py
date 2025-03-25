import pytest

from src.decorators import log


@log()
def a_divs_b(a: int, b: int) -> float:
    if not b:
        raise ValueError("На ноль делить нельзя")

    return a / b


def test_log(capsys):
    a_divs_b(4, 2)
    captured = capsys.readouterr()
    assert captured.out == "a_divs_b ok\n"


def test_log_error():
    with pytest.raises(Exception, match="На ноль делить нельзя"):
        a_divs_b(2, 0)
