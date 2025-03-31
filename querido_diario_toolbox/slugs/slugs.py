from slugify import slugify


def make_entity_slug(name, prefix="", separator="_"):
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    if not isinstance(prefix, str):
        raise ValueError("prefix must be a string")
    if not isinstance(separator, str):
        raise ValueError("separator must be a string")
    if separator not in ["", "_", "-"]:
        raise ValueError(
            "separator must be a empty string (''), underscore ('_') or hyphen ('-')"
        )

    fullname = f"{prefix} {name}"

    for replace_case in [("-", ""), ("'", "")]:
        fullname = fullname.replace(replace_case[0], replace_case[1])

    return slugify(fullname, separator=separator)
