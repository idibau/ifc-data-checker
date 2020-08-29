"""Path Operators"""
import abc
from typing import Any, List

from ifc_data_checker.yaml import YamlMatchingKeys


class PathOperator(abc.ABC, YamlMatchingKeys):
    """The path operator base class.

        Every path operator implementation need to
        inherit from this class :class:`PathOperator`.
    """

    def __init__(self, actual_position: List[Any], definition: dict):
        """Constructor

            Args:
                actual_position (List[Any]):
                    The actual position in the ifc model.
                    The actual selected values.
                path_operator (dict):
                    The path operator from the rules file.

            Raises:
                ValueError:
                    Raised on an invalid input parameter of
                    `actual_position` or `path_operator`.
        """
        if not actual_position:
            raise ValueError("actual_position is None")
        if not isinstance(actual_position, list):
            raise ValueError((f"actual_position {actual_position} is not of type list "
                              f"- actual_position is of type {type(actual_position)}"))
        self.actual_position = actual_position
        if not definition:
            raise ValueError("definition is None")
        if not isinstance(definition, dict):
            raise ValueError((f"definition {definition} is not of type dict "
                              f"- definition is of type {type(definition)}"))
        for yaml_key in self.yaml_keys:
            if not yaml_key in definition:
                raise ValueError(
                    f"The key {yaml_key} is missing in path_operator {definition}")
            if not definition[yaml_key]:
                raise ValueError(
                    f"definition[{yaml_key}] is None")
        self.definition = definition

    @abc.abstractmethod
    def apply(self) -> List[Any]:
        """The base method to validate the input parameter.

            The `apply` method implementing the input parameter validation
            of `self.actual_path_position` and `path_operator`.

            Returns:
                List[Any]:
                    The selected values after applying the `path_operator`.
        """


class AttributePathOperator(PathOperator):
    """The attribute path operator class

        Example:
            Defintion of a attribute path operator in the rules file::

                path:
                  - attribute: attributename
    """

    yaml_keys = tuple(["attribute"])
    """In the rules yaml the :class:`AttributePathOperator` is defined by the keyword `attribute`"""

    def apply(self) -> List[Any]:
        """Applies the attribute path operator on the actual position.

            Using of `getattr` to get the value of an attribute by its name.

            Returns:
                List[Any]:
                    The selected values after applying the `path_operator`.
        """
        return list(map(lambda i: getattr(i, self.definition["attribute"]), self.actual_position))


class AttributeFilterPathOperator(PathOperator):
    """The attribute filter path operator class

        Example:
            Defintion of a attribute filter path operator in the rules file::

                path:
                  - attribute: attributename
                    value: value to filter
    """

    yaml_keys = tuple(["attribute", "value"])
    """In the rules yaml the :class:`AttributeFilterPathOperator`
    is defined by the keyword `attribute` and `value`"""

    def apply(self) -> List[Any]:
        """Applies the attribute filter path operator on the actual position.

            Using of `getattr` to get the value of an attribute by its name.
            And then filters by their values.

            Returns:
                list:
                    The selected values after applying the `path_operator`.
        """
        attribute_name = self.definition["attribute"]
        attribute_value = self.definition["value"]
        return list(filter(lambda i:
                           hasattr(i, attribute_name) and
                           getattr(i, attribute_name) == attribute_value, self.actual_position))


class TypeFilterPathOperator(PathOperator):
    """The type filter path operator class

        Example:
            Defintion of a type filter path operator in the rules file::

                path:
                  - type: type to filter
    """

    yaml_keys = tuple(["type"])
    """In the rules yaml the :class:`TypeFilterPathOperator` is defined by the keyword `type`"""

    def apply(self) -> List[Any]:
        """Applies the type filter path operator on the actual position.

            Using of ifcopenshell function `is_a` to get the type of the actual position.
            And then filters by their type.

            Returns:
                List[Any]:
                    The selected values after applying the `path_operator`.
        """
        return list(filter(lambda i: i.is_a(self.definition["type"]), self.actual_position))


class ListPathOperator(PathOperator):
    """The list path operator class

        Example:
            Defintion of a list path operator in the rules file::

                path:
                  - list: listname
    """

    yaml_keys = tuple(["list"])
    """In the rules yaml the :class:`ListPathOperator` is defined by the keyword `list`"""

    def apply(self) -> List[Any]:
        """Applies the list path operator on the actual position.

            Using of `getattr` to get the list of its name.
            And then selecting all the items of this list as the new `actual_position`.

            Returns:
                List[Any]:
                    The selected values after applying the `path_operator`.
        """
        def execute_list(instances, list_name):
            return [tuple_attribute
                    for i in instances
                    for tuple_attribute in list(getattr(i, list_name))]
        return execute_list(self.actual_position, self.definition["list"])
