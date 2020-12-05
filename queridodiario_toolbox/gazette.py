from typing import Optional
import configparser
import json
import os

from .etl.file_transform import *

class Gazette:
    """
        The Gazette class contains the methods to process all gazette
        editions downloaded in project querido diário.

        Args:
            filepath: a gazette edition to process or read. it takes
                      precedence over content if both are specified.
            apache_tika_jar: a filepath pointing to the apache tika
                             installation.
            content: a processed content

    """
    def __init__(
            self, filepath: Optional[str]=None,
            apache_tika_jar: Optional[str]=None, content: Optional[str]=None
        ):

        self.filepath = filepath
        self.tika_jar = apache_tika_jar
        self.content = content

        if self.filepath:
            check_file_type_supported(self.filepath)
            if not is_txt(self.filepath):
                check_apache_tika_jar_is_valid(self.tika_jar)
        else:
            if not self.content:
                raise Exception(
                    "Either the filepath or content argument must be specified"
                )

    def extract_content(self, metadata: Optional[bool]=False) -> None:
        """
            Extract gazette content, save to disk, and store filepath
            in filepath class content
        """
        self.filepath = write_file_content(
            filepath=self.filepath, apache_tika_jar=self.tika_jar,
            metadata=metadata
        )

    def load_content(self) -> None:
        """
            Load gazette content and store in content class object
        """
        self.content = load_file_content(filepath=self.filepath)

    def process_text(self) -> str:
        """
            Process gazette text and return linearized text
        """
        pass
