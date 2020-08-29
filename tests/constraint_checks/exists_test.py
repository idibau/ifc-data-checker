"""Exists Check Unit Test Suite"""
from ifc_data_checker import config
from ifc_data_checker.constraint_checks import ExistsCheck
from ifc_data_checker.validation import ValidationInformation
from ifc_data_checker.validation import ValidationResult

from tests.constraint_checks.constraint_check_test import TestConstraintCheck
from tests.helpers import IfcInstanceMock
from tests.helpers import MicroMock


class TestExistsCheck(TestConstraintCheck.TestParameterValidation):
    """Test Exists Constraint"""

    constraint_check_class = ExistsCheck
    default_path_result = MicroMock(attribute1="value1")
    default_constraint = {"exists": "attribute1"}

    def test_exists_valid(self):
        """Tests ``ExistsCheck`` on valid validation results

        Test-Purpose:
            Tests that a ifc instance that has an attribute,
            finishs in a `valid` validation information.

        Under Test:
            * ``ExistsCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * expected_attribute: The attribute `GlobalId` of the ifc instance
            * actual value: The `ifc_instance`
            * constraint: The exists constraint to check.
              Using `expected_attribute`

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        expected_attribute = "GlobalId"
        path_result = ifc_instance
        expected_result = ValidationInformation()
        expected_result.message = f"attribute {str(expected_attribute)} exists as expected."
        expected_result.validation_result = ValidationResult.VALID
        check_definition = {"exists": expected_attribute}
        check = ExistsCheck(
            check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())

    def test_exists_failed(self):
        """Tests ``ExistsCheck`` on failed validation results

        Test-Purpose:
            Tests that a ifc instance that hasn't an expected attribute,
            finishs in a `failed` validation information.

        Under Test:
            * ``ExistsCheck``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * expected_attribute: The attribute `NewAttribute`
            * actual value: The `ifc_instance`
            * constraint: The exists constraint to check.
              Using `expected_attribute`

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        expected_attribute = "NewAttribute"
        path_result = ifc_instance
        expected_result = ValidationInformation()
        expected_result.message = (f"attribute {str(expected_attribute)} not"
                                   f"exists in {str(path_result)}.")
        expected_result.validation_result = ValidationResult.FAILED
        check_definition = {"exists": expected_attribute}
        check = ExistsCheck(
            check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())

    def test_exists_check_invalid_keyword(self):
        """Tests ``ExistsCheck`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{exists}`

        Under Test:
            * ``ExistsCheck``

        Given:
            * `ifc_instance`: Mock Ifc Instance
            * `path_result`: "value1"
            * `constraint_check`: {"": "nonexisting"} and {"notexists": "nonexisting"}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and "notexists"

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        path_result = "value1"
        exists_check = {"": "IfcMock"}
        self.assertRaises(ValueError, ExistsCheck,
                          exists_check, path_result, ifc_instance)
        exists_check = {"notexists": "IfcMock"}
        self.assertRaises(ValueError, ExistsCheck,
                          exists_check, path_result, ifc_instance)

    def test_exists_check_invalid_attribute(self):
        """Tests ``ExistsCheck`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{exists}`

        Under Test:
            * ``ExistsCheck.validate``

        Given:
            * `ifc_instance`: Mock Ifc Instance
            * `path_result`: "value1"
            * `constraint_check`: {"exists": ""} and {"exists": None}

        Expected:
            Raises ``ValueError`` because of invalid dict attribute "" and ``None``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        path_result = "value1"
        exists_check = {"exists": ""}
        self.assertRaises(ValueError, ExistsCheck,
                          exists_check, path_result, ifc_instance)
        exists_check = {"exists": None}
        self.assertRaises(ValueError, ExistsCheck,
                          exists_check, path_result, ifc_instance)

    def test_exists_yaml_keys(self):
        """Tests ``ExistsCheck`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``ExistsCheck`` won't change

        Under Test:
            * ``ExistsCheck.yaml_keys``

        Given:
            * ``ExistsCheck``

        Expected:
            The `yaml_keys` of ``ExistsCheck`` is 'exists'"""
        self.assertEqual(("exists",), ExistsCheck.get_yaml_keys())

    def test_exists_constraint_get_constraint_check(self):
        """Tests ``config.get_constraint_check`` on applying the constraint check correctly.

        Test-Purpose:
            Tests that the constraint check ``ExistsCheck``
            validated correctly on the actual value

        Under Test:
            * ``config.get_constraint_check``

        Given:
            * `ifc_instance`: Object of ``IfcInstanceMock``
            * dict of exists constraint check

        Expected:
            That the constraint check ``ExistsCheck``
            get validated on the `path_result` is a valid validation information

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        expected_attribute = "GlobalId"
        path_result = ifc_instance
        expected_result = ValidationInformation()
        expected_result.message = f"attribute {str(expected_attribute)} exists as expected."
        expected_result.validation_result = ValidationResult.VALID
        constraint_definition = {"exists": expected_attribute}
        check = config.get_constraint_check(
            constraint_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())
