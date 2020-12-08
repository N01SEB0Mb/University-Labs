# coding=utf-8

from flask import current_app
from typing import Iterable, List, Set

from topauto_parser.types.clients import BaseClient


def getParametersList(
        parameters: str
) -> List[str]:
    """
    Used to get parameters list from string

    Args:
        parameters (str): Parameters string

    Returns:
        List[str]: Found parameters

    Examples:
        >>> getParametersList("[1, 2]")
        ['1', '2']
    """

    parametersList = list()

    if parameters and parameters[0] == "[" and parameters[-1] == "]":
        parameter = ""

        for char in parameters[1:]:
            if char in (",", "]") and parameter:
                parametersList.append(parameter)
                parameter = ""
            else:
                parameter += char

    return parametersList


def getClients(
    clientNames: Iterable[str]
) -> List[BaseClient]:
    """
    Get clients from client names

    Args:
        clientNames (Iterable[str]): Client names

    Returns:
        List[BaseClient]: Client classes with matching names.
            If no name matches, then returns all client classes
    """

    appClients = current_app.clients

    if clientNames:
        return list(
            filter(
                lambda client: client.name in clientNames,
                appClients
            )
        )
    else:
        return appClients
