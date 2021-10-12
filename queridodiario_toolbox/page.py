from typing import Optional

from .etl.file_transform import is_pdf
from .gazette import Gazette
from .process.text_process import execute_tabula


class Page(Gazette):
    """
    The Page class augments the Gazette class methods by processing
    tables in a gazette page if there are any.

    Args:
        filepath:        a gazette edition to process or read. it
                         takes precedence over content if both are
                         specified.
        apache_tika_jar: a filepath pointing to the apache tika
                         installation.
        tabula_jar:      a filepath poiting to the tabula jar
                         installation.
        content:         a processed content.

    """

    def __init__(
        self,
        filepath: Optional[str] = None,
        apache_tika_jar: Optional[str] = None,
        tabula_jar: Optional[str] = None,
        content: Optional[str] = None,
    ):
        super(Page, self).__init__(filepath, apache_tika_jar, content)
        self.tabula_jar = tabula_jar

    def extract_table(self, *args: str, **kwargs: str) -> str:
        """
        Extract table from gazette page indicating where table
        begins and ends.
        """
        if is_pdf(self.filepath):
            if self.tabula_jar:
                table = execute_tabula(
                    filepath=self.filepath, tabula_jar=self.tabula_jar, *args, **kwargs
                )
                return table
            else:
                raise Exception("You must pass a tabula jar path")
