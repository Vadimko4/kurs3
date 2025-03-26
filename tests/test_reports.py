import pytest

from src.reports import get_date_three_month_earlier


@pytest.mark.parametrize('date, expected', [('20.07.2025', '20.04.2025'),
                                            ('04.04.2023', '04.01.2023'),
                                            ('15.02.2024', '15.11.2023')])
def test_get_date_three_month_earlier(date, expected):
    assert get_date_three_month_earlier(date) == expected
