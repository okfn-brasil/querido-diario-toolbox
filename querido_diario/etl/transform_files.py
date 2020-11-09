from typing import List
import codecs
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
        Check if Apache Tika can convert this type of file
    """
    if not is_doc(filepath) and not is_pdf(filepath) and not is_txt(filepath):
        raise Exception(f"Unsupported file type: {get_file_type(filepath)}")


def check_is_jar_file(filepath: str) -> None:
    """
        Check if the given file is a jar file.
    """
    if not is_jar(filepath):
        raise Exception(
            f"Expected Apache Tika jar file {get_file_type(filepath)}"
        )


def check_is_valid_apache_tika_jar(apache_tika_jar: str) -> None:
    """
        Verify if the given file is a valid Apache Tika jar file used to
        extract the text from files.
    """
    check_file_exists(apache_tika_jar)
    check_is_jar_file(apache_tika_jar)


def check_is_valid_file_to_extract_text(filepath: str) -> None:
    """
        Verify if the given file is a valid file to extract the text from.
    """
    check_file_exists(filepath)
    check_file_type_supported(filepath)


def is_doc(filepath: str) -> bool:
    """
        If the file type is doc or similar, return True. Otherwise,
        return False.
    """
    file_types = [
        "application/msword",
        "application/vnd.oasis.opendocument.text",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    return is_file_type(filepath, file_types)


def is_jar(filepath: str) -> bool:
    """
        If the file type is jar, return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["application/java-archive"])


def is_pdf(filepath: str) -> bool:
    """
        If the file type is pdf, return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["application/pdf"])


def is_txt(filepath: str) -> bool:
    """
        If the file type is txt return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["text/plain"])


def get_file_type(filepath: str) -> str:
    """
        Return the file type
    """
    filetype = magic.from_file(filepath, mime=True)
    logging.debug(f"{filepath}: {filetype}")
    return magic.from_file(filepath, mime=True)


def is_file_type(filepath: str, file_types: List[str]) -> bool:
    """
        Generic method to check if an identified file type matches a
        given list of types
    """
    return get_file_type(filepath) in file_types


def write_metadata(filepath: str, apache_tika_jar: str) -> str:
    """
        Extract the metadata of the original file using the given Apache
        Tika jar file. Write text file and return its filepath.
    """
    if is_txt(filepath):
        return filepath
    else:
        src_path, _ = os.path.splitext(filepath)
        dest_path = src_path + ".json"
        command = f"java -jar {apache_tika_jar} --metadata --json {filepath}"
        logging.debug(command)
        with open(dest_path, "w") as f:
            subprocess.run(command, shell=True, check=True, stdout=f)
        return dest_path

def write_text(filepath: str, apache_tika_jar: str) -> str:
    """
        Extract the text from the given file using the given Apache Tika
        jar file. Write text file and return its filepath
    """
    logging.debug(f"Extracting text from {filepath}")
    if is_txt(filepath):
        return filepath
    else:
        dest_path, _ = os.path.splitext(filepath)
        dest_path = dest_path + ".txt"
        command = f"java -jar {apache_tika_jar} --text {filepath}"
        logging.debug(command)
        with open(dest_path, "w") as f:
            subprocess.run(command, shell=True, check=True, stdout=f)
        return dest_path


def get_content_from_file(filepath: str) -> str:
    """
        Load content from file
    """
    try:
        with codecs.open(filepath, encoding='utf-8') as fp:
            content = fp.read()
    except:
        with codecs.open(filepath, encoding='cp-1252') as fp:
            content = fp.read()
    return content
