"""And Combination Unit Test Suite"""
from ifc_data_checker.constraints import Constraint
from ifc_data_checker import config
from ifc_data_checker.constraints import AndGroup
from ifc_data_checker.validation import ValidationInformation

from tests.constraints.constraint_component_test import TestConstraintComponent

from tests.helpers import IfcInstanceMock


class TestAndConstraint(TestConstraintComponent.TestParameterValidation):
    """Test And Constraint"""

    constraint_component_class = AndGroup
    default_constraint_component = {"and": []}

    def test_and_group_valid(self):
        """Tests ``AndGroup`` on valid validation results.

        Test-Purpose:
            Tests that a valid ifc instance finishs in a `valid` validation information.
            Validating 2 different constraints on the ifc instance, which both are valid.
            Because of the and combination of both results,
            the validation information of the constraint group results `valid`.

        Under Test:
            * ``AndGroup.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `instance_name`: "IfcMock"
            * `and_group`: The and constraint group

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        instance_name = "IfcMock"
        global_id = "IfcMockId"
        ifc_instance = IfcInstanceMock(
            Name=instance_name,
            GlobalId=global_id,
            ifc_type="MockType"
        )
        # definitions
        constraint_definition_one = {
            "path": [{"attribute": "Name"}], "check": {"equals": instance_name}}
        constraint_definition_two = {
            "path": [{"attribute": "GlobalId"}], "check": {"equals": global_id}}
        and_group_definition = {
            "and": [constraint_definition_one, constraint_definition_two]}
        # expected
        expected_validation_information_one = ValidationInformation()
        expected_validation_information_one.set_valid(
            instance_name + " as expected")
        expected_constraint_one = Constraint(
            constraint_definition_one, ifc_instance)
        expected_constraint_one.validation_information = expected_validation_information_one
        expected_constraint_one.path_result = instance_name
        expected_validation_information_two = ValidationInformation()
        expected_validation_information_two.set_valid(
            global_id + " as expected")
        expected_constraint_two = Constraint(
            constraint_definition_two, ifc_instance)
        expected_constraint_two.validation_information = expected_validation_information_two
        expected_constraint_two.path_result = global_id
        expected_group_validation_information = ValidationInformation()
        expected_group_validation_information.set_valid(
            "and group: ValidationResult.VALID: Each of 2 constraints are valid.")
        expected_group = AndGroup(and_group_definition, ifc_instance)
        expected_group.validation_information = expected_group_validation_information
        expected_group.validated_constraints = [
            expected_constraint_one, expected_constraint_two]
        # test
        and_group = AndGroup(and_group_definition, ifc_instance)
        and_group.validate()
        self.assertEqual(expected_group, and_group)

    def test_and_group_constraint_second_invalid(self):
        """Tests ``AndGroup`` on invalid validation results.

        Test-Purpose:
            Tests that a invalid ifc instance finishs in a `invalid` validation information.
            Validating 2 different constraints on the ifc instance:
            One is `valid` the other is `invalid`.
            Because of the and combination of the 2 constraints,
            the validation information of the constraint group results `invalid`.
            To be `valid`, 2 of 2 constraints need to be valid.

        Under Test:
            * ``AndGroup.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `instance_name`: "IfcMock"
            * `and_group`: The and constraint group

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        instance_name = "IfcMock"
        global_id = "IfcMockId"
        ifc_instance = IfcInstanceMock(
            Name=instance_name,
            GlobalId="Invalid Id",
            ifc_type="MockType"
        )
        # definitions
        constraint_definition_one = {
            "path": [{"attribute": "Name"}], "check": {"equals": instance_name}}
        constraint_definition_two = {
            "path": [{"attribute": "GlobalId"}], "check": {"equals": global_id}}
        and_group_definition = {
            "and": [constraint_definition_one, constraint_definition_two]}
        # expected
        expected_validation_information_one = ValidationInformation()
        expected_validation_information_one.set_valid(
            instance_name + " as expected")
        expected_constraint_one = Constraint(
            constraint_definition_one, ifc_instance)
        expected_constraint_one.validation_information = expected_validation_information_one
        expected_constraint_one.path_result = instance_name
        expected_validation_information_two = ValidationInformation()
        expected_validation_information_two.set_failed(
            "validation equals failed - expected: IfcMockId, actual: Invalid Id")
        expected_constraint_two = Constraint(
            constraint_definition_two, ifc_instance)
        expected_constraint_two.validation_information = expected_validation_information_two
        expected_constraint_two.path_result = "Invalid Id"
        expected_group_validation_information = ValidationInformation()
        expected_group_validation_information.set_failed(
            "and group: ValidationResult.FAILED: 1 of 2 constraints are valid.")
        expected_group = AndGroup(and_group_definition, ifc_instance)
        expected_group.validated_constraints = [
            expected_constraint_one, expected_constraint_two]
        expected_group.validation_information = expected_group_validation_information
        # test
        and_group = AndGroup(and_group_definition, ifc_instance)
        and_group.validate()
        self.assertEqual(expected_group, and_group)

    def test_and_group_constraint_first_invalid(self):
        """Tests ``AndGroup`` on invalid validation results.

        Test-Purpose:
            Tests that a invalid ifc instance finishs in a `invalid` validation information.
            Validating 2 different constraints on the ifc instance:
            One is `valid` the other is `invalid`.
            Because of the and combination of the 2 constraints,
            the validation information of the constraint group results `invalid`.
            To be `valid`, 2 of 2 constraints need to be valid.

        Under Test:
            * ``AndGroup.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `instance_name`: "IfcMock"
            * `and_group`: The and constraint group

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        instance_name = "IfcMock"
        global_id = "IfcMockId"
        ifc_instance = IfcInstanceMock(
            Name=instance_name,
            GlobalId="Invalid Id",
            ifc_type="MockType"
        )
        # definitions
        constraint_definition_one = {
            "path": [{"attribute": "Name"}], "check": {"equals": instance_name}}
        constraint_definition_two = {
            "path": [{"attribute": "GlobalId"}], "check": {"equals": global_id}}
        and_group_definition = {
            "and": [constraint_definition_two, constraint_definition_one]}
        # expected
        expected_validation_information_one = ValidationInformation()
        expected_validation_information_one.set_valid(
            instance_name + " as expected")
        expected_constraint_one = Constraint(
            constraint_definition_one, ifc_instance)
        expected_constraint_one.validation_information = expected_validation_information_one
        expected_constraint_one.path_result = instance_name
        expected_validation_information_two = ValidationInformation()
        expected_validation_information_two.set_failed(
            "validation equals failed - expected: IfcMockId, actual: Invalid Id")
        expected_constraint_two = Constraint(
            constraint_definition_two, ifc_instance)
        expected_constraint_two.validation_information = expected_validation_information_two
        expected_constraint_two.path_result = "Invalid Id"
        expected_group_validation_information = ValidationInformation()
        expected_group_validation_information.set_failed(
            "and group: ValidationResult.FAILED: 1 of 2 constraints are valid.")
        expected_group = AndGroup(and_group_definition, ifc_instance)
        expected_group.validated_constraints = [
            expected_constraint_two, expected_constraint_one]
        expected_group.validation_information = expected_group_validation_information
        # test
        and_group = AndGroup(and_group_definition, ifc_instance)
        and_group.validate()
        self.assertEqual(expected_group, and_group)

    def test_and_group_constraint_both_invalid(self):
        """Tests ``AndGroup`` on invalid validation results.

        Test-Purpose:
            Tests that a invalid ifc instance finishs in a `invalid` validation information.
            Validating 2 different constraints on the ifc instance:
            Both constraints are `invalid` on this ifc instance.
            This results in an `invalid` group validation result.
            To result in a `valid` group validation result, 2 of 2 constraints need to be valid.

        Under Test:
            * ``AndGroup.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `instance_name`: "IfcMock"
            * `and_group`: The and constraint group

        Expected:
            validation information with ``ValidationResult.VALID``

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        instance_name = "IfcMock"
        global_id = "IfcMockId"
        ifc_instance = IfcInstanceMock(
            Name="No Name",
            GlobalId="Invalid Id",
            ifc_type="MockType"
        )
        # definitions
        constraint_definition_one = {
            "path": [{"attribute": "Name"}], "check": {"equals": instance_name}}
        constraint_definition_two = {
            "path": [{"attribute": "GlobalId"}], "check": {"equals": global_id}}
        and_group_definition = {
            "and": [constraint_definition_one, constraint_definition_two]}
        # expected
        expected_validation_information_one = ValidationInformation()
        expected_validation_information_one.set_failed(
            "validation equals failed - expected: IfcMock, actual: No Name")
        expected_constraint_one = Constraint(
            constraint_definition_one, ifc_instance)
        expected_constraint_one.validation_information = expected_validation_information_one
        expected_constraint_one.path_result = "No Name"
        expected_validation_information_two = ValidationInformation()
        expected_validation_information_two.set_failed(
            "validation equals failed - expected: IfcMockId, actual: Invalid Id")
        expected_constraint_two = Constraint(
            constraint_definition_two, ifc_instance)
        expected_constraint_two.validation_information = expected_validation_information_two
        expected_constraint_two.path_result = "Invalid Id"
        expected_group_validation_information = ValidationInformation()
        expected_group_validation_information.set_failed(
            "and group: ValidationResult.FAILED: 0 of 2 constraints are valid.")
        expected_group = AndGroup(and_group_definition, ifc_instance)
        expected_group.validated_constraints = [
            expected_constraint_one, expected_constraint_two]
        expected_group.validation_information = expected_group_validation_information
        # test
        and_group = AndGroup(and_group_definition, ifc_instance)
        and_group.validate()
        self.assertEqual(expected_group, and_group)

    def test_and_group_invalid_keyword(self):
        """Tests ``AndGroup`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{and}`

        Under Test:
            * ``AndGroup.validate``

        Given:
            * instances: List of Mock Instances
            * and_group: {"": "nonexisting"} and {"notand": "nonexisting"}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and "notand"

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        and_group_definition = {
            "": [{"path": [{"attribute": "Name"}], "check": {"equals": "IfcMock"}}]}
        self.assertRaises(ValueError, AndGroup,
                          and_group_definition, tuple([ifc_instance]))

        and_group_definition = {"notand": [
            {"path": [{"attribute": "Name"}], "check": {"equals": "IfcMock"}}]}
        self.assertRaises(ValueError, AndGroup,
                          and_group_definition, tuple([ifc_instance]))

    def test_and_group_yaml_keys(self):
        """Tests ``AndGroup`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``AndGroup`` won't change

        Under Test:
            * ``AndGroup.yaml_keys``

        Given:
            * ``AndGroup``

        Expected:
            The `yaml_keys` of ``AndGroup`` is 'and'"""
        self.assertEqual(("and",), AndGroup.get_yaml_keys())

    def test_and_group_get_constraint(self):
        """Tests ``config.get_constraint`` on applying the constraint group correctly.

        Test-Purpose:
            Tests that the constraint group ``AndGroup``
            applied correctly on the actual value

        Under Test:
            * ``config.get_constraint``
            * implicit ``_get_constraint_group``
            * implicit ``all_constraint_groups``

        Given:
            * `ifc_instance`: Object of ``IfcInstanceMock``
            * dict of and constraint group:
            using path operator `attribute` and constraint check `equals`

        Expected:
            That the constraint group ``AndGroup``
            get validated on the list of `ifc_instance` and
            that the `path_result` is a valid validation information

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        instance_name = "IfcMock"
        global_id = "IfcMockId"
        ifc_instance = IfcInstanceMock(
            Name=instance_name,
            GlobalId=global_id,
            ifc_type="MockType"
        )
        # definitions
        constraint_definition_one = {
            "path": [{"attribute": "Name"}], "check": {"equals": instance_name}}
        and_group_definition = {
            "and": [constraint_definition_one]}
        # expected
        expected_validation_information_one = ValidationInformation()
        expected_validation_information_one.set_valid(
            instance_name + " as expected")
        expected_constraint_one = Constraint(
            constraint_definition_one, ifc_instance)
        expected_constraint_one.validation_information = expected_validation_information_one
        expected_constraint_one.path_result = instance_name
        expected_group_validation_information = ValidationInformation()
        expected_group_validation_information.set_valid(
            "and group: ValidationResult.VALID: Each of 1 constraints are valid.")
        expected_group = AndGroup(and_group_definition, ifc_instance)
        expected_group.validation_information = expected_group_validation_information
        expected_group.validated_constraints = [
            expected_constraint_one]
        # test
        and_group = config.get_constraint(and_group_definition, ifc_instance)
        and_group.validate()
        self.assertEqual(expected_group, and_group)
