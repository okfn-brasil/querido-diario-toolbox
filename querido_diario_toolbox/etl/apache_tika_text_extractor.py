import json
import logging
import os
import subprocess

from querido_diario_toolbox.etl.file_transform import (
    check_file_to_extract_text_is_valid,
    is_jar,
)
from querido_diario_toolbox.etl.text_extractor_interface import TextExtractor

LOGGER = logging.getLogger(__name__)


class ApacheTikaExtractor(TextExtractor):
    def __init__(self, apache_tika_jar):
        if not is_jar(apache_tika_jar):
            raise Exception("ApacheTikaExtractor expected a jar file.")
        self.apache_tika_jar = apache_tika_jar

    def _build_apache_tika_command(self, gazette_file: str, metadata=False):
        command = [
            "java",
            "-jar",
            self.apache_tika_jar,
            "--encoding=UTF-8",
        ]
        if metadata:
            command.append("--metadata")
            command.append("--json")
            command.append(gazette_file)
        else:
            command.append("--text")
            command.append(gazette_file)
        command = " ".join(command)
        LOGGER.debug(command)
        return command

    def extract_text(self, gazette, path_dest=None):
        """
        Calls the Apache Tika command using the configured jar file to extract
        text from the given gazette. The extract text will be write back to a
        text file on disk. The path to the text file will be stored in the
        content_file member variable in the gazette object
        """
        check_file_to_extract_text_is_valid(gazette.filepath)
        command = self._build_apache_tika_command(gazette.filepath)
        path_src, _ = os.path.splitext(gazette.filepath)
        path_dest = path_dest or (path_src + ".txt")
        with open(path_dest, "w") as f:
            subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=f,
                stderr=subprocess.DEVNULL,
            )
        gazette.content_file = path_dest

    def load_content(self, gazette):
        """
        Loads the content of the content_file file into the content member
        variable in the gazette object.
        """
        with open(gazette.content_file, "r") as f:
            gazette.content = f.read()

    def extract_metadata(self, gazette, path_dest=None):
        """
        Calls the Apache Tika command using the configured jar file to extract
        metadata from the given gazette. The extracted metadata info will be
        write back to a json file on disk. The path to the json file will be
        stored in the metadata_file member variable in the gazette object.
        """
        check_file_to_extract_text_is_valid(gazette.filepath)
        command = self._build_apache_tika_command(gazette.filepath, metadata=True)
        path_src, _ = os.path.splitext(gazette.filepath)
        path_dest = path_dest or (path_src + ".json")

        with open(path_dest, "w") as f:
            subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=f,
                stderr=subprocess.DEVNULL,
            )
        gazette.metadata_file = path_dest

    def load_metadata(self, gazette):
        """
        Loads the content of the metadata_file file into the metadata member
        variable in the gazette object.
        """
        with open(gazette.metadata_file, "r") as f:
            metadata_content = f.read()
            gazette.metadata = json.loads(metadata_content)
