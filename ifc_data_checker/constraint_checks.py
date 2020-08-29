"""Constraint Checks"""
import abc

from ifc_data_checker import config
from ifc_data_checker.validation import ValidationInformation
from ifc_data_checker.yaml import YamlMatchingKeys


class ConstraintCheck(abc.ABC, YamlMatchingKeys):
    """The constraint check base class.

        Every constraint check implementation need to
        inherit from this class :class:`ConstraintCheck`.
    """

    def __init__(self, definition: dict, path_result, ifc_instance):
        """Constructor

            Args:
                definition (dict):
                    The constraint check from the rules file.
                path_result:
                    The value after applying the path on the ifc instance.
                ifc_instance:
                    For reporting reasons the ifc instance is required.

            Raises:
                ValueError:
                    Raised on an invalid input parameter of
                    ifc_instance, path_result or constraint_check.
        """
        if not definition:
            raise ValueError("definition is None")
        for yaml_key in self.yaml_keys:
            if not yaml_key in definition:
                raise ValueError(
                    f"The key {yaml_key} is missing in {definition}")
            if not definition[yaml_key]:
                raise ValueError(
                    f"definition[{yaml_key}] is None")
        self.definition = definition
        if not path_result:
            raise ValueError("path_result is None")
        self.path_result = path_result
        if not ifc_instance:
            raise ValueError("ifc_instance is None")
        self.ifc_instance = ifc_instance

    @abc.abstractmethod
    def validate(self) -> ValidationInformation:
        """Validates the constraint check"""


class EqualsCheck(ConstraintCheck):
    """The equals constraint check class

        Example:
            Defintion of a equals constraint check in the rules file: :

                check:
                    equals: The valid value
    """

    yaml_keys = tuple(["equals"])
    """In the rules yaml the: class: `EqualsCheck` is defined by the keyword `equals`"""

    def validate(self) -> ValidationInformation:
        """Validates the `path_result` on equality.

            Using the `==` operator to check equality.

            Returns:
                ValidationInformation:
                    The validation information about the validation
                    of the constraint check on the path result.
        """
        expected_value = self.definition["equals"]
        validation_information = ValidationInformation()
        if self.path_result == expected_value:
            validation_information.set_valid(f"{expected_value} as expected")
        else:
            validation_information.set_failed((
                f"validation equals failed - expected: {expected_value}, "
                f"actual: {self.path_result}"))
        return validation_information


class ExistsCheck(ConstraintCheck):
    """The exists constraint check class

        Example:
            Defintion of a exists constraint check in the rules file::

                check:
                    exists: attributename
    """

    yaml_keys = tuple(["exists"])
    """In the rules yaml the :class:`ExistsCheck` is defined by the keyword `exists`"""

    def validate(self) -> ValidationInformation:
        """Validates the `path_result` on an attribute to exists.

            Using the `hasattr` method to check if an attribute exists.

            Returns:
                ValidationInformation:
                    The validation information about the validation
                    of the constraint check on the path result.
        """
        validation_information = ValidationInformation()
        expected_attribute = self.definition['exists']
        if hasattr(self.path_result, expected_attribute):
            validation_information.set_valid(
                f"attribute {str(expected_attribute)} exists as expected.")
        else:
            validation_information.set_failed((f"attribute {str(expected_attribute)} not"
                                               f"exists in {str(self.path_result)}."))
        return validation_information


class InCheck(ConstraintCheck):
    """The in constraint check class

        Example:
            Defintion of a in constraint check in the rules file::

                check:
                    in:
                      - valid value one
                      - valid value two
                      - valid value three
    """

    yaml_keys = tuple(["in"])
    """In the rules yaml the :class:`InCheck` is defined by the keyword `in`"""

    def validate(self) -> ValidationInformation:
        """Validates the `path_result` that it it is one of the allowed values.

            Using the `in` operator to check if `path_result` is in the allowed values.

            Returns:
                ValidationInformation:
                    The validation information about the validation
                    of the constraint check on the path result.
        """
        allowed_values = self.definition["in"]
        validation_information = ValidationInformation()
        if self.path_result in allowed_values:
            validation_information.set_valid(f"{self.path_result} is allowed")
        else:
            validation_information.set_failed(
                f"validation in error - allowed: {allowed_values}, actual: {self.path_result}")
        return validation_information


class NotCheck(ConstraintCheck):
    """The not constraint check class

        Example:
            Defintion of a equals constraint check in the rules file::

                check:
                    not:
                      equals: the valid value
    """

    yaml_keys = tuple(["not"])
    """In the rules yaml the :class:`NotCheck` is defined by the keyword `not`"""

    def validate(self) -> ValidationInformation:
        """Validates the `path_result` on negation, using the underlying check.

            Using the `if` and `else` for negation.

            Returns:
                ValidationInformation:
                    The validation information about the validation
                    of the constraint check on the path result.
        """
        check_definition = self.definition["not"]
        check = config.get_constraint_check(
            check_definition, self.path_result, self.ifc_instance)
        validation_information = check.validate()
        not_validation_information = ValidationInformation()
        if validation_information:
            not_validation_information.set_failed(
                f"check was VALID, but expected FAILED, message: {validation_information.message}")
        else:
            not_validation_information.set_valid(
                f"check FAILED as expected, message: {validation_information.message}")
        return not_validation_information


class TypeCheck(ConstraintCheck):
    """The type constraint check class

        Example:
            Defintion of a type constraint check in the rules file::

                check:
                    type: expectedtype
    """

    yaml_keys = tuple(["type"])
    """In the rules yaml the :class:`TypeCheck` is defined by the keyword `type`"""

    def validate(self) -> ValidationInformation:
        """Validates the `path_result` on an expected type.

            Using the `is_a` method to check the type.

            Returns:
                ValidationInformation:
                    The validation information about the validation
                    of the constraint check on the path result.
        """
        validation_information = ValidationInformation()
        expected_type = self.definition['type']
        if not hasattr(self.path_result, 'is_a'):
            validation_information.set_error((f"path_result {str(self.path_result)} is "
                                              f"not of type entity_instance of ifcopenshell"))
        elif self.path_result.is_a(expected_type):
            validation_information.set_valid((f"type of {str(self.path_result)} "
                                              f"as expected {str(expected_type)}."))
        else:
            validation_information.set_failed((f"{str(self.path_result)} is "
                                               f"not of type {str(expected_type)}, "
                                               f"it is of type {str(self.path_result.is_a())}."))
        return validation_information
