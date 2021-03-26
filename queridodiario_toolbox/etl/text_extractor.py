from queridodiario_toolbox.etl.apache_tika_text_extractor import (
    ApacheTikaExtractor,
    ApacheTikaServerExtractor,
)
from queridodiario_toolbox.etl.text_extractor_interface import TextExtractor


def create_text_extractor(config) -> TextExtractor:

    """
    Instantiates a text extractor object based on user configuration.
    """

    if "apache_tika_server" in config.keys():
        extractor = ApacheTikaServerExtractor(config["apache_tika_server"])

    elif "apache_tika_jar" in config.keys():
        extractor = ApacheTikaExtractor(config["apache_tika_jar"])

    return extractor
