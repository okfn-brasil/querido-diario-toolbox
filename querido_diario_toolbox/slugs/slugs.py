from slugify import slugify


def make_entity_slug(name, prefix="", separator="_"):
    """Create a slugified string for name and prefix using separator as connection

    Note:
        At the moment, Querido Diário slugifies entities names by using empty (""),
        underscore ('_') or hyphen ('-') only, so this function limits the
        separator options to these characters.

    Args:
        name (str): entity name
        prefix (str): extra info related to name (optional). Default: ""
        separator (str): char used to connect words (optional). Default: '_'

    Returns:
        str: slugified text

    Raises:
        ValueError: If params aren't strings or separator isn't an allowed char

    Examples:
        >>> make_entity_slug("Rio Branco", "Acre")
        "acre_rio_branco"
        >>> make_entity_slug("São Tomé das Letras", "", "-")
        "sao-tome-das-letras"
        >>> make_entity_slug("Associação de Municípios", "", "")
        "associacaodemunicipios"
    """
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    if not isinstance(prefix, str):
        raise ValueError("prefix must be a string")
    if not isinstance(separator, str):
        raise ValueError("separator must be a string")
    if separator not in ["", "_", "-"]:
        raise ValueError(
            "separator must be an empty string (''), underscore ('_') or hyphen ('-')"
        )

    fullname = f"{prefix} {name}"

    for replace_case in [("-", ""), ("'", "")]:
        fullname = fullname.replace(replace_case[0], replace_case[1])

    return slugify(fullname, separator=separator)
