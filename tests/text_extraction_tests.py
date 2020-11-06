from unittest import TestCase
import os

from querido_diario.etl.file_transformation import get_text_from_file


class TextExtractionTests(TestCase):

    APACHE_TIKA_JAR_PATH = "/tika-app.jar"

    def tearDown(self):
        self.clean_txt_file_generated_during_tests()

    def clean_txt_file_generated_during_tests(self):
        for root, dirs, files in os.walk("tests/data/"):
            for generated_file in self.get_generated_files_during_tests(root, files):
                print(f"{generated_file}")
                os.remove(generated_file)

    def get_generated_files_during_tests(self, root, files):
        for f in files:
            if ".txt" in f and f != "fake_gazette.txt":
                yield f"{root}{f}"

    def test_extract_text_from_invalid_file(self):
        with self.assertRaisesRegex(Exception, "File does not exists"):
            get_text_from_file(
                "file/does/not/exits", apache_tika_jar=self.APACHE_TIKA_JAR_PATH
            )

    def test_extract_text_using_invalid_apache_tika_jar_path(self):
        with self.assertRaisesRegex(Exception, "File does not exists"):
            get_text_from_file(
                "tests/data/fake_gazette.pdf",
                apache_tika_jar="/invalid/apache/tika/jar/path",
            )

    def test_extract_text_using_invalid_file_type_apache_tika_(self):
        with self.assertRaisesRegex(Exception, "Expected Apache Tika jar file"):
            get_text_from_file(
                "tests/data/fake_gazette.pdf",
                apache_tika_jar="tests/data/fake_gazette.pdf",
            )

    def test_extract_from_invalid_file_type_should_fail(self):
        with self.assertRaisesRegex(Exception, "Unsupported file type"):
            get_text_from_file(
                "tests/data/fake_gazette.jpg", apache_tika_jar=self.APACHE_TIKA_JAR_PATH
            )

    def test_extract_from_pdf_file_should_return_text_file(self):
        text_file = get_text_from_file(
            "tests/data/fake_gazette.pdf", apache_tika_jar=self.APACHE_TIKA_JAR_PATH
        )
        self.assertIsNotNone(text_file)
        self.assertNotEqual(0, len(text_file))
        self.check_if_text_has_the_fake_text(text_file)

    def test_extract_from_docx_file_should_return_text_file(self):
        text_file = get_text_from_file(
            "tests/data/fake_gazette.docx", apache_tika_jar=self.APACHE_TIKA_JAR_PATH
        )
        self.assertIsNotNone(text_file)
        self.assertNotEqual(0, len(text_file))
        self.check_if_text_has_the_fake_text(text_file)

    def test_extract_from_doc_file_should_return_text_file(self):
        text_file = get_text_from_file(
            "tests/data/fake_gazette.doc", apache_tika_jar=self.APACHE_TIKA_JAR_PATH
        )
        self.assertIsNotNone(text_file)
        self.assertNotEqual(0, len(text_file))
        self.check_if_text_has_the_fake_text(text_file)

    def test_extract_from_odt_file_should_return_text_file(self):
        text_file = get_text_from_file(
            "tests/data/fake_gazette.odt", apache_tika_jar=self.APACHE_TIKA_JAR_PATH
        )
        self.assertIsNotNone(text_file)
        self.assertNotEqual(0, len(text_file))
        self.check_if_text_has_the_fake_text(text_file)

    def test_extract_from_txt_file_should_return_text_file(self):
        text = get_text_from_file(
            "tests/data/fake_gazette.txt", apache_tika_jar=self.APACHE_TIKA_JAR_PATH
        )
        self.assertIsNotNone(text)
        self.assertNotEqual(0, len(text))
        self.check_if_text_has_the_fake_text(text)

    def check_if_text_has_the_fake_text(self, text_file_path):
        with open(text_file_path, "r") as f:
            text = f.read()
            self.assertIn(
                "Hi this is a document created to test the text extraction for the Querido Diário project.",
                text,
                msg="Extracted text does not have the expected string",
            )
