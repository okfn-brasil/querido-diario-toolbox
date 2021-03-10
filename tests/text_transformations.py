from unittest import TestCase

from queridodiario_toolbox.process.text_process import remove_breaks, remove_duplicate_punctuation

class TextTransformationTests(TestCase):

    def test_remove_whitspaces(self):
        with self.subTest(msg = "Remove whitespace from the beginning and end"):
            new_text = remove_breaks(" Test ")
            self.assertEqual(new_text, "Test")
            new_text = remove_breaks(" Test test ")
            self.assertEqual(new_text, "Test test")
        with self.subTest(msg = "Remove duplicate spaces between words"):
            new_text = remove_breaks("Test    test")
            self.assertEqual(new_text, "Test test")
            new_text = remove_breaks("Test   test")
            self.assertEqual(new_text, "Test test")

    def test_remove_newlines(self):
        new_text = remove_breaks("Test\nTest")
        self.assertEqual(new_text, "Test Test")
        new_text = remove_breaks("Test\rTest")
        self.assertEqual(new_text, "Test Test")
        new_text = remove_breaks("Test\tTest")
        self.assertEqual(new_text, "Test Test")
        new_text = remove_breaks("Test\r\tTest")
        self.assertEqual(new_text, "Test Test")
        new_text = remove_breaks("Test\n\nTest")
        self.assertEqual(new_text, "Test Test")
        new_text = remove_breaks("Test-\nTest")
        self.assertEqual(new_text, "TestTest")

    def test_remove_duplicate_punctuation(self):
        new_text = remove_duplicate_punctuation("Test..Test")
        self.assertEqual(new_text, "Test.Test")
