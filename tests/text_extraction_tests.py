from unittest import TestCase
import os

from process.etl.file_transform import *
from process import Gazette

class TextExtractionTests(TestCase):

    # APACHE_TIKA_JAR_PATH = "/tika-app.jar"
    TIKA_PATH = "/usr/local/Cellar/tika/1.24.1_1/libexec/tika-app-1.24.1.jar"

    def tearDown(self):
        self.clean_txt_file_generated_during_tests()

    def clean_txt_file_generated_during_tests(self):
        for root, dirs, files in os.walk("tests/data/"):
            for generated_file in self.get_files_generated_during_tests(
                root, files
            ):
                print(f"{generated_file}")
                os.remove(generated_file)

    def get_files_generated_during_tests(self, root, files):
        for f in files:
            if ".txt" in f and f not in ["fake_content.txt", "fake_gazette.txt"]:
                yield f"{root}{f}"

    def test_extract_text_from_invalid_file(self):
        with self.assertRaisesRegex(Exception, "No such file"):
            gazette = Gazette("file/does/not/exist", self.TIKA_PATH)
            gazette.extract_content()

    def test_extract_metadata_from_invalid_file(self):
        with self.assertRaisesRegex(Exception, "No such file"):
            gazette = Gazette("file/does/not/exist", self.TIKA_PATH)
            gazette.extract_content(metadata=True)

    def test_extract_text_using_invalid_apache_tika_jar_path(self):
        with self.assertRaisesRegex(Exception, "File does not exist"):
            gazette = Gazette("tests/data/fake_gazette.pdf", "/tika/path")
            gazette.extract_content()

    def test_extract_metadata_using_invalid_apache_tika_jar_path(self):
        with self.assertRaisesRegex(Exception, "File does not exist"):
            gazette = Gazette("tests/data/fake_gazette.pdf", "/tika/path")
            gazette.extract_content(metadata=True)

    def test_extract_text_using_invalid_file_type_apache_tika(self):
        with self.assertRaisesRegex(Exception, "Expected Apache Tika jar"):
            gazette = Gazette(
                "tests/data/fake_gazette.pdf", "tests/data/fake_gazette.pdf"
            )
            gazette.extract_content(metadata=True)

    def test_extract_metadata_using_invalid_file_type_apache_tika(self):
        with self.assertRaisesRegex(Exception, "Expected Apache Tika jar"):
            gazette = Gazette(
                "tests/data/fake_gazette.pdf", "tests/data/fake_gazette.pdf",
            )
            gazette.extract_content(metadata=True)

    def test_extract_text_from_invalid_file_type_should_fail(self):
        with self.assertRaisesRegex(Exception, "Unsupported file type"):
            gazette = Gazette("tests/data/fake_gazette.m4a", self.TIKA_PATH)
            gazette.extract_content()

    def test_extract_metadata_from_invalid_file_type_should_fail(self):
        with self.assertRaisesRegex(Exception, "Unsupported file type"):
            gazette = Gazette("tests/data/fake_gazette.m4a", self.TIKA_PATH)
            gazette.extract_content(metadata=True)

    def test_empty_class_instantiation_should_fail(self):
        with self.assertRaises(Exception):
            Gazette()

    def test_class_instantiation_with_filepath_but_no_tika_path(self):
        with self.assertRaises(Exception):
            gazette = Gazette(filepath="tests/data/fake_gazette.pdf")

    def test_class_instantiation_with_tika_path_but_no_filepath(self):
        with self.assertRaises(Exception):
            gazette = Gazette(apache_tika_jar=self.TIKA_PATH)

    def test_class_instantiation_with_content(self):
        gazette = Gazette(content="tests/data/fake_gazette.txt")
        self.assertNotEqual(gazette.content, None)

    def test_class_instantiation_with_no_content(self):
        gazette = Gazette(
            filepath="tests/data/fake_gazette.pdf",
            apache_tika_jar=self.TIKA_PATH
        )
        self.assertNotEqual(gazette.filepath, None)
        self.assertNotEqual(gazette.tika_jar, None)
        self.assertEqual(gazette.content, None)

    def test_class_instantiation_with_no_filepath(self):
        gazette = Gazette(
            apache_tika_jar=self.TIKA_PATH,
            content="tests/data/fake_gazette.txt"
        )
        self.assertEqual(gazette.filepath, None)
        self.assertNotEqual(gazette.tika_jar, None)
        self.assertNotEqual(gazette.content, None)

    def test_class_instantiation_with_all_arguments(self):
        gazette = Gazette(
            filepath="tests/data/fake_gazette.pdf",
            apache_tika_jar=self.TIKA_PATH,
            content="tests/data/fake_gazette.txt"
        )
        self.assertNotEqual(gazette.filepath, None)
        self.assertNotEqual(gazette.tika_jar, None)
        self.assertNotEqual(gazette.content, None)


    def test_extract_text_from_doc_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.doc", self.TIKA_PATH)

        gazette.extract_content()
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.txt")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))
        self.assertIn("Querido", gazette.content, "Extraction Failed")

    def test_extract_text_from_docx_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.docx", self.TIKA_PATH)

        gazette.extract_content()
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.txt")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))
        self.assertIn("Querido", gazette.content, "Extraction Failed")

    def test_extract_text_from_odt_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.odt", self.TIKA_PATH)

        gazette.extract_content()
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.txt")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))
        self.assertIn("Querido", gazette.content, "Extraction Failed")

    def test_extract_text_from_html_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.html", self.TIKA_PATH)

        gazette.extract_content()
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.txt")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))
        self.assertIn("Querido", gazette.content, "Extraction Failed")

    def test_extract_text_from_pdf_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.pdf", self.TIKA_PATH)

        gazette.extract_content()
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.txt")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))
        self.assertIn("Querido", gazette.content, "Extraction Failed")

    def test_extract_text_from_jpeg_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.jpeg", self.TIKA_PATH)

        gazette.extract_content()
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.txt")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))
        self.assertIn("Querido", gazette.content, "Extraction Failed")

    def test_extract_text_from_png_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.png", self.TIKA_PATH)

        gazette.extract_content()
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.txt")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))
        self.assertIn("Querido", gazette.content, "Extraction Failed")

    def test_extract_text_from_tiff_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.tiff", self.TIKA_PATH)

        gazette.extract_content()
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.txt")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))
        self.assertIn("Querido", gazette.content, "Extraction Failed")

    def test_extract_metadata_from_doc_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.doc", self.TIKA_PATH)

        gazette.extract_content(metadata=True)
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.json")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))

    def test_extract_metadata_from_docx_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.docx", self.TIKA_PATH)

        gazette.extract_content(metadata=True)
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.json")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))

    def test_extract_metadata_from_odt_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.odt", self.TIKA_PATH)

        gazette.extract_content(metadata=True)
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.json")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))

    def test_extract_metadata_from_html_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.html", self.TIKA_PATH)

        gazette.extract_content(metadata=True)
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.json")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))

    def test_extract_metadata_from_pdf_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.pdf", self.TIKA_PATH)

        gazette.extract_content(metadata=True)
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.json")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))

    def test_extract_metadata_from_jpeg_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.jpeg", self.TIKA_PATH)

        gazette.extract_content(metadata=True)
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.json")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))

    def test_extract_metadata_from_png_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.png", self.TIKA_PATH)

        gazette.extract_content(metadata=True)
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.json")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))

    def test_extract_metadata_from_tiff_should_return_content(self):
        gazette = Gazette("tests/data/fake_gazette.tiff", self.TIKA_PATH)

        gazette.extract_content(metadata=True)
        self.assertEqual(gazette.filepath, "tests/data/fake_gazette.json")

        gazette.load_content()
        self.assertNotEqual(0, len(gazette.content))


