# coding=utf-8

from typing import Optional


def clear(string: str, delchars: Optional[str] = "") -> str:
    """
    Clears string by removing unwanted spaces, HTML-tags, special and specified characters

    Args:
        string (str): String you want to clear
        delchars (Optional[str]): Characters you want to remove from string

    Returns:
        str: Cleared string

    Raises:
        TypeError: if 'string' argument type is not 'str'
    """

    # Checking str type

    if string is None:
        return ""
    elif not isinstance(string, str):
        raise TypeError(f"'string' argument type must be 'str', not '{string.__class__.__name__}'")

    # Deleting unwanted symbols

    for delstring in ["\n", "\t", "\r", "<b>", "</b>"]:
        string = string.replace(delstring, "")

    string = string.translate(
        str.maketrans(dict.fromkeys(delchars))
    )

    # Clearing extra spaces

    if string:
        index = 1

        try:
            # Clearing extra spaces at the beginning of string

            while string[0] == " ":
                string = string[1:]

            # Clearing extra spaces between words

            while index < len(string) - 2:
                if string[index] == string[index + 1] == " ":
                    string = string[:index] + string[index + 1:]
                else:
                    index += 1

            # Clearing extra spaces at the end of string

            if string:
                while string[-1] == " ":
                    string = string[:-1]
        except IndexError:
            pass

    return string
