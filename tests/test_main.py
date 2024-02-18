from utils.main import mask_card_number, mask_account_number, format_amount, format_date, format_operation


def test_mask_card_number():
    assert mask_card_number("") == "Unknown"
    assert mask_card_number("Счет 1234567890123456") == "Счет **3456"
    assert mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert mask_card_number("Maestro 1615141312111098") == "Maestro 1615 14** **** 1098"


def test_mask_account_number():
    assert mask_account_number("Счет 1234567890125555") == "Счет **5555"
    assert mask_account_number("") == "Счет **"
    assert mask_account_number("Счет 1234-567890-1234") == "Счет **1234"
    assert mask_account_number("Счет 1234-567890-1234") == "Счет **1234"


def test_format_amount():
    assert format_amount({"amount": "1000", "currency": {"code": "USD"}}) == "1000.00 USD"


def test_format_date():
    assert format_date("2020-01-01T12:34:56") == "01.01.2020"
    assert format_date("2019-10-31T23:59:59") == "31.10.2019"
    assert format_date("2023-02-15T00:00:00") == "15.02.2023"
    assert format_date("1940-01-01T00:00:00") == "01.01.1940"


def test_format_operation():
    operation = {
        "date": "2019-12-07T06:17:14.634890",
        "description": "Перевод организации",
        "from": "Visa Classic 2842878893689012",
        "to": "Счет 35158586384610753655",
        "operationAmount": {"amount": "48150.39", "currency": {"code": "USD"}}
    }

    expected_result = """\
07.12.2019
Перевод организации
Visa Classic 2842 87** **** 9012 -> Счет **3655
48150.39 USD"""

    assert format_operation(operation) == expected_result
