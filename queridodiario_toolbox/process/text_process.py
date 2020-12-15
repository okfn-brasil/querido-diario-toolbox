from subprocess import check_output, DEVNULL
import re
import string


def remove_breaks(text: str) -> str:
    """
        Remove breaks, multiple whitespaces (including trimming leading
        and trailing spaces), and return single text.
    """
    text = re.sub(r"(\w)-(\n|\r){1,2}(\w)", r"\1\2", text)
    text = re.sub(r"(\n|\r|\t| ){1,}", " ", text)
    text = re.sub(r"(^ | $)", "", text)
    return text


def remove_duplicate_punctuation(text: str) -> str:
    """
        Remove duplicate punctuation, which may have been a feature of
        gazette design.
    """
    pattern = f"([{string.punctuation}])" + "{1,}"
    pattern = re.compile(pattern)
    text = re.sub(pattern, r"\1", text)
    return text


def execute_tabula(
    filepath: str, tabula_jar: str, *args: str, **kwargs: str
) -> str:
    """
        Extract table and text from gazette. pass additional args to
        tabula following its documentation
    """
    command = ["java", "-jar", tabula_jar, filepath]

    if args:
        for arg in args:
            command.extend([arg])

    if kwargs:
        for k, v in kwargs.items():
            command.extend([k, v])

    page = check_output(command, stderr=DEVNULL)
    page = page.decode("utf-8")
    return page
