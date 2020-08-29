"""Filter Type Unit Test Suite"""
from ifc_data_checker.path_operators import TypeFilterPathOperator
from ifc_data_checker import config

from tests.path_operators.path_operator_test import TestPathOperator
from tests.helpers import IfcInstanceMock
from tests.helpers import MicroMock


class TestFilterType(TestPathOperator.TestParameterValidation):
    """Test Filter Type"""

    path_operator_class = TypeFilterPathOperator
    default_path_operator = {"type": "IfcMock"}

    def test_filter_type_same_instances(self):
        """Tests ``TypeFilterPathOperator`` on applying path operator correctly.

        Test-Purpose:
            Tests that each instance, which matching the typing criteria, gets filtered.

        Under Test:
            * ``TypeFilterPathOperator.apply``

        Given:
            * ifc instances: List of Mock IFC Instances, each matching the typing criteria
            * path_operator: The path operator with the typing criteria

        Expected:
            The same list as the given `ifc instances` list,
            because every instance matching the typing criteria.

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="IfcMock"
        )
        ifc_instances = [ifc_instance, ifc_instance, ifc_instance]
        path_operator = {"type": "IfcMock"}
        expected_result = ifc_instances
        operator = TypeFilterPathOperator(ifc_instances, path_operator)
        self.assertEqual(expected_result, operator.apply())

    def test_filter_type_different_instances(self):
        """Tests ``TypeFilterPathOperator`` on applying path operator correctly.

        Test-Purpose:
            Tests that each instance, which matching the typing criteria, gets filtered.

        Under Test:
            * ``TypeFilterPathOperator.apply``

        Given:
            * ifc instances: List of Mock IFC Instances,
              some matching The typing criteria, some won't
            * path_operator: The path operator with the typing criteria

        Expected:
            A filtered list with the instances matching the typing criteria only

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="IfcMock"
        )
        other_ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="OtherMock"
        )
        ifc_instances = [ifc_instance, other_ifc_instance,
                         ifc_instance, other_ifc_instance,
                         ifc_instance, other_ifc_instance]
        expected_result = [ifc_instance, ifc_instance, ifc_instance]
        path_operator = {"type": "IfcMock"}
        operator = TypeFilterPathOperator(ifc_instances, path_operator)
        self.assertEqual(expected_result, operator.apply())

    def test_filter_type_invalid_keyword(self):
        """Tests ``TypeFilterPathOperator`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `path_operator`

        Under Test:
            * ``TypeFilterPathOperator.apply``

        Given:
            * instances: List of Mock Instances
            * path_operator: {"": "nonexisting"} and {"nottype": "nonexisting"}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and "nottype"

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        instance = MicroMock(list_attribute=["string1", "string2", "string3"])
        instances = [instance, instance, instance]
        path_operator = {"": "nonexisting"}
        self.assertRaises(ValueError, TypeFilterPathOperator,
                          instances, path_operator)
        path_operator = {"nottype": "nonexisting"}
        self.assertRaises(ValueError, TypeFilterPathOperator,
                          instances, path_operator)

    def test_filter_type_invalid_attribute(self):
        """Tests ``TypeFilterPathOperator`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `path_operator`

        Under Test:
            * ``TypeFilterPathOperator.apply``

        Given:
            * instances: List of Mock Instances
            * path_operator: {"type": ""} and {"type": None}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and ``None``

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        instance = MicroMock(list_attribute=["string1", "string2", "string3"])
        instances = [instance, instance, instance]
        path_operator = {"type": ""}
        self.assertRaises(ValueError, TypeFilterPathOperator,
                          instances, path_operator)
        path_operator = {"type": None}
        self.assertRaises(ValueError, TypeFilterPathOperator,
                          instances, path_operator)

    def test_filter_type_path_operator_yaml_keys(self):
        """Tests ``TypeFilterPathOperator`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``TypeFilterPathOperator`` won't change

        Under Test:
            * ``TypeFilterPathOperator.yaml_keys``

        Given:
            * ``TypeFilterPathOperator``

        Expected:
            The `yaml_keys` of ``TypeFilterPathOperator`` is 'type'"""
        self.assertEqual(("type",), TypeFilterPathOperator.get_yaml_keys())

    def test_filter_type_apply_path(self):
        """Tests ``apply_path`` on applying the path operators correctly.

        Test-Purpose:
            Tests that the path operator ``TypeFilterPathOperator``
            applied correctly on the actual value

        Under Test:
            * ``apply_path``
            * implicit ``_get_path_operator``
            * implicit ``all_path_operators``

        Given:
            * `ifc_attribute`: Object of `IfcInstanceMock` with `ifc_type="MockTypeA"`
            * `other_ifc_attribute`: Object of `IfcInstanceMock` with `ifc_type="MockTypeB"`
            * `attributes`: list of `ifc_attribute` and `other_ifc_attribute`
            * `ifc_instance`: Object of ``IfcInstanceMock`` with list of `attributes`
            * list with the path operator ``ListPathOperator``, ``TypeFilterPathOperator``:
            `[{"type": "MockTypeA"}]`

        Expected:
            That the path operator ``TypeFilterPathOperator``
            get applied on the `ifc_instance` and that the `path_result` is `ifc_attribute`

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_attribute = IfcInstanceMock(
            Name="IfcMockA",
            GlobalId="IfcAttributeMockIdA",
            ifc_type="MockTypeA"
        )
        other_ifc_attribute = IfcInstanceMock(
            Name="IfcMockB",
            GlobalId="IfcAttributeMockIdB",
            ifc_type="MockTypeB"
        )
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType",
            attributes=[ifc_attribute, other_ifc_attribute]
        )
        path_operator = {"type": "MockTypeA"}
        operator = config.get_path_operator(path_operator, [ifc_instance])
        self.assertIsInstance(operator, TypeFilterPathOperator)
