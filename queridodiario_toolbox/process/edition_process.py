import re
from typing import Sequence

CPF_REGEX = r"\d{3}\.\d{3}\.\d{3}\-\d{2}"
CNPJ_REGEX = r"\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}"


def calculate_id_digit(numbers, weights):
    """
    Calculation validation digits for cpf and cnpj for
    validation functions
    """
    multiply = [int(num) * weight for num, weight in zip(numbers, weights)]
    total = sum(multiply)
    remainder = total % 11
    if remainder < 2:
        return numbers + "0"
    else:
        return numbers + str(11 - remainder)


def extract_cpfs(text: str) -> Sequence[str]:
    """
    Extract all substrings in text which match with the CPF pattern
    """
    regex = re.compile(CPF_REGEX)
    cpfs = re.findall(regex, text)
    return cpfs


def is_valid_cpf(cpf: str) -> bool:
    """
    Validates if the given CPF is valid.
    """
    cpf = re.sub(r"\-|\.|/", "", cpf)
    dv = cpf[:-2]
    CPF_WEIGHTS = (11, 10, 9, 8, 7, 6, 5, 4, 3, 2)
    check = calculate_id_digit(numbers=dv, weights=CPF_WEIGHTS[1:])
    check = calculate_id_digit(numbers=check, weights=CPF_WEIGHTS)
    return cpf == check


def extract_and_validate_cpf(text: str) -> Sequence[str]:
    """
    Extract all substrings in text which match with the CPF pattern removing
    those one which digits validates failed.
    """
    cpfs = extract_cpfs(text)
    cpfs = [cpf for cpf in cpfs if is_valid_cpf(cpf)]
    return cpfs


def extract_cnpjs(text: str) -> Sequence[str]:
    """
    Extract all substrings in text which match with the CNPJ pattern
    """
    regex = re.compile(CNPJ_REGEX)
    cnpjs = re.findall(regex, text)
    return cnpjs


def is_valid_cnpj(cnpj: str) -> bool:
    """
    Validates if the given CNPJ is valid.
    """
    cnpj = re.sub(r"\-|\.|/", "", cnpj)
    dv = cnpj[:-2]
    CNPJ_WEIGHTS = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    check = calculate_id_digit(numbers=dv, weights=CNPJ_WEIGHTS[1:])
    check = calculate_id_digit(numbers=check, weights=CNPJ_WEIGHTS)
    return cnpj == check


def extract_and_validate_cnpj(text: str) -> Sequence[str]:
    """
    Extract all substrings in text which match with the CNPJ pattern removing
    those one which digits validates failed.
    """
    cnpjs = extract_cnpjs(text)
    cnpjs = [cnpj for cnpj in cnpjs if is_valid_cnpj(cnpj)]
    return cnpjs
