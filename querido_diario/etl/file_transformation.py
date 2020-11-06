from typing import List
import logging
import magic
import os
import subprocess


def check_file_exists(filepath: str) -> None:
    """
    Check if the file exists.
    """
    if not os.path.exists(filepath):
        raise Exception(f"File does not exists: {filepath}")


def check_file_type_supported(filepath: str) -> None:
    """
    Check if the given file is of a type supported to get the text extracted from
    """
    if not is_doc(filepath) and not is_pdf(filepath) and not is_txt(filepath):
        raise Exception("Unsupported file type: " + get_file_type(filepath))


def extract_text(filepath: str, apache_tika_jar: str) -> str:
    """
    Extract the text from the given file using the given Apache Tika jar file.

    The text will be write to a text file in disk and the filepath to it will be returned
    """
    logging.debug(f"Extracting text from {filepath}")
    if is_txt(filepath):
        return filepath
    text_path = filepath + ".txt"
    command = f"java -jar {apache_tika_jar} --text {filepath}"
    logging.debug(command)
    with open(text_path, "w") as f:
        subprocess.run(command, shell=True, check=True, stdout=f)
    return text_path


def check_is_jar_file(filepath: str) -> None:
    """
    Check if the given file is a jar file.
    """
    if not is_jar(filepath):
        raise Exception("Expected Apache Tika jar file" + get_file_type(filepath))


def check_is_valid_apache_tika_jar(apache_tika_jar: str) -> None:
    """
    Verify if the given file is a valid Apache Tika jar file used to extract the text from files.
    """
    check_file_exists(apache_tika_jar)
    check_is_jar_file(apache_tika_jar)


def check_is_valid_file_to_extract_text(filepath: str) -> None:
    """
    Verify if the given file is a valid file to extract the text from.
    """
    check_file_exists(filepath)
    check_file_type_supported(filepath)


def get_text_from_file(filepath: str, apache_tika_jar: str) -> str:
    check_is_valid_file_to_extract_text(filepath)
    check_is_valid_apache_tika_jar(apache_tika_jar)
    return extract_text(filepath, apache_tika_jar)


def is_jar(filepath: str) -> bool:
    """
    If the file type is jar returns True. Otherwise, returns False.
    """
    return is_file_type(filepath, file_types=["application/java-archive"])


def is_pdf(filepath: str) -> bool:
    """
    If the file type is pdf returns True. Otherwise,
    returns False
    """
    return is_file_type(filepath, file_types=["application/pdf"])


def is_doc(filepath: str) -> bool:
    """
    If the file type is doc or similar returns True. Otherwise,
    returns False
    """
    file_types = [
        "application/msword",
        "application/vnd.oasis.opendocument.text",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    return is_file_type(filepath, file_types)


def is_txt(filepath: str) -> bool:
    """
    If the file type is txt returns True. Otherwise,
    returns False
    """
    return is_file_type(filepath, file_types=["text/plain"])


def get_file_type(filepath: str) -> str:
    """
    Returns the file's type
    """
    filetype = magic.from_file(filepath, mime=True)
    logging.debug(f"{filepath}: {filetype}")
    return magic.from_file(filepath, mime=True)


def is_file_type(filepath: str, file_types: List[str]) -> bool:
    """
    Generic method to check if a identified file type matches a given list of types
    """
    return get_file_type(filepath) in file_types
