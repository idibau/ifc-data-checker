"""Type Check Unit Test Suite"""
from ifc_data_checker import config
from ifc_data_checker.constraint_checks import TypeCheck
from ifc_data_checker.validation import ValidationInformation
from ifc_data_checker.validation import ValidationResult

from tests.constraint_checks.constraint_check_test import TestConstraintCheck
from tests.helpers import IfcInstanceMock
from tests.helpers import MicroMock


class TestTypeCheck(TestConstraintCheck.TestParameterValidation):
    """Test Type Constraint"""

    constraint_check_class = TypeCheck
    default_path_result = MicroMock(is_a="microtype")
    default_constraint = {"type": "type1"}

    def test_type_valid(self):
        """Tests ``TypeCheck`` on valid validation results

        Test-Purpose:
            Tests that a ifc instance that machting an expected type,
            finishs in a `valid` validation information.

        Under Test:
            * ``TypeCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * expected_type: The type `IfcWindow` of the ifc instance
            * path_result: The `ifc_instance`
            * constraint: The type constraint to check.
              Using `expected_type`

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="IfcWindow"
        )
        expected_type = "IfcWindow"
        path_result = ifc_instance
        expected_result = ValidationInformation()
        expected_result.message = f"type of {str(path_result)} as expected {str(expected_type)}."
        expected_result.validation_result = ValidationResult.VALID
        check_definition = {"type": expected_type}
        check = TypeCheck(
            check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())

    def test_type_failed(self):
        """Tests ``TypeCheck`` on failed validation results

        Test-Purpose:
            Tests that a ifc instance that not matching an expected type,
            finishs in a `failed` validation information.

        Under Test:
            * ``TypeCheck``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance with type `anothertype`
            * expected_type: The type `IfcWindow` of the ifc instance
            * path_result: The `ifc_instance`
            * constraint: The type constraint to check.
              Using `expected_type`

        Expected:
            validation information with ``ValidationResult.FAILED``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="anothertype"
        )
        expected_type = "IfcWindow"
        path_result = ifc_instance
        expected_result = ValidationInformation()
        expected_result.message = (f"{str(path_result)} is "
                                   f"not of type {str(expected_type)}, "
                                   f"it is of type {str(path_result.is_a())}.")
        expected_result.validation_result = ValidationResult.FAILED
        check_definition = {"type": expected_type}
        check = TypeCheck(
            check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())

    def test_type_error(self):
        """Tests ``TypeCheck`` on error validation results

        Test-Purpose:
            Tests that a non-ifc instance that without the `is_a` method,
            finishs in a `error` validation information.

        Under Test:
            * ``TypeCheck``
            * implicit: ``ValidationInformation``

        Given:
            * instance: Mock Instance without the method `is_a`
            * expected_type: The type `IfcWindow` of the ifc instance
            * path_result: The `instance`
            * constraint: The type constraint to check.
              Using `expected_type`

        Expected:
            validation information with ``ValidationResult.ERROR``

        Comment:
            Usage of ``MicroMock`` to represent an instance not of type entity_instance"""
        instance = MicroMock(
            Name="IfcMock",
            GlobalId="IfcMockId"
        )
        expected_type = "IfcWindow"
        path_result = instance
        expected_result = ValidationInformation()
        expected_result.message = (f"path_result {str(path_result)} is "
                                   f"not of type entity_instance of ifcopenshell")
        expected_result.validation_result = ValidationResult.ERROR
        check_definition = {"type": expected_type}
        check = TypeCheck(
            check_definition, path_result, instance)
        self.assertEqual(expected_result, check.validate())

    def test_type_check_invalid_keyword(self):
        """Tests ``TypeCheck`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{type}`

        Under Test:
            * ``TypeCheck``

        Given:
            * `ifc_instance`: Mock Ifc Instance
            * `path_result`: "value1"
            * `constraint_check`: {"": "nonexisting"} and {"nottype": "nonexisting"}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and "nottype"

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        path_result = "value1"
        type_check = {"": "IfcMock"}
        self.assertRaises(ValueError, TypeCheck,
                          type_check, path_result, ifc_instance)
        type_check = {"nottype": "IfcMock"}
        self.assertRaises(ValueError, TypeCheck,
                          type_check, path_result, ifc_instance)

    def test_type_check_invalid_attribute(self):
        """Tests ``TypeCheck`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{type}`

        Under Test:
            * ``TypeCheck.validate``

        Given:
            * `ifc_instance`: Mock Ifc Instance
            * `path_result`: "value1"
            * `constraint_check`: {"type": ""} and {"type": None}

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
        type_check = {"type": ""}
        self.assertRaises(ValueError, TypeCheck,
                          type_check, path_result, ifc_instance)
        type_check = {"type": None}
        self.assertRaises(ValueError, TypeCheck,
                          type_check, path_result, ifc_instance)

    def test_type_yaml_keys(self):
        """Tests ``TypeCheck`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``TypeCheck`` won't change

        Under Test:
            * ``TypeCheck.yaml_keys``

        Given:
            * ``TypeCheck``

        Expected:
            The `yaml_keys` of ``TypeCheck`` is 'type'"""
        self.assertEqual(("type",), TypeCheck.get_yaml_keys())

    def test_type_constraint_get_constraint_check(self):
        """Tests ``config.get_constraint_check`` on applying the constraint check correctly.

        Test-Purpose:
            Tests that the constraint check ``TypeCheck``
            validated correctly on the actual value

        Under Test:
            * ``config.get_constraint_check``

        Given:
            * `ifc_instance`: Object of ``IfcInstanceMock``
            * dict of type constraint check

        Expected:
            That the constraint check ``TypeCheck``
            get validated on the `path_result` is a valid validation information

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="IfcWindow"
        )
        expected_type = "IfcWindow"
        path_result = ifc_instance
        expected_result = ValidationInformation()
        expected_result.message = f"type of {str(path_result)} as expected {str(expected_type)}."
        expected_result.validation_result = ValidationResult.VALID
        check_definition = {"type": expected_type}
        check = config.get_constraint_check(
            check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())
