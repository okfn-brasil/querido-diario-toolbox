from typing import Optional, Sequence

from .etl.file_transform import *
from .process.edition_process import *
from .process.text_process import *


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
        self.content_file = None
        self.metadata_file = None
        self.metadata = None

        if self.filepath:
            check_file_type_supported(self.filepath)
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
        if isinstance(self.content, dict):
            raise TypeError("str expected, not dict")
        else:
            text = remove_breaks(self.content)
            text = remove_duplicate_punctuation(text)
            if store_text:
                self.content = text
            else:
                return text

    @staticmethod
    def scan_cpf(text, validate: Optional[bool] = False) -> Sequence[str]:
        """
            Scan for cpfs and validate cpfs them if required by user.
        """
        cpfs = scan_individual_identifiers(text)

        if validate:
            cpfs = [
                cpf for cpf in cpfs if validate_individual_identifiers(cpf)
            ]

        if cpfs:
            return set(cpfs)

    @staticmethod
    def scan_cnpj(text, validate: Optional[bool] = False) -> Sequence[str]:
        """
            Scan for cnpjs and validate cpfs them if required by user.
        """
        cnpjs = scan_individual_identifiers(text, cpf=False)

        if validate:
            cnpjs = [
                cnpj
                for cnpj in cnpjs
                if validate_individual_identifiers(cnpj, cpf=False)
            ]

        if cnpjs:
            return set(cnpjs)
