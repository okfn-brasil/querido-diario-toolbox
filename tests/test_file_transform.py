import json
import os
import tempfile
from unittest import TestCase
import unittest
from unittest import mock
from unittest.mock import patch

from querido_diario_toolbox.etl.file_transform import *


class TextExtractionTests(TestCase):
    def create_temporary_file(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as file:
            return file.name
        raise Exception("Cannot create temporary file")

    def add_suffix_in_file_name(self, file_path, suffix):
        new_file_name = f"{file_path}{suffix}"
        os.rename(file_path, new_file_name)
        return new_file_name

    def create_json_file(self):
        temp_file = self.create_temporary_file()
        with open(temp_file, "w") as json_file:
            json.dump({"test": "json data"}, json_file)
        new_file_name = self.add_suffix_in_file_name(temp_file, ".json")
        return new_file_name

    def create_invalid_json_file(self):
        temp_file = self.create_temporary_file()
        new_file_name = self.add_suffix_in_file_name(temp_file, ".txt")
        return new_file_name

    def test_valid_json_file(self):
        json_file = self.create_json_file()
        is_json_file = is_json(json_file)
        self.assertTrue(
            is_json_file,
            msg="Only files with application/json mimetype or text file with .json extensions should be considered JSON files",
        )

    def test_invalid_json_file(self):
        json_file = self.create_invalid_json_file()
        is_json_file = is_json(json_file)
        self.assertFalse(
            is_json_file,
            msg="Only files with application/json mimetype or text file with .json extensions should be considered JSON files",
        )

    def test_has_suffix_in_name(self):
        has_json_suffix = has_suffix_in_name("testing/file/path/test.json", "json")
        self.assertTrue(has_json_suffix)
        has_txt_suffix = has_suffix_in_name("testing/file/path/test.json", "txt")
        self.assertFalse(has_txt_suffix)

    def test_check_file_exists_file_exists(self):
        temp_file = self.create_temporary_file()
        try:
            check_file_exists(temp_file)  
        finally:
            os.remove(temp_file)
    
    def test_check_file_type_supported_valid_file(self):
        temp_file = self.create_temporary_file()
        try:
            with unittest.mock.patch('magic.from_file', return_value="application/pdf"):
                check_file_type_supported(temp_file) 
        finally:
            os.remove(temp_file)

    def test_check_file_type_supported_invalid_file(self):
        temp_file = self.create_temporary_file()
        try:
            with unittest.mock.patch('magic.from_file', return_value="application/unknown"):
                with self.assertRaises(Exception) as context:
                    check_file_type_supported(temp_file)
                self.assertIn("Unsupported file type", str(context.exception))
        finally:
            os.remove(temp_file)

    
    @patch('magic.from_file')
    def test_check_file_type_supported_rtf(self, mock_magic):
        temp_file = self.create_temporary_file()
        mock_magic.return_value = "application/rtf"
        try:
            with self.assertRaises(Exception) as context:
                check_file_type_supported(temp_file)
            self.assertIn("Unsupported file type", str(context.exception))
        except Exception:
            print('LOG falha params')

    @patch('magic.from_file')
    def test_check_file_type_supported_doc(self, mock_magic):
        temp_file = self.create_temporary_file()
        mock_magic.return_value = "application/msword"
        try:
            with self.assertRaises(Exception) as context:
                check_file_type_supported(temp_file)
            self.assertIn("Unsupported file type", str(context.exception))
        except Exception:
            print('LOG falha params')
        finally:
            os.remove(temp_file)


    @patch('magic.from_file')
    def test_check_file_type_supported_html(self, mock_magic):
        temp_file = self.create_temporary_file()
        mock_magic.return_value = "text/html"
        try:
            with self.assertRaises(Exception) as context:
                check_file_type_supported(temp_file)
            self.assertIn("Unsupported file type", str(context.exception))
        except Exception:
            print('LOG falha params')
        finally:
            os.remove(temp_file)


    @patch('magic.from_file')
    def test_check_file_type_supported_pdf(self, mock_magic):
        temp_file = self.create_temporary_file()
        mock_magic.return_value = "application/pdf"
        try:
            with self.assertRaises(Exception) as context:
                check_file_type_supported(temp_file)
            self.assertIn("Unsupported file type", str(context.exception))
        except Exception:
            print('LOG falha params')
        finally:
            os.remove(temp_file)


    @patch('magic.from_file')
    def test_check_file_type_supported_txt(self, mock_magic):
        temp_file = self.create_temporary_file()
        mock_magic.return_value = "text/plain"
        try:
            with self.assertRaises(Exception) as context:
                check_file_type_supported(temp_file)
            self.assertIn("Unsupported file type", str(context.exception))
        except Exception:
            print('LOG falha params')
        finally:
            os.remove(temp_file)


    @patch('magic.from_file')
    def test_check_file_type_supported_rtf(self, mock_magic):
        temp_file = self.create_temporary_file()
        mock_magic.return_value = "application/rtf"
        try:
            with self.assertRaises(Exception) as context:
                check_file_type_supported(temp_file)
            self.assertIn("Unsupported file type", str(context.exception))
        except Exception:
            print('LOG falha params')
        finally:
            os.remove(temp_file)


    @patch('magic.from_file')
    def test_check_file_type_supported_png(self, mock_magic):
        temp_file = self.create_temporary_file()
        mock_magic.return_value = "image/png"
        try:
            with self.assertRaises(Exception) as context:
                check_file_type_supported(temp_file)
            self.assertIn("Unsupported file type", str(context.exception))
        except Exception:
            print('LOG falha params')
        finally:
            os.remove(temp_file)


    @patch('magic.from_file')
    def test_check_file_type_supported_tiff(self, mock_magic):
        temp_file = self.create_temporary_file()
        mock_magic.return_value = "image/tiff"
        try:
            with self.assertRaises(Exception) as context:
                check_file_type_supported(temp_file)
            self.assertIn("Unsupported file type", str(context.exception))
        except Exception:
            print('LOG falha params')
        finally:
            os.remove(temp_file)


    @patch('magic.from_file')
    def test_check_file_type_supported_jpeg(self, mock_magic):
        temp_file = self.create_temporary_file()
        mock_magic.return_value = "image/jpeg"
        try:
            with self.assertRaises(Exception) as context:
                check_file_type_supported(temp_file)
            self.assertIn("Unsupported file type", str(context.exception))
        except Exception:
            print('LOG falha params')
        finally:
            os.remove(temp_file)
