import re
import datetime
from service.models import SIZE_OF_PART_NAME
from service.models import SIZE_OF_PASSPORT_NUMBER
from service.models import SIZE_OF_PASSPORT_SERIES

from service.models import SimpleWords
from service.models import IdentifiablePerson, IdentificationAttempt, BadPassports
from service.models import BadPassports


def check(check_list, value):
    for check_function in check_list:
        msg, ok = check_function(value)
        if not ok:
            return msg, ok
    return '', True


def check_passport_series(series: str):
    check_list = [
        lambda x: ('', True) if not bool(re.search(r'[^0-9]', x))
        else ('Серия должна содержать цифры от 0 до 9', False),
        lambda s: ('', True) if len(s) == SIZE_OF_PASSPORT_SERIES
        else ('Серия должна содержать {} цифр(ы)'.format(SIZE_OF_PASSPORT_SERIES), False),
    ]
    return check(check_list, series)


def check_passport_number(number: str):
    check_list = [
        lambda n: ('', True) if not bool(re.search(r'[^0-9]', n))
        else ('Номер должен содержать цифры от 0 до 9', False),
        lambda n: ('', True) if len(n) == SIZE_OF_PASSPORT_NUMBER
        else ('Номер должен содержать {} цифр(ы)'.format(SIZE_OF_PASSPORT_NUMBER), False),
    ]
    return check(check_list, number)


def check_birthday(birthday: datetime.date):
    check_list = [
        lambda b: ('', True) if datetime.date.today() > b
        else ('Дата рождения позже текущей даты', False),
        lambda b: ('', True) if (datetime.date.today() - b).days > 18 * 365
        else ('Клиент должен быть старше 18 лет', False),
        lambda b: ('', True) if (datetime.date.today() - b).days < 100 * 365
        else ('Некорректное значение даты рождения', False),
    ]
    return check(check_list, birthday)


def check_part_of_name(part_of_name: str):
    check_list = [
        lambda p: ('', True) if len(p) >= 2
        else ('Фамилия/Имя/Отчество не может быть короче 2-х букв', False),
        lambda p: ('', True) if len(p) < SIZE_OF_PART_NAME
        else ('Фамилия/Имя/Отчество не может быть длиннее {} букв'.format(SIZE_OF_PART_NAME), False),
        lambda p: ('', True) if not bool(re.search(r'[^а-яА-ЯёЁ]', p))
        else ('Фамилия/Имя/Отчество может содержать только кириллические буквы', False),
        __compare_part_of_name_with_simple_word,
    ]
    return check(check_list, part_of_name)


def __compare_part_of_name_with_simple_word(part_of_name):
    if SimpleWords.objects.filter(value=part_of_name).count() > 0:
        return 'Некорректное Фамилия/Имя/Отчество', False
    return '', True


def check_person(data: dict):
    check_list = [
        __check_bad_passports,
        __check_passport_is_already_identified,
        __check_differences_passport_data,
    ]
    return check(check_list, data)


def __check_bad_passports(data):
    if BadPassports.objects.filter(passport_number=data['passport_number'],
                                   passport_series=data['passport_series']).count() > 0:
        return 'Плохой клиент', False
    return '', True


def __check_passport_is_already_identified(data):
    saved_persons = IdentifiablePerson.objects.filter(passport_number=data['passport_number'],
                                                      passport_series=data['passport_series'])
    is_identified_passport = False
    for person in saved_persons:
        if person.identificationattempt_set.filter(response=True).count() > 0:
            is_identified_passport = True
            break
    if is_identified_passport:
        return 'Такой паспорт уже зарегистрирован', False
    return '', True


def __check_differences_passport_data(data):
    # Реализуется через сравнение текущего запроса на идентификацию
    # c успешными запросами на идентификацию в течении некоторого периода времени
    return '', True
