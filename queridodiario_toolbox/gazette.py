from typing import Optional, Sequence

from .etl.file_transform import *
from .process.text_process import *
from .process.edition_process import *


class Gazette:
    """
        The Gazette class contains the methods to process all gazette
        editions downloaded in project querido diário.

        Args:
            filepath:        a gazette edition to process or read. it
                             takes precedence over content if both are
                             specified.
            apache_tika_jar: a filepath pointing to the apache tika
                             installation.
            content:         a processed content.

    """

    def __init__(
        self,
        filepath: Optional[str] = None,
        apache_tika_jar: Optional[str] = None,
        content: Optional[str] = None,
    ):

        self.filepath = filepath
        self.tika_jar = apache_tika_jar
        self.content = content
        self.store_text = False

        if self.filepath:
            check_file_type_supported(self.filepath)
            if not is_txt(self.filepath):
                check_apache_tika_jar_is_valid(self.tika_jar)
        else:
            if not self.content:
                raise Exception(
                    "Either the filepath or content argument must be specified"
                )

    def extract_content(self, metadata: Optional[bool] = False) -> None:
        """
            Extract gazette content, save to disk, and store filepath
            in filepath class content
        """
        self.filepath = write_file_content(
            filepath=self.filepath,
            apache_tika_jar=self.tika_jar,
            metadata=metadata,
        )

    def load_content(self) -> None:
        """
            Load gazette content and store in content class object
        """
        self.content = load_file_content(filepath=self.filepath)

    def process_text(self, store_text: Optional[bool] = False) -> str:
        """
            Process gazette text and return linearized text
        """
        self.store_text = store_text

        if isinstance(self.content, dict):
            raise TypeError("str expected, not dict")
        else:
            text = remove_breaks(self.content)
            text = remove_duplicate_punctuation(text)
            if self.store_text:
                self.content = text
            else:
                return text

    def scan_cpf(
        self, text: Optional[str] = None, validate: Optional[bool] = False
    ) -> Sequence[str]:
        """
            Scan for cpfs and validate cpfs them if required by user.
        """
        if self.store_text:
            cpfs = scan_individual_identifiers(self.content)
        elif not self.store_text and not text:
            raise Exception("You need to provide a string to scan for CPF.")
        else:
            cpfs = scan_individual_identifiers(text)

        if validate:
            cpfs = [
                cpf for cpf in cpfs if validate_individual_identifiers(cpf)
            ]

        if cpfs:
            return set(cpfs)

    def scan_cnpj(
        self, text: Optional[str] = None, validate: Optional[bool] = False
    ) -> Sequence[str]:
        """
            Scan for cnpjs and validate cpfs them if required by user.
        """
        if self.store_text:
            cnpjs = scan_individual_identifiers(self.content, cpf=False)
        elif not self.store_text and not text:
            raise Exception("You need to provide a string to scan for CNPJ.")
        else:
            cnpjs = scan_individual_identifiers(text, cpf=False)

        if validate:
            cnpjs = [
                cnpj
                for cnpj in cnpjs
                if validate_individual_identifiers(cnpj, cpf=False)
            ]

        if cnpjs:
            return set(cnpjs)
