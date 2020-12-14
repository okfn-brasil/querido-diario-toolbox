from typing import List, Optional
import re


# edition methods
def _is_a_single_municipality():
    pass


def split_pages():
    pass


def split_sections():
    pass


def calculate_id_digit(numbers, weights):
    """
        Calculation validation digits for cpf and cnpj for
        validate_individual_identifiers function
    """
    multiply = [int(num) * weight for num, weight in zip(numbers, weights)]
    total = sum(multiply)
    remainder = total % 11
    if remainder < 2:
        return numbers + "0"
    else:
        return numbers + str(11 - remainder)


def scan_individual_identifiers(text: str, cpf: bool = True) -> List[str]:
    """
        Scan for cpfs (social security IDs) and cnpjs (corporate IDs)
        in gazette.
    """
    if cpf:
        regex = re.compile(r"\w{3}\.\w{3}\.\w{3}\-\w{2}")
    else:
        regex = re.compile(r"\w{2}\.\w{3}\.\w{3}/\w{4}\-\w{2}")

    identifiers = re.findall(regex, text)
    return identifiers


def validate_individual_identifiers(identifier: str, cpf: bool = True) -> bool:
    """
        Validate identifiers for use in scan_individual_identifiers
        function.
    """
    identifier = re.sub(r"\-|\.|/", "", identifier)
    dv = identifier[:-2]

    CPF_WEIGHTS = (11, 10, 9, 8, 7, 6, 5, 4, 3, 2)
    CNPJ_WEIGHTS = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)

    if cpf:
        check = calculate_id_digit(numbers=dv, weights=CPF_WEIGHTS[1:])
        check = calculate_id_digit(numbers=check, weights=CPF_WEIGHTS)
    else:
        check = calculate_id_digit(numbers=dv, weights=CNPJ_WEIGHTS[1:])
        check = calculate_id_digit(numbers=check, weights=CNPJ_WEIGHTS)

    return identifier == check


def extract_procurement():
    pass
