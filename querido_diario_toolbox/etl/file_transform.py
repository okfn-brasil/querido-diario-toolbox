import codecs
import json
import logging
import os
import subprocess
from typing import List, Optional

import magic


def check_file_exists(filepath: str) -> None:
    """
    Check if the file exists.
    """
    if not os.path.exists(filepath):
        raise Exception(f"File does not exist: {filepath}")


def check_file_type_supported(filepath: str) -> None:
    """
    Check if Apache Tika can convert this type of file
    """
    file_supported = any(
        (
            is_doc(filepath),
            is_html(filepath),
            is_pdf(filepath),
            is_txt(filepath),
            is_rtf(filepath),
            is_png(filepath),
            is_tiff(filepath),
            is_jpeg(filepath),
        )
    )

    if not file_supported:
        raise Exception(f'Unsupported file type: "{get_file_type(filepath)}"')


def check_is_jar_file(filepath: str) -> None:
    """
    Check if the given file is a jar file.
    """
    if not is_jar(filepath):
        raise Exception(
            f"Expected Apache Tika jar file but instead "
            f'received "{get_file_type(filepath)}"'
        )


def check_apache_tika_jar_is_valid(apache_tika_jar: str) -> None:
    """
    Verify if the given file is a valid Apache Tika jar file used to
    extract the text from files.
    """
    check_file_exists(apache_tika_jar)
    check_is_jar_file(apache_tika_jar)


def check_file_to_extract_text_is_valid(filepath: str) -> None:
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
        f"application/{ext}"
        for ext in [
            "msword",
            "vnd.oasis.opendocument.text",
            "vnd.openxmlformats-officedocument.wordprocessingml.document",
            "octet-stream",
        ]
    ]
    return is_file_type(filepath, file_types)


def is_html(filepath: str) -> bool:
    """
    If the file type is html, return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["text/html"])


def is_json(filepath: str) -> bool:
    """
    If the file type is html, return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["application/json"]) or (
        is_txt(filepath) and has_suffix_in_name(filepath, "json")
    )


def has_suffix_in_name(filepath: str, suffix: str) -> bool:
    """
    Check if the given file path has the given suffix (file extension).
    """
    return filepath.endswith(suffix)


def is_jar(filepath: str) -> bool:
    """
    If the file type is jar, return True. Otherwise, return False.
    """
    return is_file_type(
        filepath, file_types=["application/java-archive", "application/zip"]
    )


def is_jpeg(filepath: str) -> bool:
    """
    If the file type is jpeg, return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["image/jpeg"])


def is_pdf(filepath: str) -> bool:
    """
    If the file type is pdf, return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["application/pdf"])


def is_png(filepath: str) -> bool:
    """
    If the file type is png, return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["image/png"])


def is_rtf(filepath: str) -> bool:
    """
    If the file type is rtf, return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["application/rtf", "text/rtf"])


def is_tiff(filepath: str) -> bool:
    """
    If the file type is tiff, return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["image/tiff"])


def is_txt(filepath: str) -> bool:
    """
    If the file type is txt return True. Otherwise, return False.
    """
    return is_file_type(filepath, file_types=["text/plain", "text/x-Algol68"])


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


def write_file_content(
    filepath: str, apache_tika_jar: str, metadata: Optional[bool] = False
) -> str:
    """
    Extract the metadata of the original file using the given Apache
    Tika jar file. Write text file and return its filepath.
    """
    check_file_to_extract_text_is_valid(filepath)
    check_apache_tika_jar_is_valid(apache_tika_jar)

    path_src, _ = os.path.splitext(filepath)
    command = f'java -jar "{apache_tika_jar}" --encoding=UTF-8'

    if is_txt(filepath):
        return filepath
    else:
        if metadata:
            command += f' --metadata --json "{filepath}"'
            path_dest = path_src + ".json"
        else:
            command += f' --text "{filepath}"'
            path_dest = path_src + ".txt"

        logging.debug(command)

        with open(path_dest, "w") as f:
            subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=f,
                stderr=subprocess.DEVNULL,
            )
        return path_dest


def load_file_content(filepath: str) -> str:
    """
    Load content from file
    """
    if is_json(filepath):
        logging.debug(f"{filepath} is json")
        with open(filepath, "r") as fp:
            content = json.load(fp)
        return content
    elif is_txt(filepath):
        logging.debug(f"{filepath} is text")
        try:
            with codecs.open(filepath) as fp:
                content = fp.read()
            return content
        except UnicodeError:
            with codecs.open(filepath, encoding="cp1252") as fp:
                content = fp.read()
            return content
        except Exception as e:
            logging.error(e)
            print(e)
    else:
        raise Exception(
            (
                f'Expected "text/plain" file type but instead '
                f'received "{get_file_type(filepath)}"'
            )
        )
