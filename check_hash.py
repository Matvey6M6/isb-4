import hashlib
import logging

SETTING = {
    'hash': '78495810cec383f3f82049d03a522f5141583d1d6577235c74084c1d21f7a1df4612c05c0d6b5eb15edd1270ab5069f0',
    'initial_digits': '220070',
    'last_digits': '9920',
}


def check_hash(card_number: int) -> int:
    """Функция проверяет соответствие хеша надйенного числа, с данным нам хешем

    Args:
        card_number (int): номер карты

    Returns:
        int: номер карты
    """
    card_hash = hashlib.sha3_384(
        f'{SETTING["initial_digits"]}{card_number}{SETTING["last_digits"]}'.encode()).hexdigest()
    if card_hash == f'{SETTING["hash"]}':
        logging.info("hash matched")
        return card_number
    else:
        return False


def algorithm_luna(card_number: int) -> bool:
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
    bin = [int(i) for i in SETTING['initial_digits']]
    code = [int(i) for i in card_number]
    end = [int(i) for i in SETTING['last_digits']]
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
    if check_sum == int(SETTING['last_digits'][-1]):
        return True
    else:
        return False
