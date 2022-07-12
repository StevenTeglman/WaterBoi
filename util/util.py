from dataclasses import asdict, dataclass


def remove_empty(dc: dataclass) -> dict:
    """
    Takes given dataclass, removes all None or False values, and converts to dictionary.

    return: dict
    """
    new_dict = {k: v for k, v in asdict(dc).items() if v}

    return new_dict
