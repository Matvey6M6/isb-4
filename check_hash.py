import hashlib
import logging


def check_hash(card_number: int, setting: dict) -> int:
    """Функция проверяет соответствие хеша надйенного числа, с данным нам хешем

    Args:
        card_number (int): номер карты
        setting (dict): настройки
    Returns:
        int: номер карты
    """
    card_info = f'{setting["initial_digits"][0]}{card_number}{setting["last_digits"]}'
    card_hash = hashlib.sha3_384(card_info.encode()).hexdigest()
    if card_hash == f'{setting["hash"]}':
        logging.info("hash matched")
        return card_number
    else:
        return False


def algorithm_luna(card_number: int, setting: dict) -> bool:
    """Функция проверки номера карты алгоритмом Луна

    Args:
        card_number (int): номер карты

    Returns:
        bool: результата проверки
    """
    logging.info("check by Luhn algorithm")
    card_number = str(card_number)
    if len(card_number) != 6:
        return False
    bin = [int(i) for i in setting['initial_digits'][0]]
    code = [int(i) for i in card_number]
    end = [int(i) for i in setting['last_digits']]
    all_number = bin+code+end
    all_number = all_number[::-1]
    for i, num in enumerate(all_number):
        if i % 2 == 0:
            mul = num*2
            if mul > 9:
                mul -= 9
            all_number[i] = mul
    total_sum = sum(all_number)
    rem = total_sum % 10
    check_sum = 10 - rem if rem != 0 else 0
    if check_sum == int(setting['last_digits'][-1]):
        return True
    else:
        return False
