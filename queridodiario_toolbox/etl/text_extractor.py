from queridodiario_toolbox.etl.apache_tika_text_extractor import ApacheTikaExtractor
from queridodiario_toolbox.etl.text_extractor_interface import TextExtractor


def create_text_extractor(config) -> TextExtractor:
    """
    Instantiates a text extractor object based on the given configuration.
    """
    return ApacheTikaExtractor(config["apache_tika_jar"])
