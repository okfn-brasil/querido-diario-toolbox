from typing import List, Optional, Sequence
import re


def _calculate_digits(numbers, weights):
    """
    Calculate validation digits for cpf and cnpj for the
    validate_individual_identifiers function
    """
    multiply = [int(num) * weight for num, weight in zip(numbers, weights)]
    total = sum(multiply)
    remainder = total % 11
    if remainder < 2:
        return numbers + "0"
    else:
        return numbers + str(11 - remainder)


def _scan_IDs(text: str, cpf: bool = True) -> List[str]:
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


def _validate_IDs(identifier: str, cpf: bool = True) -> bool:
    """
    Validate identifiers for use in scan_individual_identifiers
    function.
    """
    identifier = re.sub(r"\-|\.|/", "", identifier)
    dv = identifier[:-2]

    CPF_WEIGHTS = (11, 10, 9, 8, 7, 6, 5, 4, 3, 2)
    CNPJ_WEIGHTS = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)

    if cpf:
        check = _calculate_digits(numbers=dv, weights=CPF_WEIGHTS[1:])
        check = _calculate_digits(numbers=check, weights=CPF_WEIGHTS)
    else:
        check = _calculate_digits(numbers=dv, weights=CNPJ_WEIGHTS[1:])
        check = _calculate_digits(numbers=check, weights=CNPJ_WEIGHTS)

    return identifier == check


def scan_cpf(text, validate: Optional[bool] = False) -> Sequence[str]:
    """
    Scan for cpfs and validate cpfs them if required by user.
    """
    cpfs = _scan_IDs(text)

    if validate:
        cpfs = [cpf for cpf in cpfs if _validate_IDs(cpf)]

    if cpfs:
        return set(cpfs)


def scan_cnpj(text, validate: Optional[bool] = False) -> Sequence[str]:
    """
    Scan for cnpjs and validate cpfs them if required by user.
    """
    cnpjs = _scan_IDs(text, cpf=False)

    if validate:
        cnpjs = [cnpj for cnpj in cnpjs if _validate_IDs(cnpj, cpf=False)]

    if cnpjs:
        return set(cnpjs)
