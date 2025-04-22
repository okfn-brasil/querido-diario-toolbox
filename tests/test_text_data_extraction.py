from unittest import TestCase

from querido_diario_toolbox.process.edition_process import (
    extract_and_validate_cnpj,
    extract_and_validate_cpf,
    extract_cnpjs,
    extract_cpfs,
    is_valid_cnpj,
    is_valid_cpf,
)


class DataExtractionTests(TestCase):
    def setUp(self):
        self.test_string = """
Invalid CNPJ and CPF:
12.333.444/0001-55
12.333.444/0001-55
12.333.444/0001-55
12.333.444/0001-55
12.333.444/0001-55
111.222.333-00
444.555.666-11
Valid CNPJ and CPF:
453.178.287-91
133.267.246-91
070.680.938-68
062.446.028-20
05.144.757/0001-72
38.902.822/0001-30
04.090.574/0001-59
"""

    def test_extract_cpf_from_text(self):
        cpfs = extract_cpfs(self.test_string)
        expected_cpf = [
            "453.178.287-91",
            "133.267.246-91",
            "070.680.938-68",
            "062.446.028-20",
            "111.222.333-00",
            "444.555.666-11",
        ]
        self.assertCountEqual(expected_cpf, cpfs)

    def test_extract_cnpj_from_text(self):
        cnpjs = extract_cnpjs(self.test_string)
        expected_cnpj = [
            "05.144.757/0001-72",
            "38.902.822/0001-30",
            "04.090.574/0001-59",
            "12.333.444/0001-55",
            "12.333.444/0001-55",
            "12.333.444/0001-55",
            "12.333.444/0001-55",
            "12.333.444/0001-55",
        ]
        self.assertCountEqual(expected_cnpj, cnpjs)

    def test_validate_cpf(self):
        cpf = "079.692.759-66"
        valid_cpf = is_valid_cpf(cpf)
        self.assertTrue(valid_cpf)

    def test_validate_cnpj(self):
        cnpj = "26.994.558/0001-23"
        valid_cnpj = is_valid_cnpj(cnpj)
        self.assertTrue(valid_cnpj)

    def test_extract_and_validate_cpf_from_text(self):
        cpfs = extract_and_validate_cpf(self.test_string)
        expected_cpf = [
            "453.178.287-91",
            "133.267.246-91",
            "070.680.938-68",
            "062.446.028-20",
        ]
        self.assertCountEqual(expected_cpf, cpfs)

    def test_extract_and_validate_cnpj_from_text(self):
        cnpjs = extract_and_validate_cnpj(self.test_string)
        expected_cnpj = [
            "05.144.757/0001-72",
            "38.902.822/0001-30",
            "04.090.574/0001-59",
        ]
        self.assertCountEqual(expected_cnpj, cnpjs)
