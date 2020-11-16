from typing import List, Optional

from .etl.file_extract import *


class Gazette:
    """
        The Gazette class contains the methods to process all gazette
        editions downloaded in project querido diário.

        Args:
            filepaths: a list of gazette editions to process or read
            apache_tika_jar: a filepath pointing to the apache tika
                             installation.
            metadata: a flag for extracting metadata rather than text

    """
    def __init__(
            self, filepaths: list, apache_tika_jar: Optional[str]=None,
            texts: Optional[str]=None
        ):

        self.filepaths = filepaths
        self.apache_tika_jar = apache_tika_jar
        self.texts = texts

    def extract_content(self, metadata: Optional[str]=None) -> List[str]:
        """ Extract gazette content and store as gazette text """
        self.texts = extract_wrapper(
            self.filepaths, self.apache_tika_jar, metadata
        )

