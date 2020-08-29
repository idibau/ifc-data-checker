"""Or Combination Unit Test Suite"""
from ifc_data_checker import config
from ifc_data_checker.constraints import Constraint
from ifc_data_checker.constraints import OrGroup
from ifc_data_checker.validation import ValidationInformation

from tests.constraints.constraint_component_test import TestConstraintComponent

from tests.helpers import IfcInstanceMock


class TestOrConstraint(TestConstraintComponent.TestParameterValidation):
    """Test Or Constraint"""

    constraint_component_class = OrGroup
    default_constraint_component = {"or": []}

    def test_or_group_valid_both(self):
        """Tests ``OrGroup`` on valid validation results.

        Test-Purpose:
            Tests that a valid ifc instance finishs in a `valid` validation information.
            Validating 2 different constraints on the ifc instance, which both are valid.
            Because of the or combination of both results,
            the validation information of the constraint group results in `valid`.

        Under Test:
            * ``OrGroup.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `instance_name`: "IfcMock"
            * `or_group`: The or constraint group

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
        or_group_definition = {
            "or": [constraint_definition_one, constraint_definition_two]}
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
            "or group: ValidationResult.VALID: 2 of 2 constraints are valid.")
        expected_group = OrGroup(or_group_definition, ifc_instance)
        expected_group.validation_information = expected_group_validation_information
        expected_group.validated_constraints = [
            expected_constraint_one, expected_constraint_two]
        # test
        or_group = OrGroup(or_group_definition, ifc_instance)
        or_group.validate()
        self.assertEqual(expected_group, or_group)

    def test_or_group_constraint_valid_first(self):
        """Tests ``OrGroup`` on invalid validation results.

        Test-Purpose:
            Validating 2 different constraints on the ifc instance:
            The first is `valid` the second is `invalid`.
            Because of the or combination of the 2 constraints,
            the validation information of the constraint group results in `valid`.

        Under Test:
            * ``OrGroup.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `instance_name`: "IfcMock"
            * `or_group`: The or constraint group

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
        or_group_definition = {
            "or": [constraint_definition_one, constraint_definition_two]}
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
        expected_group_validation_information.set_valid(
            "or group: ValidationResult.VALID: 1 of 2 constraints are valid.")
        expected_group = OrGroup(or_group_definition, ifc_instance)
        expected_group.validated_constraints = [
            expected_constraint_one, expected_constraint_two]
        expected_group.validation_information = expected_group_validation_information
        # test
        or_group = OrGroup(or_group_definition, ifc_instance)
        or_group.validate()
        self.assertEqual(expected_group, or_group)

    def test_or_group_constraint_valid_second(self):
        """Tests ``OrGroup`` on invalid validation results.

        Test-Purpose:
            Validating 2 different constraints on the ifc instance:
            The first is `invalid` the second is `valid`.
            Because of the or combination of the 2 constraints,
            the validation information of the constraint group results in `valid`.

        Under Test:
            * ``OrGroup.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `instance_name`: "IfcMock"
            * `or_group`: The or constraint group

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
        or_group_definition = {
            "or": [constraint_definition_two, constraint_definition_one]}
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
        expected_group_validation_information.set_valid(
            "or group: ValidationResult.VALID: 1 of 2 constraints are valid.")
        expected_group = OrGroup(or_group_definition, ifc_instance)
        expected_group.validated_constraints = [
            expected_constraint_two, expected_constraint_one]
        expected_group.validation_information = expected_group_validation_information
        # test
        or_group = OrGroup(or_group_definition, ifc_instance)
        or_group.validate()
        self.assertEqual(expected_group, or_group)

    def test_or_group_constraint_invalid(self):
        """Tests ``OrGroup`` on invalid validation results.

        Test-Purpose:
            Validating 2 different constraints on the ifc instance:
            Both constraints are `invalid` on this ifc instance.
            This results in an `invalid` group validation result.
            To result in a `valid` group validation result,
            at minimum one of the constraints need to be valid.

        Under Test:
            * ``OrGroup.validate``
            * implicit: ``ValidationInformation``

        Given:
            * `ifc_instance`: IFC Mock Instance
            * `instance_name`: "IfcMock"
            * `or_group`: The or constraint group

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
        or_group_definition = {
            "or": [constraint_definition_one, constraint_definition_two]}
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
            "or group: ValidationResult.FAILED: No one of 2 constraints are valid.")
        expected_group = OrGroup(or_group_definition, ifc_instance)
        expected_group.validated_constraints = [
            expected_constraint_one, expected_constraint_two]
        expected_group.validation_information = expected_group_validation_information
        # test
        or_group = OrGroup(or_group_definition, ifc_instance)
        or_group.validate()
        self.assertEqual(expected_group, or_group)

    def test_or_group_invalid_keyword(self):
        """Tests ``OrGroup`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `{or}`

        Under Test:
            * ``OrGroup.validate``

        Given:
            * instances: List of Mock Instances
            * or_group: {"": "nonexisting"} or {"notor": "nonexisting"}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" or "notor"

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType"
        )
        or_group_definition = {
            "": [{"path": [{"attribute": "Name"}], "check": {"equals": "IfcMock"}}]}
        self.assertRaises(ValueError, OrGroup,
                          or_group_definition, tuple([ifc_instance]))

        or_group_definition = {"notor": [
            {"path": [{"attribute": "Name"}], "check": {"equals": "IfcMock"}}]}
        self.assertRaises(ValueError, OrGroup,
                          or_group_definition, tuple([ifc_instance]))

    def test_or_group_yaml_keys(self):
        """Tests ``OrGroup`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``OrGroup`` won't change

        Under Test:
            * ``OrGroup.yaml_keys``

        Given:
            * ``OrGroup``

        Expected:
            The `yaml_keys` of ``OrGroup`` is 'or'"""
        self.assertEqual(("or",), OrGroup.get_yaml_keys())

    def test_or_group_get_constraint(self):
        """Tests ``config.get_constraint`` on applying the constraint group correctly.

        Test-Purpose:
            Tests that the constraint group ``OrGroup``
            applied correctly on the actual value

        Under Test:
            * ``apply_constraint_group``

        Given:
            * `ifc_instance`: Object of ``IfcInstanceMock``
            * dict of or constraint group:
            using path operator `attribute` or constraint check `equals`

        Expected:
            That the constraint group ``OrGroup``
            get validated on the list of `ifc_instance` or
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
        or_group_definition = {
            "or": [constraint_definition_one]}
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
            "or group: ValidationResult.VALID: 1 of 1 constraints are valid.")
        expected_group = OrGroup(or_group_definition, ifc_instance)
        expected_group.validation_information = expected_group_validation_information
        expected_group.validated_constraints = [
            expected_constraint_one]
        # test
        or_group = config.get_constraint(
            or_group_definition, ifc_instance)
        or_group.validate()
        self.assertEqual(expected_group, or_group)
