"""Not Check Unit Test Suite"""
from ifc_data_checker import config
from ifc_data_checker.constraint_checks import NotCheck
from ifc_data_checker.validation import ValidationInformation
from ifc_data_checker.validation import ValidationResult

from tests.constraint_checks.constraint_check_test import TestConstraintCheck
from tests.helpers import IfcInstanceMock


class TestNotCheck(TestConstraintCheck.TestParameterValidation):
    """Test Not Constraint"""

    constraint_check_class = NotCheck
    default_path_result = "value1"
    default_constraint = {"not": {"equals": "value1"}}

    def test_not_valid(self):
        """Tests ``NotCheck`` on valid validation results.

        Test-Purpose:
            Tests that a FAILED check finishes in a VALID validation information result.

        Under Test:
            * ``NotCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * valid_value: The testing value of type ``str``
            * path_result: The result of applying `path operators` on the ifc instance.
            * not_check_definition: The not constraint to check.
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
        path_result = "othervalue"
        expected_result = ValidationInformation()
        expected_result.message = ("check FAILED as expected, message: "
                                   f"validation equals failed - expected: {valid_value}, "
                                   f"actual: {path_result}")
        expected_result.validation_result = ValidationResult.VALID
        not_check_definition = {"not": {"equals": valid_value}}
        not_check = NotCheck(
            not_check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, not_check.validate())

    def test_not_failed(self):
        """Tests ``NotCheck`` on failed validation information result.

        Test-Purpose:
            Tests that a VALID check finishes in a FAILED validation information result.

        Under Test:
            * ``NotCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * ifc_instance: IFC Mock Instance
            * valid_value: The testing value of type ``str``
            * path_result: The result of applying `path operators` on the ifc instance.
            * not_check_definition: The not constraint to check.
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
        path_result = valid_value
        expected_result = ValidationInformation()
        expected_result.message = ("check was VALID, but expected FAILED, message: "
                                   f"{valid_value} as expected")
        expected_result.validation_result = ValidationResult.FAILED
        not_check_definition = {"not": {"equals": valid_value}}
        not_check = NotCheck(
            not_check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, not_check.validate())

    def test_not_check_invalid_keyword(self):
        """Tests ``NotCheck`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{not}`

        Under Test:
            * ``NotCheck``

        Given:
            * `ifc_instance`: Mock Ifc Instance
            * `path_result`: "value1"
            * `not_check`: {"": "nonexisting"} and {"notnot": "nonexisting"}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and "notnot"

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        path_result = "value1"
        not_check = {"": "IfcMock"}
        self.assertRaises(ValueError, NotCheck,
                          not_check, path_result, ifc_instance)
        not_check = {"notnot": "IfcMock"}
        self.assertRaises(ValueError, NotCheck,
                          not_check, path_result, ifc_instance)

    def test_not_check_invalid_attribute(self):
        """Tests ``NotCheck`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{not}`

        Under Test:
            * ``NotCheck``

        Given:
            * `ifc_instance`: Mock Ifc Instance
            * `path_result`: "value1"
            * `not_check`: {"not": ""} and {"not": None}

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
        not_check = {"not": ""}
        self.assertRaises(ValueError, NotCheck,
                          not_check, path_result, ifc_instance)
        not_check = {"not": None}
        self.assertRaises(ValueError, NotCheck,
                          not_check, path_result, ifc_instance)

    def test_not_yaml_keys(self):
        """Tests ``NotCheck`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``NotCheck`` won't change

        Under Test:
            * ``NotCheck.yaml_keys``

        Given:
            * ``NotCheck``

        Expected:
            The `yaml_keys` of ``NotCheck`` is 'not'"""
        self.assertEqual(("not",), NotCheck.get_yaml_keys())

    def test_not_get_constraint_check(self):
        """Tests ``config.get_constraint_check`` on applying the constraint check correctly.

        Test-Purpose:
            Tests that the constraint check ``NotCheck``
            validated correctly on the actual value

        Under Test:
            * ``config.get_constraint_check``

        Given:
            * `ifc_instance`: Object of ``IfcInstanceMock``
            * dict of not constraint check

        Expected:
            That the constraint check ``NotCheck``
            get validated on the `path_result` is a valid validation information

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
        expected_result.message = ("check FAILED as expected, message: "
                                   f"validation equals failed - expected: {valid_value}, "
                                   f"actual: {path_result}")
        expected_result.validation_result = ValidationResult.VALID
        not_check_definition = {"not": {"equals": valid_value}}
        not_check = config.get_constraint_check(
            not_check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, not_check.validate())
