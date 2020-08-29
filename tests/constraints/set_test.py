"""Set Combination Unit Test Suite"""
from ifc_data_checker.constraints import Constraint
from ifc_data_checker import config
from ifc_data_checker.constraints import SetGroup
from ifc_data_checker.validation import ValidationInformation

from tests.constraints.constraint_component_test import TestConstraintComponent

from tests.helpers import IfcInstanceMock


class TestSetConstraint(TestConstraintComponent.TestParameterValidation):
    """Test Set Constraint"""

    constraint_component_class = SetGroup
    default_constraint_component = {"set": []}

    def test_set_group_valid(self):
        """Tests ``SetGroup`` on valid validation results.

        Test-Purpose:
            Tests that a valid ifc instance finishs in a `valid` validation information

        Under Test:
            * ``SetGroup.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `instance_name`: "IfcMock"
            * `set_group`: The set constraint group

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        instance_name = "IfcMock"
        ifc_instance = IfcInstanceMock(
            Name=instance_name,
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        # definitions
        constraint_definition = {
            "path": [{"attribute": "Name"}], "check": {"equals": instance_name}}
        set_group_definition = {
            "set": [constraint_definition]}
        # expected
        expected_validation_information = ValidationInformation()
        expected_validation_information.set_valid(
            instance_name + " as expected")
        expected_constraint = Constraint(
            constraint_definition, ifc_instance)
        expected_constraint.validation_information = expected_validation_information
        expected_constraint.path_result = instance_name
        expected_group = SetGroup(set_group_definition, ifc_instance)
        expected_group.validation_information.set_valid(
            "set group: ValidationResult.VALID: 1 of 1 constraints are valid.")
        expected_group.validated_constraints.append(expected_constraint)
        # test
        set_group = SetGroup(set_group_definition, ifc_instance)
        set_group.validate()
        self.assertEqual(expected_group, set_group)

    def test_set_group_failed(self):
        """Tests ``SetGroup`` on failed validation results.

        Test-Purpose:
            Tests that a invalid ifc instance finishs in a `failed` validation information

        Under Test:
            * ``SetGroup.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `instance_name`: "IfcMock"
            * `set_group`: The set constraint group

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        instance_name = "IfcMock"
        ifc_instance = IfcInstanceMock(
            Name=instance_name,
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        # definitions
        constraint_definition = {
            "path": [{"attribute": "Name"}], "check": {"equals": "Something other"}}
        set_group_definition = {
            "set": [constraint_definition]}
        # expected
        expected_validation_information = ValidationInformation()
        expected_validation_information.set_failed(
            f"validation equals failed - expected: Something other, actual: {instance_name}")
        expected_constraint = Constraint(
            constraint_definition, ifc_instance)
        expected_constraint.validation_information = expected_validation_information
        expected_constraint.path_result = instance_name
        expected_group = SetGroup(set_group_definition, ifc_instance)
        expected_group.validation_information.set_failed(
            "set group: ValidationResult.FAILED: 0 of 1 constraints are valid.")
        expected_group.validated_constraints.append(expected_constraint)
        # test
        set_group = SetGroup(set_group_definition, ifc_instance)
        set_group.validate()
        self.assertEqual(expected_group, set_group)

    def test_set_group_invalid_keyword(self):
        """Tests ``SetGroup`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{set}`

        Under Test:
            * ``SetGroup.validate``

        Given:
            * instances: List of Mock Instances
            * set_group: {"": "nonexisting"} and {"notset": "nonexisting"}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and "notset"

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        set_group_definition = {
            "": [{"path": [{"attribute": "Name"}], "check": {"equals": "IfcMock"}}]}
        self.assertRaises(ValueError, SetGroup,
                          set_group_definition, tuple([ifc_instance]))

        set_group_definition = {"notset": [
            {"path": [{"attribute": "Name"}], "check": {"equals": "IfcMock"}}]}
        self.assertRaises(ValueError, SetGroup,
                          set_group_definition, tuple([ifc_instance]))

    def test_set_group_yaml_keys(self):
        """Tests ``SetGroup`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``SetGroup`` won't change

        Under Test:
            * ``SetGroup.yaml_keys``

        Given:
            * ``SetGroup``

        Expected:
            The `yaml_keys` of ``SetGroup`` is 'set'"""
        self.assertEqual(("set",), SetGroup.get_yaml_keys())

    def test_set_group_get_constraint(self):
        """Tests ``config.get_constraint`` on applying the constraint group correctly.

        Test-Purpose:
            Tests that the constraint group ``SetGroup``
            applied correctly on the actual value

        Under Test:
            * ``config.get_constraint``

        Given:
            * `ifc_instance`: Object of ``IfcInstanceMock``
            * dict of set constraint group:
            using path operator `attribute` and constraint check `equals`

        Expected:
            That the constraint group ``SetGroup``
            get validated on the list of `ifc_instance` and
            that the `path_result` is a valid validation information

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        instance_name = "IfcMock"
        ifc_instance = IfcInstanceMock(
            Name=instance_name,
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        # definitions
        constraint_definition = {
            "path": [{"attribute": "Name"}],
            "check": {"equals": instance_name}}
        set_group_definition = {
            "set": [constraint_definition]}
        # expected
        expected_constraint_group = SetGroup(
            set_group_definition, ifc_instance)
        validation_information = ValidationInformation()
        validation_information.set_valid(instance_name + " as expected")
        validated_constraint = Constraint(
            constraint_definition, ifc_instance)
        validated_constraint.validation_information = validation_information
        validated_constraint.path_result = instance_name
        expected_constraint_group.validated_constraints.append(
            validated_constraint)
        expected_group_validation_information = ValidationInformation()
        expected_group_validation_information.set_valid(
            "set group: ValidationResult.VALID: 1 of 1 constraints are valid.")
        expected_constraint_group.validation_information = expected_group_validation_information
        # test
        set_group = config.get_constraint(
            set_group_definition, ifc_instance)
        set_group.validate()
        self.assertEqual(expected_constraint_group,
                         set_group)
