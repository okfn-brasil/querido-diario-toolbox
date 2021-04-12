from typing import Optional, Sequence

from .etl.file_transform import check_file_type_supported, is_txt, is_json
from .etl.text_extractor import create_text_extractor
from .process.information_retrieve import scan_cpf, scan_cnpj
from .process.text_process import process_text


class Gazette:

    """
    The Gazette class contains the methods to process all gazette
    editions downloaded in project querido diário.

    Args:
        config:         a config file to find your extraction
                        method.
        gazette_path:   a gazette edition to process or read. it
                        takes precedence over content if both are
                        specified.
    """

    def __init__(self, config, gazette_path: Optional[str]=None):
        self.extractor = create_text_extractor(config)
        self.gazette_path = gazette_path

        if self.gazette_path:
            check_file_type_supported(self.gazette_path)
        else:
            self.gazette_path = None

    def extract_content(self) -> None:
        """
        Extract gazette content, save to disk, and store filepath
        in filepath class content
        """
        if self.gazette_path:
            self.extractor.extract_content(self.gazette_path)
            self.content_path = self.extractor.content_path
        else:
            raise Exception("You must pass a path to a gazette file.")

    def load_content(self) -> None:
        """
        Load gazette content and store in content class object
        """
        if is_txt(self.content_path):
            self.extractor.load_content(self.content_path)
            self.content = self.extractor.content
        else:
            raise Exception("You must pass a path to a gazette content file.")

    def extract_metadata(self) -> None:
        """
        Extract gazette metadata, save to disk, and store filepath
        in filepath class method
        """
        if self.gazette_path:
            self.extractor.extract_metadata(self.gazette_path)
            self.metadata_path = self.extractor.metadata_path
        else:
            raise Exception("You must pass a path to a gazette file.")

    def load_metadata(self) -> None:
        """
        Extract gazette metadata, save to disk, and store filepath
        in filepath class method
        """
        if is_json(self.metadata_path):
            self.extractor.load_metadata(self.metadata_path)
            self.metadata = self.extractor.metadata
        else:
            raise Exception("You must pass a path to a gazette metadata file.")

    def process_text(self) -> None:
        """
        Process gazette text and return linearized text
        """
        self.content = process_text(self.content)

    def scan_cpf(self, validate: Optional[bool]=True) -> Sequence[str]:
        """
        Scan for cpfs and validate cpfs them if required by user.
        """
        return scan_cpf(self.content, validate)

    def scan_cnpj(self, validate: Optional[bool]=True) -> Sequence[str]:
        """
        Scan for cnpjs and validate cpfs them if required by user.
        """
        return scan_cnpj(self.content, validate)
