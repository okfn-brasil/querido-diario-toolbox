import json
import logging
import os
import requests
import subprocess
from ast import literal_eval

from queridodiario_toolbox.etl.text_extractor_interface import TextExtractor
from queridodiario_toolbox.etl.file_transform import (
    check_file_to_extract_text_is_valid,
    is_jar,
    is_url,
)

LOGGER = logging.getLogger(__name__)


class ApacheTikaExtractor(TextExtractor):
    def __init__(self, apache_tika_jar, **kwargs):
        if not is_jar(apache_tika_jar):
            raise Exception("ApacheTikaExtractor expected a jar file.")
        self.apache_tika_jar = apache_tika_jar

    def _build_apache_tika_command(self, gazette_file: str, metadata=False):
        command = [
            "java",
            "-jar",
            f'"{str(self.apache_tika_jar)}"',
            "--encoding=UTF-8",
        ]
        if metadata:
            command.append("--metadata")
            command.append("--json")
            command.append(f'"{str(gazette_file)}"')
        else:
            command.append("--text")
            command.append(f'"{str(gazette_file)}"')
        command = " ".join(command)
        LOGGER.debug(command)
        return command

    def extract_content(self, filepath):

        """
        Calls the Apache Tika command using the configured jar file
        to extract text from any given gazette. The extracted text
        will be written back to a text file on disk. The path to the
        text file will be stored in the content_file member variable
        in the gazette object
        """

        check_file_to_extract_text_is_valid(filepath)
        command = self._build_apache_tika_command(filepath)
        path_src, _ = os.path.splitext(filepath)
        path_dest = path_src + ".txt"
        with open(path_dest, "w") as f:
            subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=f,
                stderr=subprocess.DEVNULL,
            )
        self.content_path = path_dest

    def load_content(self, filepath):

        """
        Loads the content of the content_file file into the content
        member variable in the gazette object.
        """

        with open(filepath, "r") as f:
            self.content = f.read()

    def extract_metadata(self, filepath):

        """
        Calls the Apache Tika command using the configured jar file to extract
        metadata from the given gazette. The extracted metadata info will be
        write back to a json file on disk. The path to the json file will be
        stored in the metadata_file member variable in the gazette object.
        """

        check_file_to_extract_text_is_valid(filepath)
        command = self._build_apache_tika_command(filepath, metadata=True)
        path_src, _ = os.path.splitext(filepath)
        path_dest = path_src + ".json"

        with open(path_dest, "w") as f:
            subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=f,
                stderr=subprocess.DEVNULL,
            )
        self.metadata_path = path_dest

    def load_metadata(self, filepath):

        """
        Loads the content of the metadata_file file into the
        metadata member variable in the gazette object.
        """

        with open(filepath, "r") as f:
            self.metadata = json.load(f)


class ApacheTikaServerExtractor(TextExtractor):
    def __init__(self, apache_tika_server, **kwargs):
        if not is_url(apache_tika_server):
            raise Exception("ApacheTikaServerExtractor expected a server url.")
        self.apache_tika_server = apache_tika_server

    def _build_apache_tika_command(self, metadata=False):

        """
        something goes here
        """

        if metadata:
            command = self.apache_tika_server + 'meta'
        else:
            command = self.apache_tika_server + 'tika'
        LOGGER.debug(command)
        return command

    def extract_content(self, filepath):

        """
        something goes here
        """
        check_file_to_extract_text_is_valid(filepath)
        command = self._build_apache_tika_command()
        path_src, _ = os.path.splitext(filepath)
        path_dest = path_src + ".txt"

        with open(filepath, 'rb') as f:
            file = f.read()
            r = requests.put(command, data=file)

        with open(path_dest, 'w') as f:
            f.write(r.content.decode('UTF-8'))

        self.content_path = path_dest

    def load_content(self, filepath):

        """
        Loads the content of the content_file file into the content
        member variable in the gazette object.
        """

        with open(filepath, "r") as f:
            self.content = f.read()

    def extract_metadata(self, filepath):

        """
        something goes here
        """

        check_file_to_extract_text_is_valid(filepath)
        command = self._build_apache_tika_command(metadata=True)
        path_src, _ = os.path.splitext(filepath)
        path_dest = path_src + ".json"

        with open(filepath, "rb") as f:
            file = f.read()
            r = requests.put(
                command,
                data=file,
                headers={"Accept": "application/json"}
            )

        metadata = literal_eval(r.content.decode('UTF-8'))

        with open(path_dest, "w") as f:
            json.dump(metadata, f)

        self.metadata_path = path_dest

    def load_metadata(self, filepath):

        """
        Loads the content of the metadata_file file into the
        metadata member variable in the gazette object.
        """

        with open(filepath, "r") as f:
            self.metadata = json.load(f)
