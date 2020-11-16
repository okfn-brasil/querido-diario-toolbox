from typing import List
from .file_transform import *
import os

def extract_wrapper(
        filepaths: List[str], apache_tika_jar: str,
        metadata: Optional[str]=None
    ) -> List[str]:
    """
        Extract text or metadata from gazette, regardless of the file
        type of the gazette.
    """
    if isinstance(filepaths, str):
        filepaths = [filepaths]
    else:
        filepaths = filepaths

    for filepath in filepaths:
        if is_txt(filepath):
            yield get_content_from_file(filepath)
        else:
            fp = write_data(filepath, apache_tika_jar, metadata)
            yield get_content_from_file(fp)
