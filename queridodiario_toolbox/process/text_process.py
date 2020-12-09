from subprocess import check_output, DEVNULL
import re
import string


def remove_breaks(text) -> str:
    """
        Remove breaks, multiple whitespaces (including trimming leading
        and trailing spaces), and return single text.
    """
    text = re.sub(r'(\w)-(\n|\r){1,2}(\w)', r'\1\2', text)
    text = re.sub(r'(\n|\r| ){1,}', ' ', text)
    text = re.sub(r'(^ | $)', '', text)
    return text


def remove_duplicate_punctuation(text) -> str:
    """
        Remove duplicate punctuation, which may have been a feature of
        gazette design.
    """
    pattern = f'([{string.punctuation}])' + '{1,}'
    pattern = re.compile(pattern)
    text = re.sub(pattern, r'\1', text)
    return text


def execute_tabula_on_page(filepath, tabula_jar) -> str:
    """
        Extract table and text from page
    """
    command = ["java", "-jar", TABULA_PATH, filepath]
    page = check_output(command, stderr=DEVNULL)
    page = page.decode('utf-8')
    return page


def extract_table(page, first_word, last_word) -> str:
    """
        Slice table text and return it.
    """
    pattern = re.compile(f'{first_word}(.|\n)*{last_word}')
    table = re.search(pattern, page)
    if table:
        table = table.group(0)
        return table

