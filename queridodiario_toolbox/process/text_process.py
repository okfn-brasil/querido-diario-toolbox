from subprocess import check_output, DEVNULL
import re
import string


def remove_breaks(text: str) -> str:
    """
        Remove breaks, multiple whitespaces (including trimming leading
        and trailing spaces), and return single text.
    """
    text = _remove_new_line_splitting_word(text)
    text = _remove_repeating_whitespaces_and_new_lines(text)
    text = _remove_whitespaces_beginning_end_text(text)
    return text


def _remove_new_line_splitting_word(text: str) -> str:
    """ Removes new lines splitting words."""
    return re.sub(r"(\w)-(\n|\r){1,2}(\w)", r"\1\3", text)


def _remove_repeating_whitespaces_and_new_lines(text: str) -> str:
    """Removes repeating new lines and tabular char."""
    return re.sub(r"(\n|\r|\t| ){1,}", " ", text)


def _remove_whitespaces_beginning_end_text(text: str) -> str:
    """Removes whitespace from the beginning and end of the given text."""
    return text.strip()


def remove_duplicate_punctuation(text: str) -> str:
    """
        Remove duplicate punctuation, which may have been a feature of
        gazette design.
    """
    pattern = f"([{string.punctuation}])" + "{1,}"
    pattern = re.compile(pattern)
    text = re.sub(pattern, r"\1", text)
    return text


def execute_tabula(
    filepath: str, tabula_jar: str, *args: str, **kwargs: str
) -> str:
    """
        Extract table and text from gazette. pass additional args to
        tabula following its documentation
    """
    command = ["java", "-jar", tabula_jar, filepath]

    if args:
        for arg in args:
            command.extend([arg])

    if kwargs:
        for k, v in kwargs.items():
            command.extend([k, v])

    page = check_output(command, stderr=DEVNULL)
    page = page.decode("utf-8")
    return page


# def process_text(self, store_text: Optional[bool] = False) -> str:
#     """
#         Process gazette text and return linearized text
#     """
#     self.store_text = store_text

#     if isinstance(self.content, dict):
#         raise TypeError("str expected, not dict")
#     else:
#         text = remove_breaks(self.content)
#         text = remove_duplicate_punctuation(text)
#         if self.store_text:
#             self.content = text
#         else:
#             return text

# def scan_cpf(
#     self, text: Optional[str] = None, validate: Optional[bool] = False
# ) -> Sequence[str]:
#     """
#         Scan for cpfs and validate cpfs them if required by user.
#     """
#     if self.store_text:
#         cpfs = scan_individual_identifiers(self.content)
#     elif not self.store_text and not text:
#         raise Exception("You need to provide a string to scan for CPF.")
#     else:
#         cpfs = scan_individual_identifiers(text)

#     if validate:
#         cpfs = [
#             cpf for cpf in cpfs if validate_individual_identifiers(cpf)
#         ]

#     if cpfs:
#         return set(cpfs)

# def scan_cnpj(
#     self, text: Optional[str] = None, validate: Optional[bool] = False
# ) -> Sequence[str]:
#     """
#         Scan for cnpjs and validate cpfs them if required by user.
#     """
#     if self.store_text:
#         cnpjs = scan_individual_identifiers(self.content, cpf=False)
#     elif not self.store_text and not text:
#         raise Exception("You need to provide a string to scan for CNPJ.")
#     else:
#         cnpjs = scan_individual_identifiers(text, cpf=False)

#     if validate:
#         cnpjs = [
#             cnpj
#             for cnpj in cnpjs
#             if validate_individual_identifiers(cnpj, cpf=False)
#         ]

#     if cnpjs:
#         return set(cnpjs)
