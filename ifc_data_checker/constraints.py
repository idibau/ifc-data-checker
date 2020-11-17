"""Constraint Component Module"""
import abc
from typing import List

from ifc_data_checker import config
from ifc_data_checker.validation import ValidationInformation
from ifc_data_checker.validation import ValidationResult
from ifc_data_checker.yaml_helper import YamlMatchingKeys


class ConstraintComponent(abc.ABC, YamlMatchingKeys):
    """Constraint Component for Composite Pattern of Constraint Group and Constraint"""

    def __init__(self, definition: dict, ifc_instance):
        """Constructor

            Args:
                definition (dict): The defintion of the constraint component from the rules file.
                ifc_instance: The ifc instance to validate the constraint component.

            Raises:
                ValueError:
                    If the input parameter `definition` or `ifc_instance` is invalid.
        """
        super().__init__()
        if not definition:
            raise ValueError(f"{str(definition)} is None")
        if not isinstance(definition, dict):
            raise ValueError((f"definition "
                              f"{str(definition)} is not of type dict."
                              f"It's of type {type(definition)}"))
        if not ifc_instance:
            raise ValueError(f"ifc_instance {ifc_instance} is None")
        for yaml_key in self.yaml_keys:
            if not yaml_key in definition:
                raise ValueError((
                    f"The key {yaml_key} is missing in "
                    f"definition {str(definition)}"))
        self.definition = definition
        self.ifc_instance = ifc_instance
        self.validation_information = ValidationInformation()

    @abc.abstractmethod
    def validate(self):
        """Validates"""

    @abc.abstractmethod
    def report(self) -> List[str]:
        """Reports"""

    def is_valid(self) -> bool:
        """Returns True, if the validation result is ValidationResult.VALID, otherwise False"""
        return self.validation_information.validation_result == ValidationResult.VALID


class Constraint(ConstraintComponent):
    """Constraint"""

    yaml_keys = tuple(["path", "check"])

    def __init__(self, constraint_definition: dict, ifc_instance):
        """Constructor"""
        super().__init__(constraint_definition, ifc_instance)
        self.path_result = None

    def validate(self):
        """Validates the given constraint.

            This method can be called by an implementation of :class:`ConstraintGroup`.
            It applies the path on the given ifc instance and validates the path result
            on the constraint check.

            Raises:
                IndexError:
                    Raised if the path definition ends in nowhere.
                    Or raised if there is not one selected value at the end.
                AttributeError:
                    Raised if the path definition expect an attribute or a list,
                    which not exist in the ifc model.
        """
        try:
            self.path_result = self._apply_path()
            check = config.get_constraint_check(
                self.get_check(), self.path_result, self.ifc_instance)
            self.validation_information = check.validate()
        except (ValueError, IndexError, AttributeError) as error:
            self.validation_information.set_error(str(error))

    def report(self) -> List[str]:
        """Reports the validated constraint"""
        return [str(self.validation_information)]

    def _apply_path(self):
        """Applies the path on the ifc_instance

            If `path` is not defined, then return the `ifc_instance`.

            Raises:
                IndexError:
                    Raised if the path definition ends in nowhere.
                    Or raised if there is not one selected value at the end.
                AttributeError:
                    Raised if the path definition expect an attribute or a list,
                    which not exist in the ifc model.
        """
        path_results = [self.ifc_instance]
        if not self.get_path():
            return self.ifc_instance

        for path_operator_definition in self.get_path():
            operator = config.get_path_operator(
                path_operator_definition, path_results)
            path_results = operator.apply()
            if not path_results:
                raise IndexError("On traversing the path definition on the "
                                 "ifc instance ends in nowhere. "
                                 "There are none selected values.")
        if len(path_results) != 1:
            raise IndexError(
                "Per instance it is only allowed to have one path result")
        return path_results[0]

    def get_path(self) -> dict:
        """Returns the path definition"""
        return self.definition["path"]

    def get_check(self) -> dict:
        """Returns the constraint check definition"""
        return self.definition["check"]

    def __eq__(self, other):
        """Equals"""
        if not isinstance(other, Constraint):
            return False
        return (self.definition == other.definition and
                self.ifc_instance == other.ifc_instance and
                self.validation_information == other.validation_information and
                self.path_result == other.path_result)


class SetGroup(ConstraintComponent):
    """The set constraint group class

        Example:
            Defintion of a set constraint group in the rules file::

                constraints:
                    - set:
    """

    yaml_keys = tuple(["set"])
    """In the rules yaml the :class:`SetGroup` is defined by the keyword `set`"""

    def __init__(self, group_definition: dict, ifc_instance):
        """Constructor"""
        super().__init__(group_definition, ifc_instance)
        self.validated_constraints = []

    def validate(self):
        """Validates the constraints of the `constraint_group` on the `ifc_instances` independently.

            Raises:
                ValueError:
                    Raised on an invalid input parameter of
                    `ifc_instances` or `constraint_group`.
        """
        valid_constraints_count = 0
        for constraint_definition in self.definition["set"]:
            constraint = config.get_constraint(
                constraint_definition, self.ifc_instance)
            constraint.validate()
            if constraint.is_valid():
                valid_constraints_count += 1
            self.validated_constraints.append(constraint)
        if valid_constraints_count == len(self.validated_constraints):
            self.validation_information.set_valid(
                (f"set group: {ValidationResult.VALID}: "
                 f"{str(valid_constraints_count)} of "
                 f"{len(self.validated_constraints)} constraints are valid."))
        else:
            self.validation_information.set_failed(
                (f"set group: {ValidationResult.FAILED}: "
                 f"{str(valid_constraints_count)} of "
                 f"{len(self.validated_constraints)} constraints are valid."))

    def report(self) -> List[str]:
        """Reports the validated constraint"""
        report = [str(self.validation_information)]
        for validated_constraint in self.validated_constraints:
            report += validated_constraint.report()
        return report

    def __eq__(self, other):
        """Equals"""
        if not isinstance(other, SetGroup):
            return False
        return (self.definition == other.definition and
                self.ifc_instance == other.ifc_instance and
                self.validation_information == other.validation_information and
                self.validated_constraints == other.validated_constraints)


class OrGroup(ConstraintComponent):
    """The or constraint group class

        Example:
            Defintion of a or constraint group in the rules file::

                constraints:
                    - or:
    """

    yaml_keys = tuple(["or"])
    """In the rules yaml the :class:`OrGroup` is defined by the keyword `or`"""

    def __init__(self, group_definition: dict, ifc_instance):
        """Constructor"""
        super().__init__(group_definition, ifc_instance)
        self.validated_constraints = []

    def validate(self):
        """Validates the constraints of the `constraint_group` on the `ifc_instances` independently.

            Raises:
                ValueError:
                    Raised on an invalid input parameter of
                    `ifc_instances` or `constraint_group`.
        """
        or_validation_result = False
        valid_constraints_count = 0
        for constraint_definition in self.definition["or"]:
            constraint = config.get_constraint(
                constraint_definition, self.ifc_instance)
            constraint.validate()
            if constraint.is_valid():
                valid_constraints_count += 1
            or_validation_result = or_validation_result or constraint.is_valid()
            self.validated_constraints.append(constraint)

        if or_validation_result:
            self.validation_information.set_valid(
                (f"or group: {ValidationResult.VALID}: "
                 f"{valid_constraints_count} of "
                 f"{len(self.validated_constraints)} constraints are valid."))
        else:
            self.validation_information.set_failed(
                (f"or group: {ValidationResult.FAILED}: "
                 f"No one of "
                 f"{len(self.validated_constraints)} constraints are valid."))

    def report(self) -> List[str]:
        """Reports the validated constraint"""
        report = [str(self.validation_information)]
        for validated_constraint in self.validated_constraints:
            report += validated_constraint.report()
        return report

    def __eq__(self, other):
        """Equals"""
        if not isinstance(other, OrGroup):
            return False
        return (self.definition == other.definition and
                self.ifc_instance == other.ifc_instance and
                self.validation_information == other.validation_information and
                self.validated_constraints == other.validated_constraints)


class AndGroup(ConstraintComponent):
    """The and constraint group class

        Example:
            Defintion of a and constraint group in the rules file::

                constraints:
                    - and:
    """

    yaml_keys = tuple(["and"])
    """In the rules yaml the :class:`AndGroup` is defined by the keyword `and`"""

    def __init__(self, group_definition: dict, ifc_instance):
        """Constructor"""
        super().__init__(group_definition, ifc_instance)
        self.validated_constraints = []

    def validate(self):
        """Validates the constraints of the `constraint_group` on the `ifc_instances` independently.

            Raises:
                ValueError:
                    Raised on an invalid input parameter of
                    `ifc_instances` or `constraint_group`.
        """
        and_validation_result = True
        valid_constraints_count = 0
        for constraint_definition in self.definition["and"]:
            constraint = config.get_constraint(
                constraint_definition, self.ifc_instance)
            constraint.validate()
            if constraint.is_valid():
                valid_constraints_count += 1
            and_validation_result = and_validation_result and constraint.is_valid()
            self.validated_constraints.append(constraint)

        if and_validation_result:
            self.validation_information.set_valid(
                (f"and group: {ValidationResult.VALID}: "
                 f"Each of {len(self.validated_constraints)} constraints are valid."))
        else:
            self.validation_information.set_failed(
                (f"and group: {ValidationResult.FAILED}: "
                 f"{valid_constraints_count} of "
                 f"{len(self.validated_constraints)} constraints are valid."))

    def report(self) -> List[str]:
        """Reports the validated constraint"""
        report = [str(self.validation_information)]
        for validated_constraint in self.validated_constraints:
            report += validated_constraint.report()
        return report

    def __eq__(self, other):
        """Equals"""
        if not isinstance(other, AndGroup):
            return False
        return (self.definition == other.definition and
                self.ifc_instance == other.ifc_instance and
                self.validation_information == other.validation_information and
                self.validated_constraints == other.validated_constraints)
