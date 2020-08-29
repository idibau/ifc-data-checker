"""In Check Unit Test Suite"""
from ifc_data_checker import config
from ifc_data_checker.constraint_checks import InCheck
from ifc_data_checker.validation import ValidationInformation
from ifc_data_checker.validation import ValidationResult

from tests.constraint_checks.constraint_check_test import TestConstraintCheck
from tests.helpers import IfcInstanceMock


class TestInCheck(TestConstraintCheck.TestParameterValidation):
    """Test In Constraint"""

    constraint_check_class = InCheck
    default_path_result = "three"
    default_constraint = {"in": ["one", "two", "three", "four"]}

    def test_in_valid_str(self):
        """Tests ``InCheck`` on valid validation results. Type ``str``

        Test-Purpose:
            Tests that a valid ifc instance finishs in a `valid` validation information

        Under Test:
            * ``InCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `valid_value`: The testing value of type ``str``
            * `path_result`: The result of applying `path operators` on the ifc instance.
              is `valid_value`.
            * `constraint_check`: The in constraint to check.
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
        valid_value = "three"
        path_result = valid_value
        expected_result = ValidationInformation()
        expected_result.message = str(valid_value) + " is allowed"
        expected_result.validation_result = ValidationResult.VALID
        check_definition = {"in": ["one", "two", valid_value, "four"]}
        check = InCheck(check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())

    def test_in_valid_int(self):
        """Tests ``InCheck`` on valid validation results. Type ``int``

        Test-Purpose:
            Tests that a valid ifc instance finishs in a `valid` validation information

        Under Test:
            * ``InCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `valid_value`: The testing value of type ``int``
            * `path_result`: The result of applying `path operators` on the ifc instance.
              Is `valid_value`.
            * `constraint_check`: The in constraint to check.
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
        valid_value = 3
        path_result = valid_value
        expected_result = ValidationInformation()
        expected_result.message = str(valid_value) + " is allowed"
        expected_result.validation_result = ValidationResult.VALID
        check_definition = {"in": [1, 2, valid_value, 4]}
        check = InCheck(check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())

    def test_in_error_str(self):
        """Tests ``InCheck`` on error validation results. Type ``str``

        Test-Purpose:
            Tests that an invalid ifc instance finishs in a `error` validation information

        Under Test:
            * ``InCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `valid_value`: The testing value of type ``str``
            * `path_result`: The result of applying `path operators` on the ifc instance.
            * `constraint_check`: The in constraint to check.
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
        path_result = "six"
        expected_result = ValidationInformation()
        expected_result.message = "validation in error - allowed: " + \
            "['one', 'two', 'three', 'four'], actual: " + str(path_result)
        expected_result.validation_result = ValidationResult.FAILED
        check_definition = {"in": ["one", "two", "three", "four"]}
        check = InCheck(check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())

    def test_in_error_int(self):
        """Tests ``InCheck`` on error validation results. Type ``int``

        Test-Purpose:
            Tests that an invalid ifc instance finishs in a `error` validation information

        Under Test:
            * ``InCheck.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `valid_value`: The testing value of type ``int``
            * `path_result`: The result of applying `path operators` on the ifc instance.
            * `constraint_check`: The in constraint to check.
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
        path_result = 6
        expected_result = ValidationInformation()
        expected_result.message = "validation in error - allowed: [1, 2, 3, 4]" + \
            ", actual: " + str(path_result)
        expected_result.validation_result = ValidationResult.FAILED
        check_definition = {"in": [1, 2, 3, 4]}
        check = InCheck(check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())

    def test_in_check_invalid_keyword(self):
        """Tests ``InCheck`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{in}`

        Under Test:
            * ``InCheck.validate``

        Given:
            * `ifc_instance`: Mock Ifc Instance
            * `path_result`: "value1"
            * `constraint_check`:
            {"": ["one", "two", "three"]} and {"notin": ["one", "two", "three"]}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and "notin"

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        path_result = "value1"
        in_check = {"": ["one", "two", "three"]}
        self.assertRaises(ValueError, InCheck,
                          in_check, path_result, ifc_instance)
        in_check = {"notin": ["one", "two", "three"]}
        self.assertRaises(ValueError, InCheck,
                          in_check, path_result, ifc_instance)

    def test_in_check_invalid_attribute(self):
        """Tests ``InCheck`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{in}`

        Under Test:
            * ``InCheck.validate``

        Given:
            * `ifc_instance`: Mock Ifc Instance
            * `path_result`: "value1"
            * `constraint_check`:
            {"in": ""} and {"notin": None}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and None

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        path_result = "value1"
        in_check = {"in": ""}
        self.assertRaises(ValueError, InCheck,
                          in_check, path_result, ifc_instance)
        in_check = {"in": None}
        self.assertRaises(ValueError, InCheck,
                          in_check, path_result, ifc_instance)

    def test_in_yaml_keys(self):
        """Tests ``InCheck`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``InCheck`` won't change

        Under Test:
            * ``InCheck.yaml_keys``

        Given:
            * ``InCheck``

        Expected:
            The `yaml_keys` of ``InCheck`` is 'in'"""
        self.assertEqual(("in",), InCheck.get_yaml_keys())

    def test_in_constraint_get_constraint_check(self):
        """Tests ``config.get_constraint_check`` on getting the constraint check correctly.

        Test-Purpose:
            Tests that the constraint check ``InCheck``
            validated correctly on the actual value

        Under Test:
            * ``config.get_constraint_check``

        Given:
            * `ifc_instance`: Object of ``IfcInstanceMock``
            * dict of in constraint check

        Expected:
            That the constraint check ``InCheck``
            get validated on the `path_result` is a valid validation information

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        valid_value = "three"
        path_result = valid_value
        expected_result = ValidationInformation()
        expected_result.message = str(valid_value) + " is allowed"
        expected_result.validation_result = ValidationResult.VALID
        check_definition = {"in": ["one", "two", valid_value, "four"]}
        check = config.get_constraint_check(
            check_definition, path_result, ifc_instance)
        self.assertEqual(expected_result, check.validate())
