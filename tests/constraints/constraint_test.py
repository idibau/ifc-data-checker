"""Constraint Unit Test Suite"""
import unittest

from ifc_data_checker.constraints import Constraint
from ifc_data_checker.validation import ValidationInformation

from tests.helpers import IfcInstanceMock


class TestConstraint(unittest.TestCase):
    """Test Constraint"""

    def test_constraint_attribute_error_attribute_path_operator(self):
        """Tests ``Constraint`` handling `AttributeError`s correctly.

        Test-Purpose:
            An invalid input parameter need to result in an `AttributeError`.
            The raised `AttributeError` need to except and ends in an validation information
            with ValidationResult.ERROR.

        Under Test:
            * ``Constraint.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `constraint_definition`: path defintion with attribute path operator

        Expected:
            validation information with ``ValidationResult.ERROR``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        # definitions
        constraint_definition = {
            "path": [{"attribute": "MissingAttribute"}], "check": {"equals": "IfcMock"}
        }
        # expected
        expected_validation_information = ValidationInformation()
        expected_validation_information.set_error(
            "'IfcInstanceMock' object has no attribute 'MissingAttribute'")
        expected_constraint = Constraint(
            constraint_definition, ifc_instance)
        expected_constraint.validation_information = expected_validation_information
        # test
        constraint = Constraint(constraint_definition, ifc_instance)
        constraint.validate()
        self.assertEqual(expected_constraint, constraint)

    def test_constraint_attribute_error_list_path_operator(self):
        """Tests ``Constraint`` handling `AttributeError`s correctly.

        Test-Purpose:
            An invalid input parameter need to result in an `AttributeError`.
            The raised `AttributeError` need to except and ends in an validation information
            with ValidationResult.ERROR.

        Under Test:
            * ``Constraint.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `constraint_definition`: path defintion with list path operator

        Expected:
            validation information with ``ValidationResult.ERROR``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        # definitions
        constraint_definition = {
            "path": [{"list": "MissingList"}], "check": {"equals": "IfcMock"}
        }
        # expected
        expected_validation_information = ValidationInformation()
        expected_validation_information.set_error(
            "'IfcInstanceMock' object has no attribute 'MissingList'")
        expected_constraint = Constraint(
            constraint_definition, ifc_instance)
        expected_constraint.validation_information = expected_validation_information
        # test
        constraint = Constraint(constraint_definition, ifc_instance)
        constraint.validate()
        self.assertEqual(expected_constraint, constraint)

    def test_constraint_filter_type_nothing(self):
        """Tests ``Constraint`` handling `IndexError`s correctly.

        Test-Purpose:
            An invalid input parameter need to result in an `IndexError`.
            The raised `IndexError` need to except and ends in an validation information
            with `ValidationResult.ERROR`.

        Under Test:
            * ``Constraint.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `constraint_definition`: path defintion with type filter path operator

        Expected:
            validation information with ``ValidationResult.ERROR``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        # definitions
        constraint_definition = {
            "path": [{"type": "NoneType"}], "check": {"equals": "IfcMock"}
        }
        # expected
        expected_validation_information = ValidationInformation()
        expected_validation_information.set_error(
            "On traversing the path definition on the "
            "ifc instance ends in nowhere. "
            "There are none selected values.")
        expected_constraint = Constraint(
            constraint_definition, ifc_instance)
        expected_constraint.validation_information = expected_validation_information
        # test
        constraint = Constraint(constraint_definition, ifc_instance)
        constraint.validate()
        self.assertEqual(expected_constraint, constraint)

    def test_constraint_filter_attribute_nothing(self):
        """Tests ``Constraint`` handling `IndexError`s correctly.

        Test-Purpose:
            An invalid input parameter need to result in an `IndexError`.
            The raised `IndexError` need to except and ends in an validation information
            with `ValidationResult.ERROR`.

        Under Test:
            * ``Constraint.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `constraint_definition`: path defintion with attribute filter path operator

        Expected:
            validation information with ``ValidationResult.ERROR``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        # definitions
        constraint_definition = {
            "path": [{"attribute": "Name", "value": "NoName"}], "check": {"equals": "IfcMock"}
        }
        # expected
        expected_validation_information = ValidationInformation()
        expected_validation_information.set_error(
            "On traversing the path definition on the "
            "ifc instance ends in nowhere. "
            "There are none selected values.")
        expected_constraint = Constraint(
            constraint_definition, ifc_instance)
        expected_constraint.validation_information = expected_validation_information
        # test
        constraint = Constraint(constraint_definition, ifc_instance)
        constraint.validate()
        self.assertEqual(expected_constraint, constraint)

    def test_constraint_validate_ending_multi_selection(self):
        """Tests ``Constraint.validate`` on have only one ending value
        at the end of traversing by the path operators.

        Test-Purpose:
            There must be at the end of traversing only one single value.

        Under Test:
            * ``Constraint.validate``

        Given:
            * `ifc_instance` object of ``IfcInstanceMock`` with list attribute
            * `path_operator`: list path operator

        Expected:
            Constraint with a validation information with ValidationResult.ERROR

        Comment:
            Usage of ``IfcInstanceMock`` to represent an instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType",
            IsDefinedBy=[1, 2, 3, 4]
        )
        path_operator_definition = {"list": "IsDefinedBy"}
        constraint_definition = {
            "path": [path_operator_definition], "check": {"equals": "value"}}
        # expected
        expected_constraint = Constraint(constraint_definition, ifc_instance)
        expected_validation_information = ValidationInformation()
        expected_validation_information.set_error(
            "Per instance it is only allowed to have one path result")
        expected_constraint.validation_information = expected_validation_information
        # test
        constraint = Constraint(constraint_definition, ifc_instance)
        constraint.validate()
        self.assertEqual(expected_constraint, constraint)

    def test_constraint_validate_ends_in_nowhere(self):
        """Tests ``Constraint.validate`` on resulting in an ValidationResult.ERROR,
        because ending in nowhere.

        Test-Purpose:
            The path definition need to end always in a path result.
            It's not allowed to ends in nowhere in traversing the ifc model.
            The creator of the rules file need to know the validated ifc models.

        Under Test:
            * ``Constraint.validate``

        Given:
            * `ifc_instance` object of ``IfcInstanceMock`` with list attribute
            * `path_operator`: filter attribute path operator and filter type path operator

        Expected:
            Constraint with a validation information with ValidationResult.ERROR

        Comment:
            Usage of ``IfcInstanceMock`` to represent an instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        path_operator_definition = {"attribute": "Name", "value": "FilterNone"}
        constraint_definition = {
            "path": [path_operator_definition], "check": {"equals": "value"}}
        # expected
        expected_constraint = Constraint(constraint_definition, ifc_instance)
        expected_validation_information = ValidationInformation()
        expected_validation_information.set_error("On traversing the path definition on the "
                                                  "ifc instance ends in nowhere. "
                                                  "There are none selected values.")
        expected_constraint.validation_information = expected_validation_information
        # test
        constraint = Constraint(constraint_definition, ifc_instance)
        constraint.validate()
        self.assertEqual(expected_constraint, constraint)

        path_operator_definition = {"type": "IfcDoor"}
        constraint_definition = {
            "path": [path_operator_definition], "check": {"equals": "value"}}
        # expected
        expected_constraint = Constraint(constraint_definition, ifc_instance)
        expected_validation_information = ValidationInformation()
        expected_validation_information.set_error("On traversing the path definition on the "
                                                  "ifc instance ends in nowhere. "
                                                  "There are none selected values.")
        expected_constraint.validation_information = expected_validation_information
        # test
        constraint = Constraint(constraint_definition, ifc_instance)
        constraint.validate()
        self.assertEqual(expected_constraint, constraint)

    def test_constraint_validate_path_none(self):
        """Tests ``Constraint.validate`` on return the ifc instance, if the path is `None`.

        Test-Purpose:
            If there is no path defined, the ifc instance should be returned.

        Under Test:
            * ``Constraint.validate``

        Given:
            * `ifc_instance` object of ``IfcInstanceMock`` with list attribute

        Expected:
            The ifc instance get returned.

        Comment:
            Usage of ``IfcInstanceMock`` to represent an instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        constraint_definition = {
            "path": None, "check": {"exists": "Name"}
        }
        # expected
        expected_constraint = Constraint(constraint_definition, ifc_instance)
        expected_constraint.path_result = ifc_instance
        expected_validation_information = ValidationInformation()
        expected_validation_information.set_valid(
            "attribute Name exists as expected.")
        expected_constraint.validation_information = expected_validation_information
        # test
        constraint = Constraint(constraint_definition, ifc_instance)
        constraint.validate()
        self.assertEqual(expected_constraint, constraint)
