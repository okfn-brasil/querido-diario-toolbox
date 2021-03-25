from typing import Optional, Sequence

from .etl.file_transform import *
from .process.edition_process import *
from .process.text_process import *
from .etl.text_extractor import create_text_extractor

class Gazette:
    """
        The Gazette class contains the methods to process all gazette
        editions downloaded in project querido diário.

        Args:
            config:          a config file to find your extraction
                             method.
            filepath:        a gazette edition to process or read. it
                             takes precedence over content if both are
                             specified.
    """

    def __init__(self, config, gazette_path):

        self.extractor = create_text_extractor(config)

        self.gazette_path = gazette_path
        self.content_path = None
        self.content = None
        self.metadata_path = None
        self.metadata = None

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
