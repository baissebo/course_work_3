import json
from datetime import datetime


def read_operations_from_file(file_path):
    """
    Читает данные из файла формата JSON и возвращает их в виде объекта Python.
    """
    with open(file_path, 'r') as file:
        operations = json.load(file)
    return operations


def mask_card_number(card_number):
    """
       Маскирует номер карты и возвращает отформатированную строку.
       Если в строке присутствует слово 'Счет', то возвращает последние 4 цифры
       Иначе возвращает 'Unknown'
      """
    if card_number == "":
        return "Unknown"
    elif "Счет" in card_number:
        return f"Счет **{card_number[-4:]}"
    else:
        return f"{card_number[:-12]} {card_number[-12:-10]}** **** {card_number[-4:]}"


def mask_account_number(to):
    """
    Скрывает номер счета оставляя только последние 4 цифры
    """
    return f"Счет **{to[-4:]}"


def format_amount(amount):
    """
    Форматирует сумму операции и возвращает отформатированную строку.
    """
    return "{:.2f} {}".format(float(amount["amount"]), amount["currency"]["code"])


def format_date(date):
    """
    Форматирует дату в формате ДД.ММ.ГГГГ и возвращает отформатированную строку.

    """
    date_obj = datetime.strptime(date[:10], "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d.%m.%Y")
    return formatted_date


def format_operation(operation):
    """
    Форматирует каждый аспект операции (дата, описание, номер карты/счета и сумма операции)
    в отдельные строки и объединяет их в одну строку с использованием символа новой строки.
    """
    formatted_operation = [
        format_date(operation.get("date")),
        operation.get("description"),
        f"{mask_card_number(operation.get('from', ''))} -> {mask_account_number(operation.get('to', ''))}",
        format_amount(operation.get("operationAmount")),
    ]
    return "\n".join(formatted_operation)


def print_last_executed_operations():
    """
    Функция читает список операций из JSON-файла. Затем фильтрует список,
    оставляя только операции со статусом "EXECUTED". Далее, список отсортировывается по дате каждой
    операции в порядке убывания. В конце последние 5 выполненных операций форматируются в виде строк
    и объединение отформатированных операций с двойным переносам строки.
    """
    operations = read_operations_from_file("/Users/andalou/PycharmProjects/course_work_3/utils/operations.json")
    executed_operations = [operation for operation in operations if operation.get("state") == "EXECUTED"]
    last_executed_operations = sorted(
        executed_operations, key=lambda operation: operation.get("date"), reverse=True
    )[:5]

    formatted_operations = [format_operation(operation) for operation in last_executed_operations]
    formatted_string = "\n\n".join(formatted_operations)

    print(formatted_string)


if __name__ == "__main__":
    print_last_executed_operations()
