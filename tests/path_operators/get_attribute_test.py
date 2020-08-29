"""Get Attribute Unit Test Suite"""
from ifc_data_checker.path_operators import AttributePathOperator
from ifc_data_checker import config

from tests.path_operators.path_operator_test import TestPathOperator
from tests.helpers import IfcInstanceMock
from tests.helpers import MicroMock


class TestGetAttribute(TestPathOperator.TestParameterValidation):
    """Test Get Attribute Operator"""

    path_operator_class = AttributePathOperator
    default_path_operator = {"attribute": "property"}

    def test_attribute(self):
        """Tests ``AttributePathOperator`` on applying path operator correctly.

        Test-Purpose:
            Tests that each attribute of each instance gets selected by attribute name.

        Under Test:
            * ``AttributePathOperator.apply``

        Given:
            * instances: List of Mock Instances, each matching the attribute selection
            * path_operator: The path operator defining the attribute selection

        Expected:
            The same list as the given `instances` list,
            because every instance holding the expected attribute to select.

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        instance = MicroMock(property="property_value")
        instances = [instance, instance, instance]
        path_operator = {"attribute": "property"}
        expected_result = ["property_value",
                           "property_value",
                           "property_value"]
        operator = AttributePathOperator(instances, path_operator)
        self.assertEqual(expected_result, operator.apply())

    def test_attribute_not_found(self):
        """Tests ``AttributePathOperator`` on handling errors correctly.

        Test-Purpose:
            error handling on missing attribute

        Under Test:
            * ``AttributePathOperator.apply``

        Given:
            * instances: List of Mock Instances, no one of them matching the attribute selection
            * path_operator: The path operator defining the attribute selection

        Expected:
            Raises ``AttributeError`` because of none existing attribute defined in path operator

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        instance = MicroMock(property="property_value")
        instances = [instance, instance, instance]
        path_operator = {"attribute": "nonexisting"}
        operator = AttributePathOperator(instances, path_operator)
        self.assertRaises(AttributeError, operator.apply)

    def test_attribute_invalid_keyword(self):
        """Tests ``AttributePathOperator`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `path_operator`

        Under Test:
            * ``AttributePathOperator``

        Given:
            * instances: List of Mock Instances
            * path_operator: {"": "nonexisting"} and {"notattribute": "nonexisting"}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and "notattribute"

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        instance = MicroMock(list_attribute=["string1", "string2", "string3"])
        instances = [instance, instance, instance]
        path_operator = {"": "nonexisting"}
        self.assertRaises(ValueError, AttributePathOperator,
                          instances, path_operator)
        path_operator = {"notattribute": "nonexisting"}
        self.assertRaises(ValueError, AttributePathOperator,
                          instances, path_operator)

    def test_attribute_invalid_attribute(self):
        """Tests ``AttributePathOperator`` on validating parameters correctly.

        Test-Purpose:
            parameter validation on `path_operator`

        Under Test:
            * ``AttributePathOperator``

        Given:
            * instances: List of Mock Instances
            * path_operator: {"attribute": ""} and {"attribute": None}

        Expected:
            Raises ``ValueError`` because of invalid dict keyword "" and ``None``

        Comment:
            Usage of ``MicroMock`` to represent an instance"""
        instance = MicroMock(list_attribute=["string1", "string2", "string3"])
        instances = [instance, instance, instance]
        path_operator = {"attribute": ""}
        self.assertRaises(ValueError, AttributePathOperator,
                          instances, path_operator)
        path_operator = {"attribute": None}
        self.assertRaises(ValueError, AttributePathOperator,
                          instances, path_operator)

    def test_attribute_path_operator_yaml_keys(self):
        """Tests ``AttributePathOperator`` on the correct yaml keys

        Test-Purpose:
            Tests that the yaml keys of ``AttributePathOperator`` won't change

        Under Test:
            * ``AttributePathOperator.yaml_keys``

        Given:
            * ``AttributePathOperator``

        Expected:
            The `yaml_keys` of ``AttributePathOperator`` is 'attribute'"""
        self.assertEqual(("attribute",), AttributePathOperator.get_yaml_keys())

    def test_attribute_apply_path(self):
        """Tests ``apply_path`` on applying the path operators correctly.

        Test-Purpose:
            Tests that the path operator ``AttributePathOperator``
            applied correctly on the actual value

        Under Test:
            * ``apply_path``
            * implicit ``_get_path_operator``
            * implicit ``all_path_operators``

        Given:
            * ifc_instance: Object of ``IfcInstanceMock``
            * list with the path operator ``AttributePathOperator``:
            `[{"attribute": "IsDefinedBy"}]`

        Expected:
            That the path operator ``AttributePathOperator``
            get applied on the `ifc_instance` and that the `path_result` is "MockWindow"

        Comment:
            Usage of ``IfcInstanceMock`` to represent an ifc instance"""
        ifc_instance = IfcInstanceMock(
            Name="IfcMock",
            GlobalId="IfcMockId",
            ifc_type="MockType",
            IsDefinedBy="MockWindow"
        )
        path_operator = {"attribute": "IsDefinedBy"}
        operator = config.get_path_operator(path_operator, [ifc_instance])
        self.assertIsInstance(operator, AttributePathOperator)
