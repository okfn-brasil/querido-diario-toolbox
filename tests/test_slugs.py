import unittest

from querido_diario_toolbox.slugs.slugs import make_entity_slug


class TestMakeEntitySlug(unittest.TestCase):
    # NAME ARG
    def test_if_name_is_empty_return_empty(self):
        self.assertEqual("", make_entity_slug(""))

    def test_if_name_is_not_string_raise_error(self):
        with self.assertRaises(ValueError):
            make_entity_slug(1917)
        with self.assertRaises(ValueError):
            make_entity_slug(["texto"])
        with self.assertRaises(ValueError):
            make_entity_slug(True)

    # PREFIX ARG
    def test_if_prefix_is_not_string_raise_error(self):
        with self.assertRaises(ValueError):
            make_entity_slug("Suzano", 1917)
        with self.assertRaises(ValueError):
            make_entity_slug("Suzano", ["texto"])
        with self.assertRaises(ValueError):
            make_entity_slug("Suzano", True)

    def test_if_empty_prefix_is_ignored(self):
        self.assertEqual("rio_de_janeiro", make_entity_slug("Rio de Janeiro", ""))

    def test_if_whitespace_prefix_is_ignored(self):
        self.assertEqual("rio_de_janeiro", make_entity_slug("Rio de Janeiro", " "))

    def test_if_special_character_prefix_is_ignored(self):
        self.assertEqual("rio_de_janeiro", make_entity_slug("Rio de Janeiro", "*"))
        self.assertEqual("rio_de_janeiro", make_entity_slug("Rio de Janeiro", "#"))
        self.assertEqual("rio_de_janeiro", make_entity_slug("Rio de Janeiro", "$"))
        self.assertEqual("rio_de_janeiro", make_entity_slug("Rio de Janeiro", "!"))

    # SEPARATOR ARG
    def test_if_separator_is_not_string_raise_error(self):
        with self.assertRaises(ValueError):
            make_entity_slug("Rio de Janeiro", separator=1)
        with self.assertRaises(ValueError):
            make_entity_slug("Rio de Janeiro", separator=["texto"])
        with self.assertRaises(ValueError):
            make_entity_slug("Rio de Janeiro", separator=True)

    def test_empty_separator_should_return_full_concatenated_string(self):
        self.assertEqual("minasgerais", make_entity_slug("Minas Gerais", separator=""))

    def test_underscore_separator_should_return_underscored_string(self):
        self.assertEqual("rio_grande_do_norte", make_entity_slug("Rio Grande do Norte"))
        self.assertEqual(
            "rio_grande_do_norte",
            make_entity_slug("Rio Grande do Norte", separator="_"),
        )

    def test_hyphen_separator_should_return_hyphened_string(self):
        self.assertEqual(
            "agencia-reguladora-intermunicipal-de-saneamento",
            make_entity_slug(
                "Agência Reguladora Intermunicipal de Saneamento", separator="-"
            ),
        )

    def test_others_characters_separator_raise_error(self):
        with self.assertRaises(ValueError):
            make_entity_slug("Pernambuco", separator="#")
        with self.assertRaises(ValueError):
            make_entity_slug("Pernambuco", separator="5")
        with self.assertRaises(ValueError):
            make_entity_slug("Pernambuco", separator=".")
        with self.assertRaises(ValueError):
            make_entity_slug("Pernambuco", separator="a")

    # CONTENT
    def test_prefix_should_always_be_first_than_name(self):
        self.assertEqual("pb_santa_cecilia", make_entity_slug("Santa Cecília", "PB"))
        self.assertNotEqual("santa_cecilia_pb", make_entity_slug("Santa Cecília", "PB"))

    def test_if_name_has_spaces_replaces_with_separator(self):
        self.assertEqual("alto_bela_vista", make_entity_slug("Alto Bela Vista"))

    def test_if_name_has_uppercase_returns_lowercase(self):
        self.assertEqual("sao_paulo", make_entity_slug("São Paulo"))
        self.assertEqual("uniao", make_entity_slug("União"))

    def test_if_name_has_diacritics_removes_them(self):
        self.assertEqual("abadiania", make_entity_slug("Abadiânia"))
        self.assertEqual(
            "associacao_amazonense_de_municipios",
            make_entity_slug("Associação Amazonense de Municípios"),
        )
        self.assertEqual(
            "federacao_das_associacoes_de_municipios_do_estado_do_para",
            make_entity_slug(
                "Federação das Associações de Municípios do Estado do Pará"
            ),
        )

    def test_if_name_has_single_quotes_removes_them(self):
        self.assertEqual(
            "santa_barbara_doeste", make_entity_slug("Santa Bárbara D'Oeste")
        )
        self.assertEqual(
            "santana_do_livramento", make_entity_slug("Sant'Ana do Livramento")
        )
        self.assertEqual(
            "olhodagua_do_borges", make_entity_slug("Olho-d'Água do Borges")
        )
        self.assertEqual(
            "olho_dagua_do_casado", make_entity_slug("Olho d'Água do Casado")
        )

    def test_if_name_has_hyphen_removes_them(self):
        self.assertEqual(
            "governador_dixsept_rosado", make_entity_slug("Governador Dix-Sept Rosado")
        )
        self.assertEqual("naometoque", make_entity_slug("Não-Me-Toque"))

    def test_if_name_has_hyphen_and_separator_is_hyphen_removes_original_hyphens(self):
        self.assertEqual(
            "governador-dixsept-rosado",
            make_entity_slug("Governador Dix-Sept Rosado", separator="-"),
        )
        self.assertEqual(
            "olhodagua-do-borges",
            make_entity_slug("Olho-d'Água do Borges", separator="-"),
        )
