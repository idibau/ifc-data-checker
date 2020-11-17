"""Constraint"""
from collections import Counter
from typing import Tuple


class YamlMatchingKeys:
    """YAML Constraint"""

    yaml_keys = tuple([])

    @classmethod
    def matching_yaml_keys(cls, keys: Tuple[str]) -> bool:
        """Checks if the given keys matching this Path Operator"""
        return Counter(cls.yaml_keys) == Counter(keys)

    @classmethod
    def get_yaml_keys(cls) -> tuple:
        """Gets the YAML keys of this class"""
        return cls.yaml_keys
