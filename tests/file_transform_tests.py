import json
import os
import tempfile
from unittest import TestCase

from querido_diario_toolbox.etl.file_transform import has_suffix_in_name, is_json


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
