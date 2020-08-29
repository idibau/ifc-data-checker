"""Equals Check Unit Test Suite"""
from ifc_data_checker import config
from ifc_data_checker.constraint_checks import EqualsCheck
from ifc_data_checker.validation import ValidationInformation
from ifc_data_checker.validation import ValidationResult

from tests.constraint_checks.constraint_check_test import TestConstraintCheck
from tests.helpers import IfcInstanceMock


class TestEqualsCheck(TestConstraintCheck.TestParameterValidation):
    """Test Equals Constraint"""

    constraint_check_class = EqualsCheck
    default_path_result = "value1"
    default_constraint = {"equals": "value1"}

    def test_equals_valid_str(self):
        """Tests ``EqualsCheck`` on valid validation results. Type ``str``

        Test-Purpose:
            Tests that a valid ifc instance finishs in a `valid` validation information

        Under Test:
            * ``EqualsCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * valid_value: The testing value of type ``str``
            * actual value: The result of applying `path operators` on the ifc instance.
              Equals `valid_value`.
            * equals_check_definition: The equals constraint to check.
              Using `valid_value`

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        valid_value = "value1"
        path_result = valid_value
        expected_result = ValidationInformation()
        expected_result.message = str(valid_value) + " as expected"
        expected_result.validation_result = ValidationResult.VALID
        equals_check_definition = {"equals": valid_value}
        equals_check = EqualsCheck(
            equals_check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, equals_check.validate())

    def test_equals_valid_int(self):
        """Tests ``EqualsCheck`` on valid validation results. Type ``int``

        Test-Purpose:
            Tests that a valid ifc instance finishs in a `valid` validation information

        Under Test:
            * ``EqualsCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * valid_value: The testing value of type ``int``
            * actual value: The result of applying `path operators` on the ifc instance.
              Equals `valid_value`.
            * equals_check_definition: The equals constraint to check.
              Using `valid_value`

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        valid_value = 42
        path_result = valid_value
        expected_result = ValidationInformation()
        expected_result.message = str(valid_value) + " as expected"
        expected_result.validation_result = ValidationResult.VALID
        equals_check_definition = {"equals": valid_value}
        equals_check = EqualsCheck(
            equals_check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, equals_check.validate())

    def test_equals_valid_float(self):
        """Tests ``EqualsCheck`` on valid validation results. Type ``float``

        Test-Purpose:
            Tests that a valid ifc instance finishs in a `valid` validation information

        Under Test:
            * ``EqualsCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * valid_value: The testing value of type ``float``
            * actual value: The result of applying `path operators` on the ifc instance.
              Equals `valid_value`.
            * equals_check_definition: The equals constraint to check.
              Using `valid_value`

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        valid_value = 4.2
        path_result = valid_value
        expected_result = ValidationInformation()
        expected_result.message = str(valid_value) + " as expected"
        expected_result.validation_result = ValidationResult.VALID
        equals_check_definition = {"equals": valid_value}
        equals_check = EqualsCheck(
            equals_check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, equals_check.validate())

    def test_equals_error_str(self):
        """Tests ``EqualsCheck`` on error validation results. Type ``str``

        Test-Purpose:
            Tests that an invalid ifc instance finishs in a `error` validation information

        Under Test:
            * ``EqualsCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * valid_value: The testing value of type ``str``
            * actual value: The result of applying `path operators` on the ifc instance.
            * equals_check_definition: The equals constraint to check.
              Using `valid_value`

        Expected:
            validation information with ``ValidationResult.FAILED``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        valid_value = "value1"
        path_result = "othervalue"
        expected_result = ValidationInformation()
        expected_result.message = "validation equals failed - expected: " + \
            str(valid_value) + ", actual: " + str(path_result)
        expected_result.validation_result = ValidationResult.FAILED
        equals_check_definition = {"equals": valid_value}
        equals_check = EqualsCheck(
            equals_check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, equals_check.validate())

    def test_equals_error_int(self):
        """Tests ``EqualsCheck`` on error validation results. Type ``int``

        Test-Purpose:
            Tests that an invalid ifc instance finishs in a `error` validation information

        Under Test:
            * ``EqualsCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * valid_value: The testing value of type ``int``
            * actual value: The result of applying `path operators` on the ifc instance.
            * equals_check_definition: The equals constraint to check.
              Using `valid_value`

        Expected:
            validation information with ``ValidationResult.FAILED``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        valid_value = 42
        path_result = 51
        expected_result = ValidationInformation()
        expected_result.message = "validation equals failed - expected: " + \
            str(valid_value) + ", actual: " + str(path_result)
        expected_result.validation_result = ValidationResult.FAILED
        equals_check_definition = {"equals": valid_value}
        equals_check = EqualsCheck(
            equals_check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, equals_check.validate())

    def test_equals_error_float(self):
        """Tests ``EqualsCheck`` on error validation results. Type ``float``

        Test-Purpose:
            Tests that an invalid ifc instance finishs in a `error` validation information

        Under Test:
            * ``EqualsCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * valid_value: The testing value of type ``float``
            * actual value: The result of applying `path operators` on the ifc instance.
            * constraint: The equals constraint to check.
              Using `valid_value`

        Expected:
            validation information with ``ValidationResult.FAILED``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        valid_value = 4.2
        path_result = 5.1
        expected_result = ValidationInformation()
        expected_result.message = "validation equals failed - expected: " + \
            str(valid_value) + ", actual: " + str(path_result)
        expected_result.validation_result = ValidationResult.FAILED
        equals_check_definition = {"equals": valid_value}
        equals_check = EqualsCheck(
            equals_check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, equals_check.validate())

    def test_equals_check_invalid_keyword(self):
        """Tests ``EqualsCheck`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{equals}`

        Under Test:
            * ``EqualsCheck``

        Given:
            * `ifc_instance`: Mock Ifc Instance
            * `path_result`: "value1"
            * `equals_check`: {"": "nonexisting"} and {"notequals": "nonexisting"}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and "notequals"

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        path_result = "value1"
        equals_check = {"": "IfcMock"}
        self.assertRaises(ValueError, EqualsCheck,
                          equals_check, path_result, ifc_instance)
        equals_check = {"notequals": "IfcMock"}
        self.assertRaises(ValueError, EqualsCheck,
                          equals_check, path_result, ifc_instance)

    def test_equals_check_invalid_attribute(self):
        """Tests ``EqualsCheck`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{equals}`

        Under Test:
            * ``EqualsCheck``

        Given:
            * `ifc_instance`: Mock Ifc Instance
            * `path_result`: "value1"
            * `equals_check`: {"equals": ""} and {"equals": None}

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
        equals_check = {"equals": ""}
        self.assertRaises(ValueError, EqualsCheck,
                          equals_check, path_result, ifc_instance)
        equals_check = {"equals": None}
        self.assertRaises(ValueError, EqualsCheck,
                          equals_check, path_result, ifc_instance)

    def test_equals_yaml_keys(self):
        """Tests ``EqualsCheck`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``EqualsCheck`` won't change

        Under Test:
            * ``EqualsCheck.yaml_keys``

        Given:
            * ``EqualsCheck``

        Expected:
            The `yaml_keys` of ``EqualsCheck`` is 'equals'"""
        self.assertEqual(("equals",), EqualsCheck.get_yaml_keys())

    def test_equals_constraint_get_constraint_check(self):
        """Tests ``config.get_constraint_check`` on applying the constraint check correctly.

        Test-Purpose:
            Tests that the constraint check ``EqualsCheck``
            validated correctly on the actual value

        Under Test:
            * ``config.get_constraint_check``

        Given:
            * `ifc_instance`: Object of ``IfcInstanceMock``
            * dict of equals constraint check

        Expected:
            That the constraint check ``EqualsCheck``
            get validated on the `path_result` is a valid validation information

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        valid_value = "value1"
        path_result = valid_value
        expected_result = ValidationInformation()
        expected_result.message = str(valid_value) + " as expected"
        expected_result.validation_result = ValidationResult.VALID
        equals_check = {"equals": valid_value}
        check = config.get_constraint_check(
            equals_check, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())
