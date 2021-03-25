import abc

class TextExtractor(abc.ABC):
    """
    Text extractor interface. This interface define the methods that all text
    extractor should have in order to properly work with the library
    """

    @abc.abstractmethod
    def extract_content(self, gazette):
        """
        Extract the text from the given gazette.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def load_content(self, gazette):
        """
        Load into memory the text from the given gazette.
        """
        raise NotImplemented()

    @abc.abstractmethod
    def extract_metadata(self, gazette):
        """
        Extract the given gazette file metadata
        """
        raise NotImplemented()

    @abc.abstractmethod
    def load_metadata(self, gazette):
        """
        Load into memory the given gazette file metadata
        """
        raise NotImplemented()
