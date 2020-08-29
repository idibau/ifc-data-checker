"""Get List Unit Test Suite"""
from ifc_data_checker.path_operators import ListPathOperator
from ifc_data_checker import config

from tests.path_operators.path_operator_test import TestPathOperator
from tests.helpers import IfcInstanceMock
from tests.helpers import MicroMock


class TestGetList(TestPathOperator.TestParameterValidation):
    """Test Get List Path Operator"""

    path_operator_class = ListPathOperator
    default_path_operator = {"list": "list_attribute"}

    def test_list(self):
        """Tests ``ListPathOperator`` on applying path operator correctly.

        Test-Purpose:
            Tests that each item of list of each instance gets selected by list name.

        Under Test:
            * ``ListPathOperator.apply``

        Given:
            * instances: List of Mock Instances, each matching the list selection
            * path_operator: The path operator defining the list selection

        Expected:
            A merged list of each list of the given instances.

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        instance = MicroMock(list_attribute=["string1", "string2", "string3"])
        instances = [instance, instance, instance]
        path_operator = {"list": "list_attribute"}
        expected_result = ["string1", "string2", "string3",
                           "string1", "string2", "string3",
                           "string1", "string2", "string3"]
        operator = ListPathOperator(instances, path_operator)
        self.assertEqual(expected_result, operator.apply())

    def test_list_not_found(self):
        """Tests ``ListPathOperator`` on handling errors correctly.

        Test-Purpose:
            error handling on missing list

        Under Test:
            * ``ListPathOperator.apply``

        Given:
            * instances: List of Mock Instances, no one of them matching the list selection
            * path_operator: The path operator defining the list selection

        Expected:
            Raises ``AttributeError`` because of none existing list defined in path operator

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        instance = MicroMock(list_attribute=["string1", "string2", "string3"])
        instances = [instance, instance, instance]
        path_operator = {"list": "nonexisting"}
        operator = ListPathOperator(instances, path_operator)
        self.assertRaises(AttributeError, operator.apply)

    def test_list_invalid_keyword(self):
        """Tests ``ListPathOperator`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `path_operator`

        Under Test:
            * ``ListPathOperator``

        Given:
            * instances: List of Mock Instances
            * path_operator: {"": "nonexisting"} and {"notlist": "nonexisting"}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and "notlist"

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        instance = MicroMock(list_attribute=["string1", "string2", "string3"])
        instances = [instance, instance, instance]
        path_operator = {"": "nonexisting"}
        self.assertRaises(ValueError, ListPathOperator, instances, path_operator)
        path_operator = {"notlist": "nonexisting"}
        self.assertRaises(ValueError, ListPathOperator, instances, path_operator)

    def test_list_invalid_list_attribute(self):
        """Tests ``ListPathOperator`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `path_operator`

        Under Test:
            * ``ListPathOperator.apply``

        Given:
            * instances: List of Mock Instances
            * path_operator: {"list": ""} and {"list": None}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and ``None``

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        instance = MicroMock(list_attribute=["string1", "string2", "string3"])
        instances = [instance, instance, instance]
        path_operator = {"list": ""}
        self.assertRaises(ValueError, ListPathOperator, instances, path_operator)
        path_operator = {"list": None}
        self.assertRaises(ValueError, ListPathOperator, instances, path_operator)

    def test_list_path_operator_yaml_keys(self):
        """Tests ``ListPathOperator`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``ListPathOperator`` won't change

        Under Test:
            * ``ListPathOperator.yaml_keys``

        Given:
            * ``ListPathOperator``

        Expected:
            The `yaml_keys` of ``ListPathOperator`` is 'list'"""
        self.assertEqual(("list",), ListPathOperator.get_yaml_keys())

    def test_list_get_path_operator(self):
        """Tests ``apply_path`` on applying the path operators correctly.

        Test-Purpose:
            Tests that the path operator ``ListPathOperator``
            applied correctly on the actual value

        Under Test:
            * ``apply_path``
            * implicit ``_get_path_operator``
            * implicit ``all_path_operators``

        Given:
            * `mock_list`: list of object of type `MicroMock`,
            including `ifc_attribute`, `other_ifc_attribute`
            * `ifc_attribute`: object of type `MicroMock` with `IsDefinedBy="MockWindow"`
            * `other_ifc_attribute`: object of type `MicroMock` with `IsDefinedBy="MockDoor"`
            * `ifc_instance`: Object of ``IfcInstanceMock`` with list of `mock_list`
            * list with the path operator ``ListPathOperator``: `[{"list": "IsDefinedBy"}]`

        Expected:
            That the path operator ``ListPathOperator``
            get applied on the `ifc_instance` and that the `path_result` is `ifc_attribute`

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType",
        )
        path_operator = {"list": "IsDefinedBy"}
        operator = config.get_path_operator(path_operator, [ifc_instance])
        self.assertIsInstance(operator, ListPathOperator)
