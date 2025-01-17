import os
from unittest import TestCase, expectedFailure
from unittest.mock import patch
from querido_diario_toolbox import Gazette
from querido_diario_toolbox.etl.apache_tika_text_extractor import ApacheTikaExtractor
from querido_diario_toolbox.etl.text_extractor import create_text_extractor
from querido_diario_toolbox.etl.text_extractor_interface import TextExtractor

if os.path.basename(os.getcwd()) == "tests":
     ROOT = "data/"
else:
    ROOT = "tests/data/"
TIKA_PATH = os.path.join(ROOT, "tika-app-1.24.1.jar")


class ApacheTikaTextExtractorTests(TestCase):
    def test_if_apache_tika_extractor_is_valid_text_extractor(self):
        apache_tika_extractor = ApacheTikaExtractor(TIKA_PATH)
        self.assertIsInstance(apache_tika_extractor, TextExtractor)
        self.assertEqual(apache_tika_extractor.apache_tika_jar, TIKA_PATH)

    @expectedFailure
    def test_if_class_check_if_jar_file_exists(self):
        ApacheTikaExtractor("test/jar/path")

    @expectedFailure
    def test_if_class_check_if_binary_is_jar_file(self):
        ApacheTikaExtractor("fake_gazette.doc")

    def test_function_to_assembly_apache_tika_command(self):
        apache_tika_extractor = ApacheTikaExtractor(TIKA_PATH)
        gazette_file = "test/to/gazette/file"
        expected_command = (
            f"java -jar {TIKA_PATH} --encoding=UTF-8 --text {gazette_file}"
        )
        apache_tika_command = apache_tika_extractor._build_apache_tika_command(
            gazette_file
        )
        self.assertEqual(apache_tika_command, expected_command)

    @expectedFailure
    def test_extract_text_from_file_with_invalid_file(self):
        apache_tika_extractor = ApacheTikaExtractor(TIKA_PATH)
        gazette = Gazette(filepath="/file/doest/not/exists")
        apache_tika_extractor.extract_text(gazette)

    def test_extract_text(self):
        apache_tika_extractor = ApacheTikaExtractor(TIKA_PATH)
        gazette = Gazette(filepath=ROOT + "/fake_gazette.pdf")
        apache_tika_extractor.extract_text(gazette)
        self.assertTrue(os.path.exists(ROOT + "/fake_gazette.txt"))
        self.assertEqual(ROOT + "/fake_gazette.txt", gazette.content_file)

    def test_load_text(self):
        apache_tika_extractor = ApacheTikaExtractor(TIKA_PATH)
        gazette = Gazette(filepath=ROOT + "/fake_gazette.pdf")
        apache_tika_extractor.extract_text(gazette)
        apache_tika_extractor.load_content(gazette)
        expected_content = "Hi this is a document created to test the text extraction for the Querido Diário project."
        self.assertIn(expected_content, gazette.content)

    def test_extract_metadata(self):
        apache_tika_extractor = ApacheTikaExtractor(TIKA_PATH)
        gazette = Gazette(filepath=ROOT + "/fake_gazette.pdf")
        apache_tika_extractor.extract_metadata(gazette)
        self.assertTrue(os.path.exists(ROOT + "/fake_gazette.json"))
        self.assertEqual(ROOT + "/fake_gazette.json", gazette.metadata_file)

    def test_load_metadata(self):
        apache_tika_extractor = ApacheTikaExtractor(TIKA_PATH)
        gazette = Gazette(filepath=ROOT + "/fake_gazette.pdf")
        apache_tika_extractor.extract_metadata(gazette)
        apache_tika_extractor.load_metadata(gazette)
        self.assertIsInstance(gazette.metadata, dict)
        self.assertNotEqual(gazette.metadata.items(), None)

    def test_create_text_extractor(self):
        config = {"apache_tika_jar": TIKA_PATH}
        text_extractor = create_text_extractor(config)
        self.assertIsInstance(text_extractor, TextExtractor)
        self.assertEqual(text_extractor.apache_tika_jar, TIKA_PATH)