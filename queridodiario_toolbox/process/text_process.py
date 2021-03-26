from subprocess import check_output, DEVNULL
import re
import string


def _remove_breaks(text: str) -> str:
    """
    Remove breaks, multiple whitespaces (including trimming leading
    and trailing spaces), and return single text.
    """
    text = _remove_new_line_splitting_word(text)
    text = _remove_repeating_whitespaces_and_new_lines(text)
    text = _remove_whitespaces_beginning_end_text(text)
    return text


def _remove_new_line_splitting_word(text: str) -> str:
    """
    Removes new lines splitting words.
    """
    return re.sub(r"(\w)-(\n|\r){1,2}(\w)", r"\1\3", text)


def _remove_repeating_whitespaces_and_new_lines(text: str) -> str:
    """
    Removes repeating new lines and tabular char.
    """
    return re.sub(r"(\n|\r|\t| ){1,}", " ", text)


def _remove_whitespaces_beginning_end_text(text: str) -> str:
    """
    Removes whitespace from the beginning and end of the given text.
    """
    return text.strip()


def _remove_duplicate_punctuation(text: str) -> str:
    """
    Remove duplicate punctuation, which may have been a feature of
    gazette design.
    """
    pattern = f"([{string.punctuation}])" + "{1,}"
    pattern = re.compile(pattern)
    text = re.sub(pattern, r"\1", text)
    return text


def process_text(text) -> str:
    """
    Process gazette text and return linearized text
    """
    text = _remove_breaks(text)
    text = _remove_duplicate_punctuation(text)
    return text
