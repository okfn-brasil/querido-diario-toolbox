import abc


class TextExtractor(abc.ABC):
    """
    Text extractor interface. This interface define the methods that all text
    extractor should have in order to properly work with the library
    """

    @abc.abstractmethod
    def extract_content(self, filepath):
        """
        Extract the text from the given filepath.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def load_content(self, filepath):
        """
        Load into memory the text from the given filepath.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def extract_metadata(self, filepath):
        """
        Extract the given filepath file metadata
        """
        raise NotImplemented()

    @abc.abstractmethod
    def load_metadata(self, filepath):
        """
        Load into memory the given filepath file metadata
        """
        raise NotImplemented()
